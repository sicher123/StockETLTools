import h5py
import os
import pandas as pd

def get_shape(path,name):
    if name.endswith('hd5'):
        with h5py.File(path + '//%s'%(name)) as file:
            keys = list(file.keys())
            try:
                assert keys == ['data', 'symbol_flag', 'date_flag'], (name, keys)
            except Exception as e:
                print(e)
            #dic['symbol_flag'] = file['symbol_flag'].shape
            #dic['date_flag'] = file['date_flag'].shape
            #dic['data'] = file['data'].shape
            try:
                data = pd.DataFrame(index = file['date_flag'][:, -1], columns=file['symbol_flag'][:,-1],data = file['data'][:])
                print (data)
                #print (file['date_flag'][:,-1])
                #data = data.dropna(how = 'all')
                #if len(data) == 0:
                    #logger.error('%s newest data all None'%(name))
            except Exception as e:
                #logger.error('%s newest data all None' % (name))
                print ('error',name,e)
            print(name)
            #dic1[name] = dic
#return pd.DataFrame(dic1)

class h5View():
    def __init__(self, path, name):
        file = h5py.File(path + '//%s' % (name, ))
        self.file = file
        keys = list(file.keys())
        try:
            assert keys == ['data', 'symbol_flag','date_flag'], (name, keys)
        except Exception as e:
            print(e)
        self.symbol_flag = file['symbol_flag']
        self.date_flag = file['date_flag']

    @property
    def data(self):
        data = pd.DataFrame(index=self.file['date_flag'][:, -1], columns=self.file['symbol_flag'][:,-1],data = self.file['data'][:])
        return data

    def __call__(self):
        print (self.file['data'].shape,
               self.file['symbol_flag'].shape,
               self.file['date_flag'].shape)
        return self.file

path = r'C:\Users\xinger\Sync\data\Stock_D'
shape = get_shape(path)

import json

def set_attr(path):
    dic1 = {}
    for name in os.listdir(path):
        if name.endswith('hd5'):
            with h5py.File(path + '//%s'%(name)) as file:
                file.attrs['meta'] = json.dumps({'updated_date': 20180709})
                print(name)

#path = r'D:\data\SecDailyIndicator'
#shape = set_attr(path)
