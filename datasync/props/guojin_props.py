# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import pandas as pd
from datetime import datetime
import openpyxl

daily_db = ['dbo.ASHAREEODDERIVATIVEINDICATOR','dbo.ASHAREEODPRICES','dbo.AINDEXEODPRICES']
db_config = {'host': "172.16.100.7",
             'user': "bigfish01",
             'password': "bigfish01@0514"}
symbol = ''
start_date = 20180501
today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
end_date = today

def set_config():
    data = pd.read_excel(r'datadesk/config/name_map.xlsx')
    dic = {}
    for i in daily_db:
        dic[i] = {}
        fields = data['windColumnName'][data['windTableName'] == i].values
        dic[i]['fields'] = ','.join(set(list(fields) + ['S_INFO_WINDCODE', 'TRADE_DT','OBJECT_ID']))
        dic[i]['db_config'] = db_config
        dic[i]['start_date'] = start_date
        dic[i]['end_date'] = end_date
        dic[i]['symbol'] = ''
        dic[i]['origin'] = 'MSSqlOrigin'
        dic[i]['DATE_NAME'] = 'TRADE_DT'
    return dic


