# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:20:01 2018

@author: xinger
"""

from time import time
import pymongo
from pymongo import UpdateOne
from datetime import datetime,timedelta
from bson import ObjectId

now = datetime.now()
str_now = datetime.strftime(now,"%Y%m%d")

def mongo_client(host, port):    
    client = pymongo.MongoClient(host,port)
    return client


cl_from = mongo_client('192.168.0.102',27017)
cl_to = mongo_client('120.78.130.50',27018)
#cl_to = mongo_client('localhost',27017)

start = 20171110
end = int(str_now)

start_date = datetime.strptime(str(start),'%Y%m%d')
end_date = datetime.strptime(str(end),'%Y%m%d')




db_list = ['stock_1min']
#db_name = 'Stock_D'
#db = cl_from[db_name]
#symbol="000001.XSHE"
#[list(db[symbol].find({'datetime':{'$gt':start_date,'$lt':end_date}})) for symbol in symbol_list]

for db_name in db_list:
    start = time()
    symbol_list = db.list_collection_names()
    
    def func(symbol):
        flt = list(cl_to[db_name][symbol].find({'datetime':{'$gt':start_date,'$lt':end_date}}))
        _id = [i['_id'] for i in flt if len(flt) > 0]
        data = pd.DataFrame(list(cl_from[db_name][symbol].find({'datetime':{'$gt':start_date,'$lt':end_date}})))
        if len(data) > 0:
            data = data.set_index('_id')
        data = data.drop(_id).to_dict(orient='records')
        if len(data) > 0:
            #cl_to[db_name][symbol].insert(data,unique=True)
            cl_to[db_name][symbol].bulk_write([UpdateOne({"_id":{'$exists':False}},{'$set':x},upsert=True) for x in data])
            #cl_to[db_name][symbol].bulk_write([UpdateOne({"_id":{'$exists':False}},{'$set':x},upsert=True) for x in data])
            print(db_name,symbol,'OK')
            #print (cl_to[db_name][symbol].find_one(sort=[('datetime',pymongo.DESCENDING)]))
        else:
            print(db_name,symbol)
    [func(symbol) for symbol in symbol_list]
    
    #data = cl_to[db_name]['000001.XSHE'].find_one(sort=[('datetime',pymongo.DESCENDING)]) 
    #print(data)
    print(db_name,time() - start)
    
a = []

for db_name in db_list:
    start = time()
    db = cl_to[db_name]
    symbol_list = db.list_collection_names()
    
    def func(symbol):
        t = len(list(cl_to[db_name][symbol].find({'datetime':{'$gt':start_date,'$lt':end_date}},sort=[('datetime',pymongo.DESCENDING)])))
        if t < 5:
            print(symbol)
            a.append(symbol)
        #print (cl_to[db_name][symbol].find_one(sort=[('datetime',pymongo.DESCENDING)]))
    [func(symbol) for symbol in symbol_list]

