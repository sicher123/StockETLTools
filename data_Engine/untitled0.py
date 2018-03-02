# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 09:17:59 2018

@author: xinger
"""

import h5py

file = r'E:\Factor\data.hd5'
h = h5py.File(file)

[key for key in h5.keys()]
h5.close()
di = h5['data_inst']
dd = h5['data_d']

for name in h5:
    print (name)
    
#name

#group
    
#type 
Dataset



name : group 
_type  :Dataset

import pandas as pd

file = r'C:\Users\xinger\Desktop\test.hd5'
h5 = pd.HDFStore(file,'r')
h5.select('data',where = ['0','open'])

nrows = h5.get_storer('data').nrows

h5.select('data',where=['open>2'])

h5.select('data',w)



