import os
import math
import pymongo
from datetime import datetime, timedelta
from datasync.log import Log
from datasync.storage.hdf5 import DailyDB
from datasync.origin.mongodb_origin import MongodbOrigin
import pandas as pd


today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
yestoday = int(datetime.strftime(datetime.today() - timedelta(days=1), '%Y%m%d'))
fp = r'D:/new_data'


def update_coin():
    MONGO_DB_CONFIG = {"addr": '192.168.0.104'}
    origin = MongodbOrigin(MONGO_DB_CONFIG)
    COIN_MIN_DB = 'VnTrader_1Min_Db'
    COIN_MIN_COL = ['BTCUSDT:binance',
                    'EOSUSDT:binance',
                    'ETHUSDT:binance',
                    'XRPUSDT:binance'
                    ]

    props = {'view': COIN_MIN_DB,
             'symbol': ','.join(COIN_MIN_COL),
             'start_date': 20180101,
             'end_date': 20190112
             }

    df = origin.read(props)

    df['datetime'] =df['date']+ ' ' + df['time']
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date_flag'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H%M%S'))
    import ctypes
    df['date_flag'] = df['date_flag'].astype(ctypes.c_int64)
    df['datetime'] = df['datetime'].astype(str)
    df = df.drop(['trade_date','symbol'], axis=1)
    df = df.drop_duplicates(subset=['date_flag', 'symbol'])
    db = DailyDB(fp, COIN_MIN_DB)

    def daily_updater(db, df):
        for i in df.columns:
            if i not in ['date_flag', 'symbol']:
                data = df.pivot(index='date_flag', columns='symbol', values=i)
                db.update_a_file(data, i)

    daily_updater(db, df)



def update_ctp():
    MONGO_DB_CONFIG = {"addr": '192.168.0.104'}
    origin = MongodbOrigin(MONGO_DB_CONFIG)
    dbname = 'VnTrader_1Min_Db'

    symbol = 'RB88:CTP,HC88:CTP,CU88:CTP,AL88:CTP,ZN88:CTP,PB88:CTP,RU88:CTP,' \
             'AU88:CTP,AG88:CTP,BU88:CTP,NI88:CTP,SN88:CTP,A88:CTP,B88:CTP,M88:CTP,' \
             'Y88:CTP,L88:CTP,P88:CTP,C88:CTP,V88:CTP,J88:CTP,JM88:CTP,I88:CTP,' \
             'FB88:CTP,PP88:CTP,JD88:CTP,BB88:CTP,CS88:CTP,WH88:CTP,PM88:CTP,CF88:CTP,' \
             'SR88:CTP,TA88:CTP,OI88:CTP,RI88:CTP,MA88:CTP,FG88:CTP,RS88:CTP,RM88:CTP,' \
             'ZC88:CTP,SF88:CTP,SM88:CTP,LR88:CTP,JR88:CTP,IF88:CTP,IH88:CTP,' \
             'IC88:CTP,TF88:CTP,T88:CTP,SC88:CTP'

    props = {'view': dbname,
             'symbol': symbol,
             'start_date': 20160101,
             'end_date': 20190112
             }

    df = origin.read(props)

    df['datetime'] =df['date'] + ' ' + df['time']
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date_flag'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H%M%S'))
    import ctypes
    df['date_flag'] = df['date_flag'].astype(ctypes.c_int64)
    df['datetime'] = df['datetime'].astype(str)
    df = df.drop_duplicates(subset=['date_flag', 'symbol'])
    df = df.drop(['trade_date'], axis=1)
    db = DailyDB(fp, 'CTP1')

    def daily_updater(db, df):
        for i in df.columns:
            if i not in ['date_flag']:
                data = df.pivot(index='date_flag', columns='symbol', values=i)
                db.update_a_file(data, i)

    daily_updater(db, df)


def update_furture():
    HOST = '192.168.0.104'
    PORT = 27017
    DBName = 'future_1M'

    def get_db(host, port, db_name):
        client = pymongo.MongoClient(host, port)
        return client[db_name]

    def get_col_data(db, col_name):
        try:
            cursor = db[col_name].find({'datetime': {'$gt': datetime(2018, 5, 1)}}, {'_id': 0, '_l': 0})
            df = pd.concat([pd.DataFrame(i) for i in cursor])
            df['symbol'] = col_name
            return df
        except Exception as e:
            print(col_name, e)

    db = get_db(HOST, PORT, DBName)
    col_names = db.collection_names()[:10]
    col_data = [get_col_data(db, name) for name in col_names]
    df = pd.concat(col_data)
    df = df.drop('_d', axis=1)
    df['date_flag'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H%M%S'))
    import ctypes
    df['date_flag'] = df['date_flag'].astype(ctypes.c_int64)
    df['datetime'] = df['datetime'].astype(str)
    df = df.drop_duplicates(subset=['date_flag', 'symbol'])
    db = DailyDB(fp, DBName)

    def daily_updater(db, df):
        for i in df.columns:
            if i not in ['date_flag','symbol']:
                data = df.pivot(index='date_flag', columns='symbol', values=i)
                db.update_a_file(data, i)

    daily_updater(db, df)

