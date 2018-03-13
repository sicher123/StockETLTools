# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:37:32 2018

@author: xinger
"""
from init import *

class DataOrigin(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.data = ''

    def __str__(self):
        return self.data
     
    @abstractmethod
    def get_daily_data(self):
        pass
    
    @abstractmethod
    def get_min_data(self):
        pass

class WindData(DataOrigin):
    def __init__(self,):
        self.data = ''
        self.signinWind()
        
    def signinWind(self):
        """登录wind"""
        self.w = w
        self.w.start()
        if self.w.isconnected():
            print ("WIND API connected successfully")
        else:
            print ("WIND API connected failed")
        
    def get_index_cons(self,sector,dtype = 'list'):
        sectorID = {}
        sectorID['ALL'] = 'a001010100000000'     #u"全部A股"
        sectorID['zxb'] = 'a001010400000000'     #u"中小板"
        sectorID['cyb'] = 'a001010r00000000'    #u"创业板 "
        sectorID['hs300'] = 'a001030201000000'     #u'沪深300'
        sectorID['zz500'] = 'a001030208000000'     #u'中证500'
        
        sector_id = sectorID[sector]
        d = self.w.wset("SectorConstituent", date = str_now, sectorId = sector_id)  
        data = ''
        
        if dtype == 'list':
            data = d.Data[1]
        elif dtype == 'dataframe':
            data = pd.DataFrame(data = d.Data,index = d.Fields).T
        elif dtype == 'str':
            data = ",".join(d.Data[1])
        else:
            print ('dtype must be list or dataframe')
        return data
        
    def get_daily_data(self,prop):
        symbols = prop['symbol']
        start_time = str(prop['start_date'])
        end_time = str(prop['end_date'])
        fields = prop['fields']
        symbols = symbols.split(',')
        
        def func(symbol):
            d = w.wsd(symbol,fields,start_time,end_time,"rptYear=2014，Fill=Previous;PriceAdj=F")
            if d.ErrorCode == 0:
                fld = [f.lower() for f in d.Fields]
                times = [datetime.strftime(x,'%Y%m%d') for x in d.Times]
                data = pd.DataFrame(data = d.Data, index=fld, columns=times).T
                data['symbol'] = symbol
                data.index.name = 'trade_date'
                return data.reset_index()
            else:
                print ('error',d.ErrorCode)
                
        d_list = [func(symbol) for symbol in symbols]
        if prop['dtype'] == 'list':
            return d_list
        if prop['dtype'] == 'dataframe':
            return pd.concat(d_list)
        
    def get_min_data(self,prop):
        '''
        prop : dict   example
                       symbol : '000001.SZ'
                       start_time/end_time : '20170101 09:00:00'
                       fields : 'open,high,low,close'
                       freq : 1                     ( must in 1,3,5,10,15,30,60)
        '''
        symbol = prop['symbol']
        start_date = prop['start_date']
        end_date = prop['end_date']
        fields = prop['fields']
        freq = prop['freq'][:1]
        
        start_time = start_date + " 09:00:00"
        end_time = end_date + " 15:00:00"
        
        d = self.w.wsi(symbol, fields, start_time, end_time, "BarSize={};Fill=Previous;PriceAdj=F".format(freq))
        if d.ErrorCode == 0:
            fields = [f.lower() for f in d.Fields]
            data = pd.DataFrame(data = d.Data,index=fields,columns=d.Times).T.reset_index()
            return data.rename(columns = {'index':'datetime'})
        else:
            print ('error',d.ErrorCode)
 
class JaqsData(DataOrigin):
    def __init__(self):
        name = "13243828068"
        passwd = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MTUwNDk5MzI2MDAiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTMyNDM4MjgwNjgifQ.KpmnMkuO7ApTWvBAwgvHwWDkmoasBIdQHl2gQJVmqIA'
        self.api = DataApi(addr="tcp://data.tushare.org:8910")
        self.api.login(name, passwd)
     
 #------------------------------------------------------------------------
    def get_basic_data(self,dtype = 'dataframe'):
        df, msg = self.api.query(
            view="jz.instrumentInfo",
            fields="status,list_date, fullname_en, market",
            filter="inst_type=1&status=1&symbol=",
            data_format='pandas')
        if msg == '0,':
            data = df[~df['market'].isin(['HKH','HKS','JZ'])]
            if dtype == 'dataframe':
                return data
            if dtype == 'list':
                return list(data['symbol'])
        else:
            print ('error',msg)
            
    def get_index_cons(self,index):
        if index =='ALL':
            return self.get_basic_data(dtype='list')
        else:
            df, msg = self.api.query(
                  view="lb.indexCons",
                  fields="",
                  filter="index_code={}&start_date={}&end_date={}".format(index,str_now,str_now),
                  data_format='pandas')
            retrun
    #------------------------------------------------------------------------
    def get_date_data(self,prop,dtype = 'list'):
        start_date = prop['start_date']
        end_date = prop['end_date']
        df, msg = self.api.query(
                    view="jz.secTradeCal",
                    fields="date,istradeday,isweekday,isholiday",
                    filter="start_date={}&end_date={}".format(start_date,end_date),
                    data_format='pandas')
        if msg == '0,':
            df['trade_date'] = df['trade_date'].astype('str')
            if dtype == 'dataframe':
                return df
            elif  dtype == 'list':
                trade_date = df["trade_date"][df.istradeday == "T"]
                return list(trade_date)
        else:
            print ('error',msg)
            
    #------------------------------------------------------------------------
    def get_daily_data(self,prop):
        
        symbols = prop['symbol']
        start_date = prop['start_date']
        end_date = prop['end_date']
        fields = prop['fields']
        df, msg = self.api.daily(symbol = symbols,start_date = start_date, end_date = end_date,fields = fields,adjust_mode="post")
    
        if msg == '0,':
            #data = data.drop(['symbol','date'],axis =1)
            return df
        else:
            print ('error',msg)
            
    #------------------------------------------------------------------------      
    def get_min_data(self,prop):
        symbol = prop['symbol']
        fields = prop['fields']
        freq = prop['freq']
        
        assert freq in ("15S", "30S", "1M", "5M", "15M", "1D", "1W",'1m'), "请输入正确的分钟级别参数"

        trade_dates = self.get_date_data(prop,dtype = 'list')
        df = pd.concat([self.api.bar(symbol = symbol,trade_date = date,freq = freq,start_time=90000,end_time=150000,fields="")[0] for date in trade_dates])
        return df
        
    def get_lb_data(self,prop):
        prop['view']
        prop['fields']
        prop['filter']
        prop['data_format']
        
        df, msg = self.api.query(
                view = view,
                fields = fields,
                filter = flt,
                data_format = dfm)

        if msg == '0,':
            return df
        else:
            print (msg)
            



'''
prop : dict
origin  :  wind,jaqs
start_date/end_date  :  str ,example 20180101
symbol(or  index) : str ,example '000001.SZ' ; index must in SZ50,HS300,ZZ500,SME,GEM
field  :  str ,example 'open,high...'
freq   :  1D 1M 5M 10M 30M 60M
dataformat  :    
'''


'''
prop = {'start_date': 20170520, 'end_date': 20170601,'symbol':'000001.SZ' ,
   'fields': 'open,close,high,low,volume','dtype':'list','freq':'1M'}

ww = WindData()


m_prop = {'start_time': '20171201 09:00:00', 'end_time': '20180101 09:00:00', 'symbol':'000001.SZ' ,
   'fields': 'open,close,high,low,volume',}

js = JaqsData()
'''
