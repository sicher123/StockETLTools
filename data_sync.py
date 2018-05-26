# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
#import re
from time import time
import os
import h5py
import math
import pymongo
import numpy as np
import pandas as pd 
from copy import copy
from datetime import datetime,timedelta
from jaqs.data.dataview import DataView
import warnings
warnings.filterwarnings("ignore")
from datadesk.utils import trans_symbol

class data_sync(DataView):
    def __init__(self, fp,dv_props,ds_props):     
        super(data_sync, self).__init__()
        ds = self.set_data_api('jaqs',ds_props)
        self.fp = fp
        self.init_from_config(dv_props, data_api=ds)
        self.symbol = self.all_symbol
        self.indi_field = dv_props['indi_field']
        self.daily_field = dv_props['daily_field']
        self.adj_field = dv_props['adj_field']
        self.factors = dv_props['factors']
        self.client = pymongo.MongoClient('192.168.0.102',27017)
        global today
        today = int(datetime.strftime(datetime.today(),'%Y%m%d'))        
        #self.conn = self.connect(data_source)
        
    def set_data_api(self,origin,ds_props):
        if origin == 'mongodb':
            from dataservice import MongoDataService
            ds =  MongoDataService()
            ds.init_from_config(ds_props)
            return ds
            
        elif origin == 'jaqs':
            from jaqs.data.dataservice import RemoteDataService
            ds =  RemoteDataService()
            ds.init_from_config(ds_props)
            return ds
        
        elif origin == 'sqlserver':
            from dataservice import MSSqlDataService
            ds =  MSSqlDataService()
            ds.init_from_config(ds_props)
            return ds
        
        elif origin == 'oracle':
            from dataservice import OracleDataService
            ds =  OracleDataService()
            ds.init_from_config(ds_props)
            return ds

    @property
    def all_symbol(self,dtype = 'list'):
        symbol = self.data_api.query_index_member('000001.SH',self.extended_start_date_d,self.end_date) + self.data_api.query_index_member('399106.SZ',self.extended_start_date_d,self.end_date)
        symbol = [i for i in symbol if i[0] != '2' and i[0] != '9']
        
        if dtype == 'list':
            return symbol
            
        elif dtype == 'str':
            return ",".join(symbol)

    @property
    def index(self):
        cs = self.client['lb']['indexCons'].find({},{'_id':0,'index_code':1})
        return set([i['index_code'] for i in cs])

    def n_dates(self, start_date, end_date = None):
        if not end_date:
           end_date = today
        return self.data_api.query_trade_dates(start_date, end_date)
    
    def normalize(self,df):
        for symbol in set(self.symbol) - set(df.columns):
            df[symbol] = np.nan
            
        return df.loc[self.dates,self.symbol]
    
    
