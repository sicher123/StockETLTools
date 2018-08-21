import h5py
import pandas as pd

def get_local(fp,field):
    path = fp + '//%s.hd5'%(field)
    with h5py.File(path) as file:
        index = file['date_flag'][:,0].astype(int)
        columns = file['symbol_flag'][:,0].astype(str)
        data = pd.DataFrame(index = index,columns=columns,data = file['data'][:,:])
        data = data.drop_duplicates()
        #data = data.stack().reset_index()
        #data.columns = ['trade_date', 'symbol', field]
        return data

fp = r'C:\Users\xinger\Desktop\data2\dbo.dbo.ASHAREEODPRICES'
adj = get_local(fp,'S_DQ_ADJFACTOR')
def cal_adj(field,adj_field):
    d1 = get_local(fp, field)
    d2 = get_local(fp, adj_field).stack().reset_index()
    d2.columns = ['d', 's', adj_field]
    d1 = (d1*adj).stack().reset_index()
    d1.columns = ['d', 's', field]
    data = pd.merge(d1, d2,  on=['s', 'd'])
    data['divide'] = data[field]/data[adj_field]

    describe = data['divide'].describe()
    describe.name = field
    return data, describe

import openpyxl

field = 'S_DQ_OPEN'
adj_field = 'S_DQ_ADJOPEN'
open,open_d = cal_adj(field,adj_field)

field = 'S_DQ_CLOSE'
adj_field = 'S_DQ_ADJCLOSE'
close, close_d = cal_adj(field, adj_field)


field = 'S_DQ_HIGH'
adj_field = 'S_DQ_ADJHIGH'
high, high_d = cal_adj(field, adj_field)

field = 'S_DQ_LOW'
adj_field = 'S_DQ_ADJLOW'
low, low_d = cal_adj(field, adj_field)

import sqlite3
conn = sqlite3.connect(r'C:\Users\xinger\Desktop\data\adj.sqlite')
data = pd.read_sql('select * from data1', conn)

dsc = pd.concat([open_d,close_d,high_d,low_d,d],axis=1)
dsc.to_excel(r'C:\Users\xinger\Desktop\adj_compare.xlsx')