import os
import math
import pathlib
from datetime import datetime, timedelta

from datasync.log import Log
from datasync.dataReceiver.sqlite import sqlite_db
from datasync.data_origin.mongodb_origin import MongodbOrigin
from datasync.utils import get_config

config = get_config(pathlib.Path(__file__).absolute().parent.parent)
fp = config["fp"]
lb_views = config["lb_views"]
mongo_db_config = config["mongo_db_config"]
lb_update_type = config["lb_update_type"]
default_start_date = config["default_start_date"]
default_future_date = config["default_future_date"]

today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
yestoday = int(datetime.strftime(datetime.today() - timedelta(days=1), '%Y%m%d'))
logger = Log(os.path.join(fp, "log"), today)
origin = MongodbOrigin(mongo_db_config)
mongo_log = origin.get_last_log()


def loop(func, n=0):
    def wrapper(n=n):
        while True:
            if check_date():
                logger.info('hdf5 data check success')
                break
            else:
                n += 1
                func()
                if n > 3:
                    logger.error('hdf5 data check failed')
                    break
        return func()
    return wrapper


def get_from_jaqs(props):
    from datasync.data_origin.jaqs_origin import DataServiceOrigin
    props['fields'] = ''

    addr = "tcp://data.quantos.org:8910"
    name = "13243828068"
    passwd = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MTUwNDk5MzI2MDAiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTMyNDM4MjgwNjgifQ.KpmnMkuO7ApTWvBAwgvHwWDkmoasBIdQHl2gQJVmqIA'

    jaqs_config = {'addr': addr,
                   'user': name,
                   'password': passwd}

    dsorigin = DataServiceOrigin(jaqs_config)
    df = dsorigin.read(props=props)
    return df


def lb_sync_one(props, db, if_exists='append'):
    view = props['view']
    logger.info('%s start update' % (view,))

    if view in ['lb.indexCons', 'jz.secTradeCal']:
        df = origin.read(props, is_filter=False)
    else:
        df = origin.read(props)

    if view == 'jz.apiParam':
        df = df[~df['api'].isin(['lb.windFinance'])]
        view = 'help.predefine'

    if view == 'lb.indexCons':
        df['index_code'][df['index_code'] == '399300.SZ'] = '000300.SH'
    try:
        db.update_table(view, df, if_exists=if_exists)
        logger.info('%s data has been updated' % (view,))
    except Exception as e:
        print('updated failed', view)
        logger.error('%s update failed ,error as %s' % (view, e))
        pass


def dst_upd(props, db):
    start_date = props.get('start_date')
    end_date = props.get('end_date')
    view = props.get('view')

    num = math.floor((end_date - start_date) / 10000) + 1
    for i in range(int(num)):
        props['start_date'] = start_date + i * 10000
        if start_date + (i + 1) * 10000 < end_date:
            props['end_date'] = start_date + (i + 1) * 10000
        else:
            props['end_date'] = end_date

        if '.' in view:
            lb_sync_one(props, db)


def update_lb(update_type='add'):
    for view in lb_views:
        db = sqlite_db(fp)
        date_info = db.get_update_info(view)
        end_date = today
        if date_info:
            start_date = date_info
            if view.replace('.', '_') in mongo_log.columns:
                update_flag = mongo_log[view.replace('.', '_')][0]
                if update_flag <= 0:
                    logger.info('origin not updated new data on table-%s' % (view, ))
                    continue
                else:
                    end_date = int(mongo_log.index[0])
        else:
            start_date = default_start_date
            end_date = today

        spc_view_list = ['lb.cashFlow', 'lb.income', 'lb.balanceSheet', 'lb.finIndicator''lb.profitExpress', 'lb.secDividend']
        if update_type == 'replace' and view in spc_view_list:
            # noinspection PyBroadException
            try:
                db.execute('''DROP TABLE "%s";''' % (view, ))
            except Exception:
                pass
            start_date = default_start_date

        if start_date == end_date:
            logger.info('date-- %s ,view -- %s data is the newest' % (start_date, view))
            continue

        print('%s start query, start_date:%s, end_date: %s' % (view, start_date, end_date))

        props = {'view': view,
                 'start_date': start_date,
                 'end_date': end_date}
        if view == 'jz.secTradeCal':
            props['start_date'] = default_start_date

        if view in ['lb.cashFlow', 'lb.income', 'lb.balanceSheet', 'lb.finIndicator', 'lb.indexWeightRange','lb.secAdjFactor']:
            dst_upd(props, db)

        elif view in ['jz.instrumentInfo', 'jz.apiParam', 'jz.secTradeCal', 'lb.indexCons']:
            props['end_date'] = default_future_date
            lb_sync_one(props, db, if_exists='replace')
        else:
            # props['start_date'] = 19990101
            lb_sync_one(props, db)

    db.update_attr()
    db.conn.close()


def test_data():
    props = {
            'view': 'SecDailyIndicator',
            'start_date': 20180714,
            'end_date': 20180717
            }
    data = origin.read(props)
    return data


def check_date():
    from jaqs_fxdayu.data.dataservice import LocalDataService
    ds = LocalDataService(fp)
    try:
        info = ds._get_last_updated_date()
        dates = info[info['freq'] == '1d']['updated_date'].values
    except Exception:
        return False
    if len(list(set(dates))) > 1:
        return False
    elif int(dates[0]) not in [today, yestoday]:
        return False
    else:
        return True


if __name__ == '__main__':
    update_lb()
