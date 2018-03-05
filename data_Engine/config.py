# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:43:09 2018

@author: xinger
"""

import sys
#sys.path.append(r'C:\Users\siche\Desktop\git\data_service\data_Engine')

prop = {'start_date': 20170520,
        'end_date': 20170601,
        'symbol':'ALL' ,
        'fields': 'open,close,high,low,volume',
        'dtype':'list',
        'freq':'1M'}



conf = {}
# wind or jaqs
conf['origin'] = 'wind'
#mongodb excel hdf5
conf['database'] = 'excel'
#['basic','daily','minu','finance']
conf['data_form'] = 'daily'
conf['prop'] = prop
conf['dtype'] = 'daily'
conf['root'] = r'C:\Users\siche\Desktop\ext'
'''
data = do.getdailydata(prop)
db.update(data,symbols)    
db.insert(data,symbols)
db.find(prop)
'''
from engine import data_engine

de = data_engine(conf)
de.insert()