class hdf5_sync(data_sync):
    def __init__(self,fp ,props ,ds_props):     
        super(hdf5_sync, self).__init__(fp,props,ds_props)     
        self.all_fields = self.daily_field + self.indi_field + self.factors + self.adj_field
        self.daily_folder_name = 'daily'
        self.daily_path = fp + '//' + self.daily_folder_name
        
        if not os.path.exists(fp):
            os.mkdir(fp)
        
        if self.daily_folder_name not in os.listdir(fp):
            os.mkdir(self.daily_path)    
        
    @staticmethod
    def _convert_string_array(dt, encoding, itemsize=None):
        from pandas._libs import lib
        from pandas.core.dtypes.common import _ensure_object 
        
        if dt.dtype.name == 'object':
            # encode if needed
            if encoding is not None and len(dt):
                dt = pd.Series(dt.ravel()).str.encode(encoding).values.reshape(dt.shape)
        
            # create the sized dtype
            if itemsize is None:
                itemsize = lib.max_len_string_array(_ensure_object(dt.ravel()))
        
            dt = np.asarray(dt, dtype="S%d" % itemsize)
            return dt
        else:
            return dt

    def get_daily(self, symbol, field, start_date ,end_date,data_format = 'df'):
        if isinstance(field,str):
            field = field.split(',')  
        if isinstance(symbol,list):
            symbol= ','.join(symbol)
            
        daily_fld = ','.join([i for i in field if i in self.daily_field])
        factor_fld = ','.join([i for i in field if i in self.factors])
        indi_fld = ','.join([i for i in field if i in self.indi_field])
        adj_fld = ','.join([i for i in field if '_adj' in i])
        dates = self.data_api.query_trade_dates(start_date,end_date)
        _filter = 'symbol={}&start={}&end={}'.format(symbol,start_date,end_date)
   
        #daily
        if daily_fld != '':
            try:
                daily_data , msg = self.data_api.daily(symbol, start_date, end_date, fields = daily_fld, adjust_mode=None)
            except:
                pass
        else:
            daily_data = []
            
        #factor
        if factor_fld != '':
            try:
                factor_data , msg = self.data_api.query('factor',_filter,factor_fld)
            except:
                raise ValueError('factor data not found')
        else:
            factor_data = []
        
        #indi
        if indi_fld != '':
            try:
                indi_data , msg = self.data_api.query_lb_dailyindicator(symbol, start_date, end_date, fields = indi_fld)
            except:
                raise ValueError('indi data not found')
        else:
            indi_data = []
        
        #adjust
        if adj_fld != '':
            try:
                dic = {}
                for i in adj_fld.split(','):
                    dic[i[:-4]] = i
                fld = ','.join(list(dic.keys()))
                
                adjust_data , msg = self.data_api.daily(symbol, start_date, end_date, fld, adjust_mode='post')
                fld = fld.split(',') + ['trade_date','symbol']
                adjust_data = adjust_data.loc[:,fld]              
                adjust_data = adjust_data.rename_axis(dic,axis=1)
            except:
                adjust_data = []
        else:
            adjust_data = []
            
        l = []
        for data in [daily_data, adjust_data,factor_data,indi_data]:
            if len(data) > 0:
                if 'datetime' in data.columns:
                    data = data.rename_axis({'datetime':'trade_date'},axis=1)
                if not isinstance(data['trade_date'][0],int):
                    data['trade_date'] = data['trade_date'].astype(int)
                if len(data['symbol'][0]) != 9:
                    data['symbol'] = [trans_symbol(i) for i in data['symbol'].values]
                l.append(data)
                
        if len(l) > 1:
            from functools import reduce
            data = reduce(lambda x,y:pd.merge(x,y,on=['symbol','trade_date'],how ='outer'),l)
        elif len(l) == 1:
            data = l[0]      
        else:
            return None
        
        data = data[data['trade_date'].isin(dates)]
        
        #if 'trade_status' in data.columns.values:
        #    data['trade_status'][data['trade_status'] == '交易'] = 1.0
        #    data['trade_status'][data['trade_status'] == '停牌'] = 0.0
        
        if data_format == 'df':
            return data
        elif data_format == 'pn':
            return data.set_index(['symbol','trade_date']).to_panel()


    def _distributed_query(self,symbol, field, limit=500, on='symbol'):
        if on == 'symbol':
            num = len(symbol)
            def func(i):
                data = None
                if i*limit < num:
                    pos1, pos2 = int(i*limit),int((i+1)*limit)
                    s = symbol[pos1:pos2]
                    if field == 'adjust_factor':
                        data = self.data_api.query_adj_factor_daily(','.join(s),self.extended_start_date_d,self.end_date)                  
                    else:
                        try:
                            data = self.get_daily(s,field,self.extended_start_date_d,self.end_date)
                        except:
                            self.data_api.init_from_config(dsp)
                            data = self.get_daily(s,field,self.extended_start_date_d,self.end_date)
                    return data
                    
            l = [func(i) for i in range(math.ceil(num/limit))]
            return pd.concat(l)
        

    def update_on_one_dimension(self,df ,fields = None, _symbols = None, date = None):
        '''
        symbol or date
        '''
        data = self._convert_string_array(df.values,None)
        date_flag = pd.DataFrame(df.index.values).values
        symbol_flag = pd.DataFrame(df.columns.values).values
        symbol_flag = self._convert_string_array(symbol_flag,None)
        date_flag = self._convert_string_array(date_flag,None)
        file_names = os.listdir(self.daily_path)
                
        if fields != None and (_symbols == None or date == None):  
            def func(field):
                name = field + '.hd5' 
                _dir = self.daily_path + '\\' + name   
                if name not in file_names:
                    file = h5py.File(_dir)
                    if field not in file.keys():
                        dset = file.create_dataset(field,data = data,chunks=True,maxshape=(8000,8000),compression="gzip")
                        file.create_dataset('symbol_flag',data = symbol_flag,maxshape=(8000,1),chunks=True)
                        file.create_dataset('date_flag',data = date_flag,maxshape=(8000,1),chunks=True)
                        dset.attrs['last_update_date'] = today
                        file.close()
                        print (fields,'ok!')    
                    
            if isinstance(fields,str):
                func(fields)
            if isinstance(fields,list):
                for field in fields:
                    func(field)
            
        if _symbols != None:
            print (_symbols)
            num = len(_symbols)
            
            #with h5py.File(name) as file:
            _dir = self.daily_path + '//' + fields + '.hd5'
            file = h5py.File(_dir) 
            dset = file[fields]
                  
            new_shape = (dset.shape[0],dset.shape[1]+num)
            dset.resize(new_shape)
            dset[:,-num:] = data
            file.attrs['last_update_date'] = today
                
            symbol_dset = file['symbol_flag']
            new_shape = (symbol_dset.shape[0]+num,symbol_dset.shape[1])
            symbol_dset.resize(new_shape)
            symbol_dset[-num:,:] = symbol_flag

            print (fields,'{} data have been updated'.format(_symbols))
                
            
        if date != None:
            num = len(date)   
            
            _dir = self.daily_path + '//' + fields + '.hd5'
            file = h5py.File(_dir) 
            dset = file[fields]
                  
            new_shape = (dset.shape[0]+num,dset.shape[1])
            dset.resize(new_shape)
            dset[-num:,:] = data
            file.attrs['last_update_date'] = today
                
            date_dset = file['date_flag']
            new_shape = (date_dset.shape[0]+num,date_dset.shape[1])
            date_dset.resize(new_shape)
            date_dset[-num:,:] = date_flag
            file.close()

            print (fields,'data has been updated  from {} to {}'.format(date[0],date[-1]))

    def create_daily(self):
        #daily
        
        symbol = self.symbol
        index_symbol = copy(symbol)
        index_symbol.extend(self.index)
        
        start = time()
        df = self._distributed_query(index_symbol,self.daily_field+self.adj_field,limit=300)
        print ('daily_field',time() - start)

        for i in df.columns.values:
            data = df.pivot(index = 'trade_date',columns='symbol',values = i)
            data = data.loc[:,index_symbol]
            self.update_on_one_dimension(data,fields = i)
            
        #adj_factor = self._distributed_query(symbol,'adjust_factor')
        adj_factor = self.data_api.query_adj_factor_daily(','.join(symbol),self.extended_start_date_d,self.end_date)
        data = adj_factor.loc[:,symbol]
        self.update_on_one_dimension(data,fields = 'adjust_factor')
            
        fields = copy(self.indi_field)
        fields.extend(self.factors)
        fields = set(fields)
        for f in fields:            
            start = time()  
            data = self._distributed_query(symbol,f,limit=1000)
            print (time() - start)
            data = data.pivot(index = 'trade_date',columns='symbol',values = f)
            data = data.loc[:,symbol]
            if f in ['pb','pe','ps']:
                f += '_'
            self.update_on_one_dimension(data,fields = f)

    def update_daily(self,):
        all_field = self.all_fields
        all_dates = self.data_api.query_trade_dates(self.extended_start_date_d,today) 
        all_symbol = self.symbol
        index_symbol = copy(self.symbol)
        index_symbol.extend(self.index)
    
        file_names = os.listdir(self.daily_path)
        exist_field = [i[:-4] for i in file_names]
        fields = list(set(all_field) - set(exist_field))
        fields = list(set(fields)- set(['pe','pb','ps']))
        
        if len(fields) > 0:
            for f in fields:
                if f in self.daily_field:
                    data = self._distributed_query(all_symbol,f,limit=300)
                else:
                    data = self._distributed_query(index_symbol,f,limit=300)
                    
                data = data.pivot(index = 'trade_date',columns='symbol',values = f)
                self.update_on_one_dimension(data,fields = f)
            
        for name in set(file_names):
            field = name[:-4]
            _dir = self.daily_path + '//' + name
            file = h5py.File(_dir)
            
            if field in ['_pb','_pe','_ps']:
                field = field[1:]

            exist_symbol = list(file['symbol_flag'][:,0].astype(str))
            exist_dates = file['date_flag'][:,0].astype(int)
            
            symbol = list(set(all_symbol) - set(exist_symbol))
            dates = list(set(all_dates) - set(exist_dates))
            symbol.sort()
            dates.sort()
                    
            if len(symbol) > 0:
                data = self.get_daily(symbol,field,exist_dates[0],exist_dates[-1])
                if data is not None:
                    data = data.pivot(index = 'trade_date',columns='symbol',values = field)
                    data = data.loc[symbol,exist_dates]
                    self.update_on_one_dimension(data,fields = field,symbol = symbol)
                    exist_symbol = exist_symbol + symbol
                else:
                    print (field,'No data')
                
            if len(dates) > 0:
                data = self.get_daily(exist_symbol,field,dates[0],dates[-1])
                if data is not None:
                    data = data.pivot(index = 'trade_date',columns='symbol',values = field)
                    data = data.loc[dates,exist_symbol]
                    self.update_on_one_dimension(data,fields = field,date = dates)
                else:
                    print (field,'No data')

