import pymongo
import pandas as pd
from datetime import datetime
from pymongo import UpdateOne


class MongoSync(object):
    def __init__(self, prop_f, prop_t, dbname='all'):
        self.cl_from = self.mongo_client(prop_f)
        self.cl_to = self.mongo_client(prop_t)
        self.all_dbn = self.cl_from.database_names()
        if dbname == 'all':
            self.sync_all()
        else:
            self.set_db(dbname)
        
    def set_db(self, dbname):
        self.db_from = self.cl_from[dbname]
        self.db_to = self.cl_to[dbname]
            
    def mongo_client(self,prop): 
        host = prop['host']
        port = prop['port']
        return pymongo.MongoClient(host,port)
    
    def sync_coll(self, cl_name):
        last_f = self.db_from[cl_name].find_one(sort=[('datetime',pymongo.DESCENDING)])
        last_t = self.db_to[cl_name].find_one(sort=[('datetime',pymongo.DESCENDING)])
    
        if last_t:
            if last_t == last_f:
                print('{}数据库{}表的数据已是最新'.formart(self.dbname,cl_name))
            else:
                start_date = last_t['datetime']
                cs = self.db_from[cl_name].find({'datetime':{'$gt':start_date}})
                data = list(cs)[1:]
                [self.db_to[cl_name].update_one({}, {'$set': i}, upsert=True) for i in data]
                #print ('{}数据库{}表的数据已从{}更新到最新'.formart(self.dbname,cl_name,start_date))
        else:
            cs = self.db_from[cl_name].find({"datetime":{'$exists':True}})
            data = list(cs)
            self.db_to[cl_name].insert_many(data)
            
        #-------------------------------check----------------------------------
        new_data = list(self.db_to[cl_name].find({"datetime":{'$exists':True}}))
        if new_data == data:
            print ('数据更新成功')
        else:
            info = pd.DataFrame(data={'len':[len(data),len(new_data)],
                                      'start':[data[0]['datetime'],new_data[0]['datetime']],
                                      'end':[data[-1]['datetime'],new_data[-1]['datetime']]
                                       })
            print ('数据未全部更新成功',info)
            #print ('{}数据库{}表的数据原本不存在，已更新到最新'.formart(self.dbname,cl_name))
            
    def sync_db(self):
        colls = self.db_from.list_collection_names().sort()
        [self.sync_coll(coll) for coll in colls]
        print ('{}数据库已更新到最新'.formart(self.dbname))

    def sync_all(self):
        for dbn in self.all_dbn:
            self.set_db(dbn)
            self.sync_db()
            
prop_f = {'host':'192.168.0.102','port':27017}
prop_t = {'host':'localhost','port':27017}
ms = MongoSync(prop_f,prop_t)

