# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
from datasync.props.jaqs_props import set_config
from datasync.data_origin.jaqs_origin import DataServiceOrigin
from datasync.dataReceiver.hdf5 import DailyDB
from datasync.utils import logger
from copy import copy
import os

#fp = r'C:\Users\xinger\Sync\data1'
fp = r'C:\Users\xinger\Desktop\data1'
config = set_config()
logger = logger(fp)


def sync_one(k,v,origin):
    view = k
    logger.info('%s start' % (view), exc_info=True)
    df = origin.read(props = v,limit=500)
    df['trade_date'] = df['trade_date'].astype(int)
    if view == 'adjust':
        view = 'STOCK_D'

    if view == 'adjust_factor':
        view = 'STOCK_D'

    db = DailyDB(fp, view)
    for i in df.columns:
        data = df.pivot(index='trade_date', columns='symbol', values=i)
        try:
            db.update_a_file(data,i)
            logger.info('%s - %s data has been updated' % (view, i), exc_info=True)
        except Exception as e:
            logger.error('%s - %s update failed ,error as %s'%(view,i,e), exc_info=True)
'''
for k, v in config.items():
    #date = db.get_info('last_updated_date')
    fields = copy(v['fields'])
    db_config = v.pop('db_config')
    origin = globals()[v.pop('origin')](db_config)
    v['view'] = k
    sync_one(k, v, origin)
'''

def run():
    for k, v in config.items():
        #date = db.get_info('last_updated_date')
        fields = copy(v['fields'])
        db_config = v.pop('db_config')
        origin = globals()[v.pop('origin')](db_config)
        view = k
        start_date = v['start_date']
        end_date = v['end_date']
        v['view'] = view
        #sync_one(k, v, origin)

        import math
        num = math.floor((end_date - start_date)/10000)

        for i in range(num):
            props = {}
            props['start_date'] = start_date + i*10000
            props['end_date'] = start_date + (i+1)*10000
            props['view'] = view
            props['fields'] = fields
            sync_one(k, props, origin)

if __name__ == '__main__':
    from datetime import datetime ,timedelta
    time = datetime.now().date()
    while True:
        today = datetime.now().date()
        if today == time and today.weekday() not in [5,6]:
            run()
        time = today + timedelta(days=1)

