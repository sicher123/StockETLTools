import os
import math
import pathlib
from datetime import datetime, timedelta
from datasync.log import Log
from datasync.dataReceiver.hdf5 import DailyDB
from datasync.data_origin.mongodb_origin import MongodbOrigin
from datasync.utils import get_config

config = get_config(pathlib.Path(__file__).absolute().parent.parent)
fp = config["fp"]

daily_views = config["daily_views"]
mongo_db_config = config["mongo_db_config"]
default_start_date = config["default_start_date"]

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
    df = df.drop(['presettle', 'settle', 'preclose', 'oi'], axis=1)
    df = df.replace('交易', 1)
    df = df.replace('停牌', 0)
    return df


def h5_sync_one(props, db):
    view = props['view']
    print('%s start sync' % (view,))
    logger.info('%s start update' % (view,))
    df = origin.read(props)

    if view == 'Stock_D':
        df['code'] = df['symbol'].apply(lambda x: x.split('.')[0])
        df['freq'] = '1d'
        df['vwap'] = df['turnover']/df['volume']

        data = df.loc[:, ['trade_date', 'symbol', 'open']]
        data = data.pivot(index='trade_date', columns='symbol', values='open')
        data[~data.isna()] = 1
        data[data.isna()] = 0
        db.update_a_file(data, 'trade_status')
        db.set_attr('trade_status', {'updated_date': props['end_date']})
        # df = get_from_jaqs(props)


    for i in df.columns:
        data = df.pivot(index='trade_date', columns='symbol', values=i)
        if i in ['trade_date']:
            data = data.fillna(method='ffill', axis=1).astype(int)
        try:
            db.update_a_file(data, i)
            db.set_attr(i, {'updated_date': props.get('end_date')})
            logger.info('%s - %s data has been updated' % (view, i))
        except Exception as e:
            pass
            logger.error('%s - %s update failed ,error as %s' % (view, i, e))


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

        h5_sync_one(props, db)


def update_daily():
    for view in daily_views:
        db = DailyDB(fp, view)
        date_info = db.get_update_info()
        if date_info:
            print(date_info)
            start_date = int(date_info)

            # noinspection PyBroadException
            try:
                update_flag = mongo_log[view][0]
                if update_flag <= 0:
                    logger.info('%s mongodb data not updated today' % (view,))
                    continue
                else:
                    end_date = int(mongo_log.index[0])
            except Exception:
                end_date = int(mongo_log.index[0])
        else:
            start_date = default_start_date
            end_date = today

        if start_date == end_date:
            logger.info('date -- %s ,view -- %s data is the newest' % (start_date, view))
            continue

        props = {'view': view,
                 'start_date': start_date,
                 'end_date': end_date}

        print(view, props)

        # h5_sync_one(props, db)
        dst_upd(props, db)


def test_data():
    props = {
            'view': 'Stock_D',
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
    update_daily()


'''
def adjfactor_to_hd5(props):
    db = DailyDB(fp, 'Stock_D')
    view = 'lb.secAdjFactor'
    logger.info('%s start update' % (view,))
    props['view'] = view
    df = origin.read(props)
    df = df[df['symbol'].apply(lambda x:x[0] in ('0', '3', '6'))]
    df = df.pivot_table(index='trade_date', columns='symbol', values='adjust_factor', aggfunc=np.mean)
    df = df.ffill()
    try:
        db.update_a_file(df, 'adjust_factor')
        db.set_attr('adjust_factor', {'updated_date': props['end_date']})
        logger.info('%s data has been updated' % (view,))
    except Exception as e:
        logger.error('%s update failed ,error as %s' % (view, e))
'''
