# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
from datetime import datetime
#dict = [daily_field,indi_field,factors,ajd_field]
today = int(datetime.strftime(datetime.today(),'%Y%m%d'))

import configparser
config = configparser.ConfigParser()
config.read(r"C:\Users\xinger\Desktop\git\DataSync\config\conf.ini")
field_dic = {}
for k,v in config['fields'].items():
    field_dic[k] = v.split(',')


daily_db = ['SecDailyIndicator','STOCK_D','adjust_factor','adjust']
#daily_db = ['STOCK_D']
db_config = {'addr':'tcp://192.168.0.102:23000','user':'1','password':'2'}

symbol = ''
start_date = 20180501
today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
end_date = today

def set_config():
    dic = {}
    for i in daily_db:
        dic[i] = {}
        fields = field_dic[i.lower()]
        dic[i]['fields'] = ','.join(set(list(fields) + ['trade_date','symbol']))
        dic[i]['db_config'] = db_config
        dic[i]['start_date'] = start_date
        dic[i]['end_date'] = end_date
        dic[i]['symbol'] = ''
        dic[i]['origin'] = 'DataServiceOrigin'
        dic[i]['DATE_NAME'] = 'trade_date'
    return dic
