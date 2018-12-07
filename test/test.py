# -*- coding: utf-8 -*-

fp = r'D:\sqlite_data'

import sqlite3
from datasync.utils import trans_symbol
from datetime import datetime
from time import time
import os
import pandas as pd
from datasync.data_origin.sql_origin import OracleOrigin

conn = sqlite3.connect(r'D:\sqlite_data\ZYYXData.sqlite')
conn2 = sqlite3.connect(r'D:\sqlite_data\ZYYXData2.sqlite')

db_config = {'addr': "172.16.55.54:1521/ORCL",
             'user': "bigfish",
             'password': "bigfish"}


origin = OracleOrigin(db_config)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

start = time()
sql = 'select * from ZYYX2.CON_FORECAST_STK'
data = origin.read(sql=sql)
data['STOCK_CODE'] = trans_symbol(list(data['STOCK_CODE'].values))
data['CON_DATE'] = data['CON_DATE'].apply(lambda x:datetime.strftime(x.to_datetime(),'%Y%m%d') if x != pd.NaT else None)
print (time() - start)

for field in ['CON_OR_HISDATE','CON_NP_HISDATE','CON_EPS_HISDATE','ENTRYTIME','UPDATETIME']:
    print (field)