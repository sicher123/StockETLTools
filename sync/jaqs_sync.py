# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""

import math
from copy import copy
from datetime import datetime
from datasync.utils import logger
from datasync.storage.hdf5 import DailyDB
from datasync.props.jaqs_props import set_config
from datasync.origin.jaqs_origin import DataServiceOrigin

today = int(datetime.strftime(datetime.today(), '%Y%m%d'))

fp = r'C:\Users\xinger\Sync\data'
config = set_config()
logger = logger(today, fp)

db_config = {'addr': 'tcp://192.168.0.104:23000', 'password': '2', 'user': '1'}

config = {'STOCK_D': {'DATE_NAME': 'trade_date',
          'db_config': db_config,
          'end_date': today,
          'fields': '',
          'origin': 'DataServiceOrigin',
          'start_date': 19990101,
          'symbol': ''},
          'SecDailyIndicator': {'DATE_NAME': 'trade_date',
                                'db_config': db_config,
                                'end_date': today,
                                'fields': 'pe,oper_rev_lyr,oper_rev_ttm,ps_ttm,np_parent_comp_ttm,ncf_oper_lyr,float_mv,total_mv,ncf_oper_ttm,pcf_ocf,turnover_ratio,free_share,pcf_ocfttm,free_turnover_ratio,total_share,pcf_ncfttm,trade_date,pe_ttm,price_div_dps,symbol,pb,float_share,limit_status,pcf_ncf,ps,net_assets,np_parent_comp_lyr',
                                'origin': 'DataServiceOrigin',
                                'start_date': 19990101,
                                'symbol': ''},
         'adjust_factor': {'DATE_NAME': 'trade_date',
          'db_config': db_config,
          'end_date': today,
          'fields': 'trade_date,adjust_factor,symbol',
          'origin': 'DataServiceOrigin',
          'start_date': 19990101,
          'symbol': ''}}

def sync_one(k, v, origin):
    view = k
    logger.info('%s start' % (view,), exc_info=True)
    df = origin.read(props=v, limit=500)
    df['trade_date'] = df['trade_date'].astype(int)
    if view == 'adjust_factor':
        view = 'STOCK_D'

    db = DailyDB(fp, view)
    for i in df.columns:
        data = df.pivot(index='trade_date', columns='symbol', values=i)
        try:
            db.update_a_file(data, i)
            db.set_attr({'updated_date': v['end_date']})
            logger.info('%s - %s data has been updated' % (view, i), exc_info=True)
        except Exception as e:
            logger.error('%s - %s update failed ,error as %s' % (view, i, e), exc_info=True)


def run_one(k, v):
    db_config = v.pop('db_config')
    origin = globals()[v.pop('origin')](db_config)

    db = DailyDB(fp, k)
    date_info = db.get_update_info()
    if date_info:
        print(date_info)
        start_date = date_info
    else:
        start_date = 19990101
    end_date = today
    if start_date == end_date:
        print ('data is the newest')
        return

    if (end_date - start_date) > 10000:
        num = math.floor((end_date - start_date) / 10000) + 1
        for i in range(int(num)):
            props = dict()
            props['start_date'] = start_date + i*10000
            if start_date + (i+1)*10000 < end_date:
                props['end_date'] = start_date + (i+1)*10000
            else:
                props['end_date'] = end_date
            props['view'] = k
            props['fields'] = copy(v['fields'])
            sync_one(k, props, origin)
    else:
        v['view'] = k
        sync_one(k, v, origin)

def run_daily():
    k = 'STOCK_D'
    v = config[k]
    run_one(k, v)

if __name__ == '__main__':
    #for k, v in config.items():
    pass
    #from datasync.sync.jaqs_mongo_sync import update_lb
    #update_lb()

