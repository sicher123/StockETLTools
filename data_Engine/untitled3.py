# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 16:39:08 2018

@author: xinger
"""

prop['symbol'] = '300085.SZ'
prop['start_date'] = '2018-03-08'
prop['end_date'] = '2018-03-08'

data = ww.get_min_data(prop)
data['chg'] = data['close'] - data['open']

data['vol_n'] = data['volume'][data['chg'] < 0]
data['vol_p'] = data['volume'][data['chg'] > 0]
data['vol_m'] = data['volume'][data['chg'] == 0]
data = data.fillna(1)

data['chg'].max()


sum(data['vol_n'])
sum(data['vol_p'])
sum(data['vol_m'])
