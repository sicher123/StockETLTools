# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""

from datadesk.props import set_config
from datadesk.data_origin import *
from datadesk.dataReceiver.hdf5 import DailyDB
from datadesk.utils import logger
from copy import copy

fp = r'C:\Users\bigfish01\Desktop\data'
config = set_config()
db = DailyDB(fp,'daily')
logger = logger(fp)
ORIGIN_MAP = {}

def sync_one(k,v,origin):
    view = k

    logger.info('%s start' % (view), exc_info=True)
    df = origin.read(props = v)

    if 'S_DQ_TRADESTATUS' in df.columns.values:
        df['S_DQ_TRADESTATUS'] = df['S_DQ_TRADESTATUS'].apply(lambda x:x.encode('latin1').decode('gbk'))
        df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '交易'] = '1'
        df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '停牌'] = '0'

    #if view == 'dbo.AINDEXEODPRICES':
    #    df = df[df['S_INFO_WINDCODE'].isin([i for i in df['S_INFO_WINDCODE'] if i[-2:] in ['SZ','SH']])]

    for i in df.columns:
        data = df.pivot(index='TRADE_DT', columns='S_INFO_WINDCODE', values=i)
        if i == 'OBJECT_ID':
            i = view + '_OBJECT_ID'
        try:
            db.update_a_file(data,i)
            logger.info('%s - %s data has been updated' % (view, i), exc_info=True)
        except Exception as e:
            logger.error('%s - %s update failed ,error as e'%(view,i,e), exc_info=True)

for k, v in config.items():
    db_config = v.pop('db_config')
    origin = globals()[v.pop('origin')](db_config)
    view = k
    v['view'] = view

    prop = copy(v)
    try:
        file = db.get_file(view + '_OBJECT_ID')
        if len(file.keys()) > 0:
            data = file['data'][:].astype(str)
            exist_id = list(data.reshape(data.shape[0]*data.shape[1]))
            v['fields'] = 'OBJECT_ID'
            df = origin.read(props=v)
            _id = list(set(df['OBJECT_ID'].values)-set(exist_id))
        else:
            _id = []
    except:
        _id = []

        _id = ','.join(_id)
        prop['OBJECT_ID'] = _id
        sync_one(k,prop,origin)

#if __name__ == '__main__':
#    run()