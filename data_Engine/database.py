# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:18:00 2017

@author: sicher
"""
from datetime import datetime, timedelta
from time import time
from WindPy import w
import pandas as pd
import pymongo
import openpyxl
import os
from abc import ABCMeta, abstractmethod
now = datetime.now

class DataBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.info = ''
     
    @abstractmethod
    def insert(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def find(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    
    
class Mongodb(DataBase):
    def __init__(self,host='localhost',port=27017,dbname='a'):
        client = pymongo.MongoClient(host, port)
        self.db = client[dbname]
     
    def insert(self,df,clname):
        clnames = clname.split(',')
        cl = self.db[name]
        if type(df) == pd.core.frame.DataFrame:
            data = df.to_dict(orient='records')
            cl.insert_many(data)
            print ("成功下载合约{}的BAR数据".format(clname))
            
    def update(self,df,clname):
        '''
        clname  :  str or list
        df   :   dataframe or list
        '''
        clnames = clname.split(',')
        start = time()
        for i in range(len(clnames)):
            name = clnames[i]
            cl = self.db[name]
            if type(df) == pd.core.frame.DataFrame:
                data = df.reset_index().to_dict(orient='records')
                flt = pd.DataFrame(df.index).to_dict(orient='records')
                [cl.update_one(data[i],{'$set':flt[i]},upsert=True) for i in range(len(flt))]
                print ("成功下载合约{}的BAR数据,用时{}".format(clname,time()-start))
            if type(df) == list:
                data = df[i].reset_index().to_dict(orient='records')
                flt = pd.DataFrame(df[i].index).to_dict(orient='records')
                print (flt)
                [cl.update_one(flt[i],{'$set':data[i]},upsert=True) for i in range(len(flt))]
                print ("成功下载合约{}的BAR数据,用时{}".format(clname,time()-start))

    def find(self,prop):
        '''
        symbol : str or list
        start_time : datetime.datetime 
        end_time : datetime.datetime
        fields : list
        '''
        symbol = prop['symbol']
        start_time = prop['start_time']
        end_time = prop['end_time']
        fields = prop['fields']
        
        flt={'_id':0,'datetime':1}
        [flt.update({x:1}) for x in fields]
        
        def func(symbol):
            cs = self.db[symbol].find({'datetime':{'$gt':start_time,'$lt':end_time}},flt)
            data = pd.DataFrame(list(cs))
            data.columns
            data['symbol'] = symbol
            return data
        
        if type(symbol) == str:
            data = pd.DataFrame(list(self.db[symbol].find({'datetime':{'$gt':start_time,'$lt':end_time}},flt)))
        if type(symbol) == list:
            data = pd.concat([func(x) for x in symbol],axis=1)
        return data
        
    def delete(self):
        pass
    
    def get_db_info(self):
        _info = {}
        coll_names = self.db.list_collection_names()
        for clname in coll_names:
            info = {}
            first = self.db[clname].find_one(sort=[('datetime',pymongo.ASCENDING)])
            last = self.db[clname].find_one(sort=[('datetime',pymongo.DESCENDING)])
            
            info['legth'] = self.db['000001.XSHE'].count()
            info['fields'] = list(first.keys())
            info['first_date'] = first['datetime']
            info['last_date'] = last['datetime']
            _info[clname] = info
        return pd.DataFrame.from_dict(_info,orient='index')

class Excel(DataBase):
    def __init__(self,root,dir_name):
        self.root = root
        self.dir_name = dir_name
     
    def path(self,doc_name):
        if not os.path.exists(self.root + '\\' + self.dir_name):
            os.mkdir(self.root + '\\' + self.dir_name)
        return self.root + '\\' + self.dir_name + '\\' + doc_name + '.xlsx' 
        
    def insert(self,df,names):
        if type(names) == str:
            names = names.split(',')
        for i in range(len(names)):
            path = self.path(names[i])
            df[i].to_excel(path)
            print ('{}.xlsx已写完'.format(names[i]))

    def update(self,df,names):
        '''
        input :
            A DataFrame 
        '''
        if type(names) == str:
            names = names.split(',')
        for i in range(len(names)):
            path = self.path(names[i])
            
            wb = load_workbook(path)
            ws = wb['Sheet1']
            
            [ws.append(r) for r in dataframe_to_rows(df[i], index=True, header=False)]
            wb.save(path)    
        
        print ('{}.xlsx数据更新完成'.format(doc_name))

    def find(self,prop):
        symbols = prop['symbol'].split(',')
        fields = prop['fields'].split(',')
        start_date = prop['start_date']
        end_date = prop['end_date']
        
        data = []
        for s in symbols:   
            doc_name = self.root + '\\' + self.dir_name + '\\' + s +'.xlsx'
            dt = pd.read_excel(doc_name).set_index('trade_date')
            data.append(dt.loc[start_date:end_date,fields])
        return pd.concat(data)
        
    def delete(self):
        pass 
    
class Hdf5(DataBase):
    def __init__(self,root = r'C:\Users\xinger\Desktop'):
        self.root = root
     
    def insert(self,df,doc_name = 'data.hd5'):
        _dir = self.root + '\\' + doc_name
        data = dataformat(df,_format = 'jaqs')
        f = pd.HDFStore(_dir,'w')
        f['data_d'] = data
        f.close()

    def update(self):
        pass

    def find(self,doc_name):
        _dir = self.root + '\\' + doc_name
        f = pd.HDFStore(_dir,'r')

        data = f['data_d']
        f.close()
        return data
        
    def delete(self):
        pass
