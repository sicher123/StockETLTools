# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
from datadesk.data_sync import *
from datadesk.props import set_config

dvp , dsp = set_config()
fp = './data'

def update_all(fp):
    h5 = hdf5_sync(fp,dvp,dsp) 
    sql = sql_sync(fp,dvp,dsp)
    try:
        h5.create_daily()
        h5.update_daily()
    except:
        raise ValueError('Error when update daily')
        
    try:
        sql.update_data()
    except:
        raise ValueError('Error when update lb data')
        

update_all(fp)