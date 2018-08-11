import os
import numpy as np
from datetime import datetime, timedelta
from datasync.log import Log
from datasync.dataReceiver.hdf5 import DailyDB
from datasync.data_origin.mongodb_origin import MongodbOrigin

today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
yestoday = int(datetime.strftime(datetime.today() - timedelta(days=1), '%Y%m%d'))
fp = r'C:\Users\xinger\Sync\data'
logger = Log(fp+'//log', today)
db_config = {'addr': '192.168.0.104'}
origin = MongodbOrigin(db_config)
view = 'dyfactors'

fields = origin.conn['fxdayu_factors'].collection_names()
db = DailyDB(fp, view)
exist_fields = db.exist_fields

for f in fields:
    if f not in exist_fields:
        print(f, 'start query')
        props = {'view': 'fxdayu_factors',
                 'start_date': 20140101,
                 'end_date': today,
                 'fields': f}
        data = origin.read(props)
        data = data.pivot(index='trade_date', columns='symbol', values=f)
        print(f, 'start update')
        db.update_a_file(data, f)
