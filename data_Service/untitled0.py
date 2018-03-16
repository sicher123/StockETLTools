# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:37:32 2018

@author: xinger
"""

def select(self):
    """
    generate the selection
    """
    if self.condition is not None:
        return self.table.table.readWhere(self.condition.format(), start=self.start, stop=self.stop)
    elif self.coordinates is not None:
        return self.table.table.readCoordinates(self.coordinates)
    return self.table.table.read(start=self.start, stop=self.stop)

import io
import pandas as pd

df = pd.read_csv(io.StringIO("""
sessionID        time
3ODE3Nzll  1467590400
lMGVkMDc4  1467590400
jNzIzNmY1  1467590400
3ODE3Nzll  1467676800
lMGVkMDc4  1467676800
jNzIzNmY1  1467676800
"""), sep='\s+')

filename = r'C:\Users\xinger\Desktop\aaa.h5'

store = pd.HDFStore(filename)

store.append('/aaa/df1', df, data_columns=True)
store.append('/bbb/df1', df, data_columns=True)

# let's double # of rows
df = pd.concat([df] * 2, ignore_index=True)

# and write it to HDFStore
store.append('/aaa/df2', df, data_columns=True)

print(store)

argdate = "2016/07/04"
ts_from = int(pd.to_datetime(argdate).timestamp())
ts_to = ts_from + 24*60*60

client_flt = '/aaa/'
#qry = '(time >= {0}) & (time <= {1})'.format(dayTimestamp, dayTimestamp + 24*60*60)
qry = 'time >= ts_from & time <= ts_to'
print('WHERE:\t%s' %qry)

for k in store:
    if k.startswith(client_flt):
        x = store.select(k, where=qry)
        print(k)
        print(x)