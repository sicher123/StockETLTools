# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import os
import ast
from datasync.props.guojin_props import read_config
from datasync.data_origin.sql_origin import *
#from datasync.sync import distributed
from datasync.dataReceiver.hdf5 import DailyDB
import datasync.utils as utils
from datetime import datetime,timedelta
from datasync.dataReceiver.sqlite import sqlite_db
from datasync.data_origin.jaqs_origin import DataServiceOrigin


today = int(datetime.strftime(datetime.now(),'%Y%m%d'))

def write(view,df):
    df['TRADE_DT'] = df['TRADE_DT'].astype(int)
    if view == 'dbo.ASHAREEODPRICES':
        df = df[~df['OBJECT_ID'].isin(['{56FBE7CC-D183-11E6-A487-6C0B84A6895D}', '{56FBE85B-D183-11E6-A487-6C0B84A6895D}'])]

    if 'S_DQ_TRADESTATUS' in df.columns.values:
        print (df['S_DQ_TRADESTATUS'])
        df['S_DQ_TRADESTATUS'] = df['S_DQ_TRADESTATUS'].apply(lambda x:x.encode('latin1').decode('gbk') if isinstance(x,str) else x)
        df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '交易'] = '1'
        df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '停牌'] = '0'

    db = DailyDB(fp, view)
    for i in df.columns:
        data = df.pivot(index='TRADE_DT', columns='S_INFO_WINDCODE', values=i)
        try:
            data = df.pivot(index='TRADE_DT', columns='S_INFO_WINDCODE', values=i)
            db.update_a_file(data,i)
            db.set_attr({i: today})
            logger.info('%s -  %s data has been updated' % (view, i), exc_info=True)
        except Exception as e:
            print (i,'fail')
            logger.error('%s - %s update failed ,error as %s'%(view,i,e), exc_info=True)

def sync_daily(v,origin,large_data=False):
    try:
        view = v['view']
        db = DailyDB(fp, view)
        date = db.get_update_info('date')
        if date:
            v['start_date'] = date
            v['end_date'] = today
        logger.info('%s start query' % (view), exc_info=True)

        if large_data == True:
            from datasync.sync import distribute
            for props in distribute(v):
                df = origin.read(props = props)
        else:
            if view == 'dbo.ASHAREEODPRICES':
                symbol_df = origin.read(props=v)
                index_df = origin.read(props = index_config)
                df = pd.concat([index_df,symbol_df])
            else:
                df = origin.read(props=v)
    except Exception as e:
        if e:
            logger.error('%s query failed ,error as %s' % (view, e), exc_info=True)
        else:
            logger.error('%s query failed ,error as %s' % (view, e), exc_info=True)

    if 'df' in dir() and len(df) > 0:
        write(view,df)
    else:
        logger.info('%s data not been updated,local last date %s' % (view,date), exc_info=True)

def sync_lb_data():
    config = read_config('lb_data')

    for k, v in config.items():
        try:
            name = k.split('.')[-1]

            fp = v.pop('folder_path')
            db = sqlite_db(fp)
            info = db.get_update_info(name)
            if info:
                print (info)
                v['start_date'] = info
            v['end_date'] = today

            db_config = ast.literal_eval(v.pop('db_config'))
            origin = globals()[v.pop('origin')](db_config)
            df = origin.read(props=v)

            if 'ZYYX' in k:
                df['STOCK_CODE'] = utils.trans_symbol(list(df['STOCK_CODE'].values))
                df['CON_DATE'] = df['CON_DATE'].apply(lambda x: datetime.strftime(x.to_datetime(), '%Y%m%d') if x != pd.NaT else 'NaT')
                print (time() - start)

                for field in ['CON_OR_HISDATE', 'CON_NP_HISDATE', 'CON_EPS_HISDATE', 'ENTRYTIME', 'UPDATETIME']:
                    print (field)
                    df[field] = df[field].astype(str)

                    def func(x):
                        if len(x) == 10:
                            return x[:4] + x[5:7] + x[-2:]
                        else:
                            return x

                    df[field] = df[field].apply(lambda x: func(x))

            if 'jz' in k:
                db.update_table(k,df,if_exists='replace')
            else:
                db.update_table(k, df, if_exists='append')
                db.set_attr(name,{name: today})
                db.conn.close()
            logger.info('%s data has been updated' % (k), exc_info=True)
        except Exception as e:
            logger.error('%s update failed ,error as %s' % (k,e), exc_info=True)

def run():
    global fp
    global logger
    fp = os.path.abspath(os.path.expanduser('~/Desktop/hdf5_docs'))
    config = read_config('daily_data')
    logger = utils.logger(today,fp)

    if 'index_config' not in globals():
        global index_config
    index_config = config.pop('dbo.AINDEXEODPRICES')
    index_config.pop('db_config')
    index_config.pop('origin')
    index_config.pop('folder_path')
    index_config['view'] = 'dbo.AINDEXEODPRICES'

    for k, v in config.items():
        v['start_date'] = 20180601
        fp = v.pop('folder_path')
        db_config = ast.literal_eval(v.pop('db_config'))
        origin = globals()[v.pop('origin')](db_config)
        v['view'] = k
        sync_daily(v, origin)


if __name__ == "__main__":
    run()
    sync_lb_data()

    '''
    import time
    from time import sleep
    SECONDS_PER_DAY = 24 * 60 * 60

    while True:
        curTime = datetime.now()
        print (curTime)
        nexTime = curTime + timedelta(days=1)
        desTime = nexTime.replace(day=curTime.day+1,hour=8, minute=0, second=0, microsecond=0)
        print (desTime)
        delta =  desTime - curTime
        print (delta)
        skipSeconds = delta.total_seconds()
        print ("Next day must sleep %d seconds" % skipSeconds)
        sleep(skipSeconds)
        run()
    '''