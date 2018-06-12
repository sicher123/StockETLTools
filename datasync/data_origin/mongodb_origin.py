import pymongo
import pandas as pd
from datasync.data_origin import DataOrigin

class MongodbOrigin(DataOrigin):
    def __init__(self, db_config):
        super(MSSqlOrigin, self).__init__(db_config)
        self.conn = None
        self.connect()

    def connect(self):

        db_config = self.db_config
        try:
            self.conn = pymongo.MongoClient(db_config['host'], db_config['port'])
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self, props=None, sql=None):
        if props:
            conf = props_to_mongo(props)
        elif sql:
            conf = sql_to_mongo(sql)

        cs = self.conn[conf['db']][conf['col']].find(conf['flt'], conf['prj'])
        data = pd.DataFrame(list(cs))

        return data