class sql_sync(data_sync): 
    def __init__(self,fp,dv_props,ds_props):     
        super(sql_sync, self).__init__(fp,dv_props,ds_props)
        import sqlite3 as sql
        self.client = pymongo.MongoClient('192.168.0.102',27017)
        path = self.fp + '//' + 'data.sqlite'
        self.conn = sql.connect(path)
        
    def _get_date(self,name):
        c = self.conn.cursor()
        try :
            c.execute('''select max(trade_date) from "%s"'''%(name))  
            date = c.fetchall()[0][0]
        except:
            
            try:
                c.execute('''select max(report_date) from "%s"'''%(name))
                date = c.fetchall()[0][0]
            except:
                date = None
            
        if date:
            start_date = int(date)
            end_date = int(datetime.strftime(datetime.now(),'%Y%m%d'))
        else:
            start_date = self.extended_start_date_q
            end_date = int(datetime.strftime(datetime.now(),'%Y%m%d'))
            
        return start_date,end_date
            
    def distributed_update(self, name, start_date,end_date):
        '''
        update data_d by years
        '''
        if name == 'lb.indexWeightRange':
            DATE_NAME = 'trade_date'
        else:
            DATE_NAME = 'report_date'
        
        print(name,start_date,end_date)
        
        dbname,clname = name.split('.')
        for i in range(math.ceil((end_date - start_date)/10000)):
            pos1, pos2 = int(start_date + i*10000),int(start_date + (i+1)*10000)
            if pos2 < end_date:
            
                cs = self.client[dbname][clname].find({DATE_NAME:{"$gte":str(pos1),"$lte":str(pos2)}},{"_id":0})
                data = pd.DataFrame(list(cs))
                if len(data) > 0:
                    data.to_sql(name ,self.conn ,if_exists='append',index=False) 
                    self.conn.commit()
                
            else:
                cs = self.client[dbname][clname].find({DATE_NAME:{"$gte":str(pos1),"$lte":str(end_date)}},{"_id":0})
                    
                data = pd.DataFrame(list(cs))
                if len(data) > 0:
                    data = data.sort_values(['symbol',DATE_NAME])
                    data.to_sql(name ,self.conn ,if_exists='append',index=False) 
                    self.conn.commit()
                    return

    def update_data(self):
        names = ['lb.cashFlow','lb.income','lb.balanceSheet','lb.finIndicator','lb.indexCons',
         'jz.secTradeCal','lb.secIndustry','jz.apiParam','lb.profitExpress',
         'lb.secDividend','lb.indexWeightRange','jz.instrumentInfo']
        
        
        for name in names:
            cs = ''
            print (name ,'start')
            #name = 'lb.indexCons'
            dbname,clname = name.split('.')
            start_date ,end_date = self._get_date(name)
            fields = list(self.client[dbname][clname].find_one().keys())
            
            if name in ['lb.cashFlow','lb.balanceSheet','lb.income','lb.finIndicator','lb.indexWeightRange']:
                self.distributed_update(name,start_date,end_date)
                continue
            
            elif 'report_date' in fields:
                if type(self.client[dbname][clname].find_one()['report_date']) == str:
                    cs = self.client[dbname][clname].find({'report_date':{"$gte":str(start_date),"$lte":str(end_date+1)}},{'_id':0})
                else:
                    cs = self.client[dbname][clname].find({'report_date':{"$gte":start_date,"$lte":end_date+1}},{'_id':0})

            elif 'trade_date' in fields:
                if type(self.client[dbname][clname].find_one()['trade_date']) == str:
                    cs = self.client[dbname][clname].find({'trade_date':{"$gte":str(start_date),"$lte":str(end_date+1)}},{'_id':0})
                else:
                    cs = self.client[dbname][clname].find({'trade_date':{"$gte":start_date,"$lte":end_date+1}},{'_id':0})

            else:
                cs = self.client[dbname][clname].find({},{'_id':0})

            data = pd.DataFrame(list(cs)) 
                
            if name == 'jz.apiParam':
                data = data[~data['api'].isin(['lb.windFinance'])]
                name = 'help.apiParam'
                
            if name == 'lb.indexCons':
                symbols = [i for i in data['symbol'] if (i[0] == '2' or i[0] == '9')]
                data = data[~data['symbol'].isin(symbols)]
                data['index_code'][data['index_code'] == '399300.SZ'] = '000300.SH'
                
            if len(data) > 0:
                data.to_sql(name ,self.conn ,if_exists='replace',index=False) 
            print (name , 'OK!')
