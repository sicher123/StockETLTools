# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import os
import pandas as pd
from datetime import datetime
today = int(datetime.strftime(datetime.today(),'%Y%m%d'))

#daily_db = ['STOCK_D']
daily_db = ['SecDailyIndicator', 'STOCK_D', 'adjust_factor']
db_config = {'addr': 'tcp://192.168.0.102:23000','user':'1','password':'2'}

symbol = ''
start_date = 20080101
today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
end_date = today

import configparser
config = configparser.ConfigParser()
config.read(r"C:\Users\xinger\Desktop\git\DataSync\datasync\config\conf.ini")
field_dic = {}
for k,v in config['fields'].items():
    field_dic[k] = v.split(',')


def set_config():
    dic = {}
    for i in daily_db:
        dic[i] = {}
        fields = field_dic[i.lower()]
        dic[i]['fields'] = ','.join(set(fields + ['trade_date', 'symbol']))
        dic[i]['db_config'] = db_config
        dic[i]['start_date'] = start_date
        dic[i]['end_date'] = end_date
        dic[i]['symbol'] = ''
        dic[i]['origin'] = 'DataServiceOrigin'
        dic[i]['DATE_NAME'] = 'trade_date'
    return dic


def read_config(sheet_name,config_path = None):
    if config_path == None:
        config_path = os.path.abspath(os.path.expanduser('~/Desktop')) + '\\sync_docs\\config.xlsx'
    config = pd.read_excel(config_path,sheet_name = sheet_name)
    config = config.fillna('')
    return config.to_dict()


def read_json():
    pass


def read_config(sheet_name, config_path=None):
    if config_path == None:
        config_path = os.path.abspath(os.path.expanduser('~/Desktop')) + '\\hdf5_docs\\config.xlsx'
    config = pd.read_excel(config_path,sheet_name = sheet_name)
    config = config.fillna('')
    return config.to_dict()

