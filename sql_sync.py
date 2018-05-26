# -*- coding: utf-8 -*-
"""
Created on Thu May 10 18:23:02 2018

@author: xinger
"""

class sql_sync(local_pkg): 
    def __init__(self,fp,dv_props,ds_props):     
        super(_sql, self).__init__(fp,dv_props,ds_props)
        import sqlite3 as sql
        path = self.fp + '//' + 'data.sqlite'
        self.conn = sql.connect(path)
        
    def get_date(self,):
        cs = self.conn.cursor()
        cs.execute('select update_date from "update_log"')
        date = cs.fetchall()[0]
        if date:
            start_date = date
            end_date = int(datetime.strftime(datetime.now(),'%Y%m%d'))
            
        return start_date,end_date
            
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
                
                cs = self.client[dbname][clname].find({"report_date":{"$gte":pos1,"$lte":pos2}},{"_id":0})
                data = pd.DataFrame(list(cs))
                data.to_sql(name ,self.conn ,if_exists='append',index=False) 
                self.conn.commit()
                
            else:
                cs = self.client[dbname][clname].find({"report_date":{"$gte":pos1,"$lte":end_date}},{"_id":0})
                data = pd.DataFrame(list(cs))
                data = data.sort_values(['symbol','report_date'])
                data.to_sql(name ,self.conn ,if_exists='append',index=False) 
                self.conn.commit()
                return

    def update_data_jz(self,names):
        names = ['lb.cashFlow','lb.income','lb.balanceSheet','lb.finIndicator','lb.indexCons',
         'jz.secTradeCal','lb.secIndustry','jz.apiParam','lb.profitExpress',
         'lb.secDividend','lb.indexWeightRange','jz.instrumentInfo']
        
        start_date ,end_date = self.get_date()
        
        for name in names:
            cs = ''
            print (name ,'start')
            #name = 'lb.indexCons'
            dbname,clname = name.split('.')
            fields = list(self.client[dbname][clname].find_one().keys())
            
            if name in ['lb.cashFlow','lb.balanceSheet','lb.income']:
                self.distributed_update(name,start_date,end_date)
            
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
                
            data.to_sql(name ,self.conn ,if_exists='append',index=False) 
            print (name , 'OK!')
        
            c= self.conn.cursor()
            c.excute('''INSERT INTO "update_log" values ('update_date':%s)'''%end_date)
            self.conn.commit()