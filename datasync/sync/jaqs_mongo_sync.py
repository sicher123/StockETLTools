import math
import json
import numpy as np
from datetime import datetime, timedelta
from datasync.log import Log
from datasync.dataReceiver.hdf5 import DailyDB
from datasync.dataReceiver.sqlite import sqlite_db
from datasync.data_origin.mongodb_origin import MongodbOrigin

today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
yestoday = int(datetime.strftime(datetime.today() - timedelta(days=1), '%Y%m%d'))
fp = r'C:\Users\xinger\Sync\data'
logger = Log(fp+'//log', today)
db_config = {'addr': '192.168.0.104'}
origin = MongodbOrigin(db_config)
mongo_log = origin.get_last_log()
default_start_date = 19990101
default_furture_date = 20200101


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
    view = props['view']

    addr = "tcp://data.quantos.org:8910"
    name = "13243828068"
    passwd = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MTUwNDk5MzI2MDAiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTMyNDM4MjgwNjgifQ.KpmnMkuO7ApTWvBAwgvHwWDkmoasBIdQHl2gQJVmqIA'

    db_config = {'addr': addr,
                'user': name,
                'password': passwd}

    dsorigin = DataServiceOrigin(db_config)
    df = dsorigin.read(props=props)
    df = df.drop(['presettle', 'settle', 'preclose', 'oi'], axis=1)
    df = df.replace('交易', 1)
    df = df.replace('停牌', 0)
    return df


def h5_sync_one(props, db):
    view = props['view']
    print('%s start sync' % (view,))
    logger.info('%s start update' % (view,))
    if view != 'Stock_D':
        df = origin.read(props)
    else:
        '''
        df['code'] = df['symbol'].apply(lambda x: x.split('.')[0])
        df['freq'] = '1d'
        df['vwap'] = df['turnover']/df['volume']

        data = df.loc[:, ['trade_date', 'symbol', 'open']]
        data = data.pivot(index='trade_date', columns='symbol', values='open')
        data[~data.isna()] = 1
        data[data.isna()] = 0
        db.update_a_file(data, 'trade_status')
        db.set_attr('trade_status', {'updated_date': props['end_date']})
        '''
        df = get_from_jaqs(props)

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
        else:
            h5_sync_one(props, db)


def sync_adjfactor(props):
    db = DailyDB(fp, 'Stock_D')
    view = 'lb.secAdjFactor'
    logger.info('%s start update' % (view,))
    props['view'] = view
    df = origin.read(props)
    df = df[df['symbol'].apply(lambda x:x[0] in ('0', '3', '6'))]
    df = df.pivot_table(index='trade_date', columns='symbol', values='adjust_factor', aggfunc=np.mean)
    try:
        db.update_a_file(df, 'adjust_factor')
        db.set_attr('adjust_factor', {'updated_date': props['end_date']})
        logger.info('%s data has been updated' % (view,))
    except Exception as e:
        logger.error('%s update failed ,error as %s' % (view, e))

@loop
def update_daily():
    daily_views = ['Stock_D', 'SecDailyIndicator']

    for view in daily_views:
        db = DailyDB(fp, view)
        date_info = db.get_update_info()
        if date_info:
            print(date_info)
            start_date = int(date_info)
            try:
                update_flag = mongo_log[view][0]
                if update_flag <= 0:
                    logger.info('%s mongodb data not updated today' % (view,))
                    continue
                else:
                    end_date = int(mongo_log.index[0])
            except:
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

        h5_sync_one(props, db)
        #dst_upd(props, db)

        if view == 'Stock_D':
            sync_adjfactor(props)


def update_lb():
    lb_views = ['lb.cashFlow', 'lb.income', 'lb.balanceSheet', 'lb.finIndicator',
                'lb.indexCons', 'jz.secTradeCal', 'lb.secIndustry', 'jz.apiParam',
                'lb.profitExpress', 'lb.secDividend', 'lb.indexWeightRange',
                'jz.instrumentInfo']

    for view in lb_views:
        db = sqlite_db(fp)
        date_info = db.get_update_info(view)
        print(view, date_info)
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

        if start_date == end_date:
            logger.info('date-- %s ,view -- %s data is the newest' % (start_date, view))
            continue

        props = {'view': view,
                 'start_date': start_date,
                 'end_date': end_date}
        if view == 'jz.secTradeCal':
            props['start_date'] = default_start_date

        if view in ['lb.cashFlow', 'lb.income', 'lb.balanceSheet', 'lb.finIndicator', 'lb.indexWeightRange']:
            dst_upd(props, db)
        elif view in ['jz.instrumentInfo', 'jz.apiParam', 'jz.secTradeCal', 'lb.indexCons']:
            props['end_date'] = default_furture_date
            lb_sync_one(props, db, if_exists='replace')
        else:
            #props['start_date'] = 19990101
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


def check_date():
    from jaqs_fxdayu.data.dataservice import LocalDataService
    ds = LocalDataService(fp)
    info = ds._get_last_updated_date()
    dates = info[info['freq'] == '1d']['updated_date'].values
    if len(list(set(dates))) > 1:
        return False
    elif int(dates[0]) not in [today, yestoday]:
        return False
    else:
        return True


if __name__ == '__main__':
    update_lb()
    update_daily()

