# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 16:39:08 2018

@author: xinger
"""

prop['symbol'] = '300085.SZ'
prop['start_date'] = '2018-03-08'
prop['end_date'] = '2018-03-09'

data = ww.get_min_data(prop)
data['pct_chg'] = (data['close'] - data['open'])/data['open']

data['vol_n'] = data['volume'][data['chg'] < 0]
data['vol_p'] = data['volume'][data['chg'] > 0]
data['vol_m'] = data['volume'][data['chg'] == 0]
data = data.fillna(0)

data['chg'].max()


sum(data['vol_n'])
sum(data['vol_p'])
sum(data['vol_m'])


from datetime import timedelta
all_symbol = ww.get_index_cons('ALL')
all_symbol = ",".join(all_symbol)



prop['symbol'] = all_symbol
prop['start_date'] = datetime.strftime(now - timedelta(days=1),'%Y-%m-%d')
prop['end_date'] = datetime.strftime(now,'%Y-%m-%d')
ww.get_daily_data(prop)


prop = {'start_date': 20180208, 'end_date': str_now,'symbol':all_symbol ,
   'fields': 'open,close,high,low,volume','dtype':'list','freq':'1M'}
data = js.get_daily_data(prop)


