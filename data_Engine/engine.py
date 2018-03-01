# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 09:45:44 2018

@author: sicher
"""



prop = {'start_date': 20170520,
        'end_date': 20170601,
        'symbol':symbol ,
        'fields': 'open,close,high,low,volume',
        'self.dtype':'list',
        'freq':'1M'}


conf = {}
# wind or jaqs
conf['origin'] = 'wind'
#mongodb excel hdf5
conf['database'] = 'mongodb'
#['basic','daily','minu','finance']
conf['data_type'] = 'daily'
conf['prop'] = prop

data = do.getdailydata(prop)

db.update(data,symbols)
    
db.insert(data,symbols)
db.find()

db.find(prop)

#完全封装版
class data_engine(object):
    def __init__(self,conf):
        origin = conf['origin']
        database = conf['database']
        dbname = origin + '_' + conf['dtype'] + '_data'
        self.dtype = conf['dtype']
        #['basic','daily','minu','finance']
        self.prop = conf['prop']
        index = ['all','SZ50','HS300','ZZ500','SME','GEM']
        
        if origin == 'wind':
            self.do = WindData()
        elif origin == 'jaqs':
            self.do = JaqsData()
            
        if database == 'mongodb':
            self.db = Mongodb(dbname = dbname)
        elif database == 'excel':
            self.db = Excel(dbname = dbname)
        
    def update(self):
        if self.dtype == 'daily':
            df = self.do.get_daily_data(self.prop)
            self.db.update(df,self.prop['symbol'])
        if self.dtype == 'min':
            df = self.do.get_daily_data(self.prop)
            self.db.update(df,self.prop['symbol'])
        if self.dtype == 'finance':
            df = self.do.get_finance_data(self.prop)
            self.db.update(df,prop['fnc_clname'])
        
    def insert(self):
        if self.dtype == 'daily':   
            df = self.do.get_daily_data(self.prop)
            self.db.insert(df,self.prop['symbol'])
        if self.dtype == 'min':
            df = self.do.get_daily_data(self.prop)
            self.db.insert(df,self.prop['symbol'])
        if self.dtype == 'finance':
            df = self.do.get_finance_data(self.prop)
            self.db.insert(df,prop['fnc_clname'])
        
    def find(self):
        self.db.find(self.prop)
        
    def delete(self):
        pass
    
        