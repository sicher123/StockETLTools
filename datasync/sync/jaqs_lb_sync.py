# -*- coding: utf-8 -*-
"""
Created on Thu May 10 18:23:02 2018

@author: xinger
"""
import os
import math
import pymongo
import pandas as pd
from datetime import datetime, timedelta
from jaqs.data.dataview import DataView
import warnings

warnings.filterwarnings("ignore")
today = int(datetime.strftime(datetime.today(),'%Y%m%d'))

fp = r'C:\Users\xinger\Sync\data'


class data_sync(DataView):
    def __init__(self, fp, dv_props, ds_props):
        super(data_sync, self).__init__()
        ds = self.set_data_api('jaqs', ds_props)
        self.fp = fp
        self.init_from_config(dv_props, data_api=ds)
        self.symbol = self.all_symbol
        self.client = pymongo.MongoClient('192.168.0.102',27017)

    def get_field(self, api):
        data, msg = self.data_api.query(view="help.apiParam",
                                        fields="param",
                                        filter="api=%s" % (api),
                                        data_format='list')

        data = list(set(data))
        return data

    def set_data_api(self, origin, ds_props):
        if origin == 'jaqs':
            from jaqs.data.dataservice import RemoteDataService
            ds = RemoteDataService()
            ds.init_from_config(ds_props)
            return ds

    @property
    def all_symbol(self, dtype='list'):
        symbol = self.data_api.query_index_member('000001.SH', self.extended_start_date_d,
                                                  self.end_date) + self.data_api.query_index_member('399106.SZ',
                                                                                                    self.extended_start_date_d,
                                                                                                    self.end_date)
        symbol = [i for i in symbol if i[0] != '2' and i[0] != '9']

        df, msg = self.data_api.query(view="jz.instrumentInfo",
                                      fields="symbol",
                                      filter="market=SZ&market=SH&inst_type=100",
                                      data_format='pandas')
        index = list(df['symbol'])
        symbol.extend(index)

        if dtype == 'list':
            return symbol

        elif dtype == 'str':
            return ",".join(symbol)

    @property
    def index(self):
        df, msg = self.data_api.query(view="jz.instrumentInfo",
                                      fields="symbol",
                                      filter="market=SZ&market=SH&inst_type=100",
                                      data_format='pandas')
        return list(df['symbol'])

    def n_dates(self, start_date, end_date=None):
        if not end_date:
            end_date = today
        return self.data_api.query_trade_dates(start_date, end_date)



class sql_sync(data_sync):
    def __init__(self,fp,dv_props,ds_props):
        import sqlite3 as sql
        path = fp + '//' + 'data.sqlite'
        self.conn = sql.connect(path)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE log(
                    ID INT PRIMARY KEY  NOT NULL,
                    updated_date   int  NOT NULL);''')
        super(sql_sync, self).__init__(fp,dv_props,ds_props)
        
    def get_date(self,):
        cs = self.conn.cursor()
        try:
            start_date = cs.fetchall()[0]
        except:
            start_date = self.dates[0]

        end_date = int(datetime.strftime(datetime.now(),'%Y%m%d'))
            
        return int(start_date),int(end_date)
            
    def distributed_update(self, name, start_date,end_date):
        '''
        update data_d by years
        '''
        start_date ,end_date = self.get_date()
    
        dbname,clname = name.split('.')
        for i in range(20):
            pos1, pos2 = start_date + 10000*i,start_date + 10000*(i+1)
            if pos2 < end_date:
                print(name,pos2)
                
                cs = self.client[dbname][clname].find({"report_date":{"$gte":int(pos1),"$lte":int(pos2)}},{"_id":0})
                data = pd.DataFrame(list(cs))
                data.to_sql(name ,self.conn ,if_exists='append',index=False) 
                self.conn.commit()
                
            else:
                cs = self.client[dbname][clname].find({"report_date":{"$gte":int(pos1),"$lte":int(end_date)}},{"_id":0})
                data = pd.DataFrame(list(cs))
                data = data.sort_values(['symbol','report_date'])
                data.to_sql(name ,self.conn ,if_exists='append',index=False) 
                self.conn.commit()
                return

    def update_data(self):
        names = ['lb.cashFlow','lb.income','lb.balanceSheet','lb.finIndicator','lb.indexCons',
                 'jz.secTradeCal','lb.secIndustry','jz.apiParam','lb.profitExpress',
                 'lb.secDividend','lb.indexWeightRange','jz.instrumentInfo']

        start_date ,end_date = self.get_date()
        
        for name in names:
            cs = ''
            print (name, 'start')
            #name = 'lb.indexCons'
            dbname, clname = name.split('.')
            fields = list(self.client[dbname][clname].find_one().keys())
            
            if name in ['lb.cashFlow', 'lb.balanceSheet', 'lb.income']:
                self.distributed_update(name, start_date, end_date)
            
            elif 'report_date' in fields:
                if type(self.client[dbname][clname].find_one()['report_date']) == str:
                    cs = self.client[dbname][clname].find({'report_date':{"$gte":str(start_date),"$lte":str(end_date+1)}},{'_id':0})
                else:
                    cs = self.client[dbname][clname].find({'report_date':{"$gte":start_date,"$lte":end_date+1}},{'_id':0})

            elif 'trade_date' in fields:
                if type(self.client[dbname][clname].find_one()['trade_date']) == str:
                    cs = self.client[dbname][clname].find({'trade_date': {"$gte":str(start_date),"$lte":str(end_date+1)}}, {'_id':0})
                else:
                    cs = self.client[dbname][clname].find({'trade_date': {"$gte": start_date,"$lte":end_date+1}}, {'_id':0})

            else:
                cs = self.client[dbname][clname].find({}, {'_id': 0})

            data = pd.DataFrame(list(cs)) 
                
            if name == 'jz.apiParam':
                data = data[~data['api'].isin(['lb.windFinance'])]
                name = 'help.apiParam'
                
            if name == 'lb.indexCons':
                symbols = [i for i in data['symbol'] if (i[0] == '2' or i[0] == '9')]
                data = data[~data['symbol'].isin(symbols)]
                data['index_code'][data['index_code'] == '399300.SZ'] = '000300.SH'
                
            data.to_sql(name, self.conn, if_exists='append', index=False)
            print(name, 'OK!')
        
            #c= self.conn.cursor()
            #c.execute('''INSERT INTO "log" values ('updated_date':%s)''' % int(end_date))
            #self.conn.commit()


def update_lb_data(start_date=20080101, end_date=today):
    addr = 'tcp://192.168.0.102:23000'
    # addr="tcp://data.tushare.org:8910"
    name = "13243828068"
    passwd = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MTUwNDk5MzI2MDAiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTMyNDM4MjgwNjgifQ.KpmnMkuO7ApTWvBAwgvHwWDkmoasBIdQHl2gQJVmqIA'

    ds_props = {'remote.data.address': addr,
                'remote.data.username': name,
                'remote.data.password': passwd}

    symbol = '600000.SH,000002.SZ'
    _fields = ['close']
    dv_props = {'start_date': start_date, 'end_date': end_date, 'symbol': symbol, 'fields': ','.join(_fields),
                'freq': 1}
    fp = r'C:\Users\xinger\Desktop\data1'
    sync = sql_sync(fp, dv_props, ds_props)
    sync.update_data()
