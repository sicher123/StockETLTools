import pandas as pd
from datasync.origin import DataOrigin, props_to_sql


class MSSqlOrigin(DataOrigin):
    def __init__(self, db_config):
        super(MSSqlOrigin, self).__init__(db_config)
        self.conn = None
        self.connect()

    def connect(self):
        import pymssql as sqldb
        db_config = self.db_config
        try:
            self.conn = sqldb.connect(db_config['addr'], db_config['user'], db_config['password'])
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self, props=None, sql=None):
        if sql is None:
            sql = props_to_sql(props)
        data = pd.read_sql(sql, self.conn)
        return data

    def read_multi(self, props):
        if isinstance(props, list):
            data = pd.concat([self.read(props=i) for i in props])
            return data

    def get_fields(self, view):
        c = self.conn.cursor()
        c.execute('''Select Name FROM SysColumns Where id=Object_Id('%s')''' % (view,))
        cols = [i[0] for i in c.fetchall()]
        return cols

    @staticmethod
    def multi_insert_table(src_file, conn, cursor, table='STOCK_SNAPSHOT_1m', chunk_size=80):
        """
        手动优化<一次多行写入数据库指定TABLE>
        """
        with open(src_file, 'r', encoding='gbk') as f:
            items = f.readlines()

        line_decorator = lambda x: "('" + x.strip('\r\n').replace(',', "', '") + "')"
        all_rows = [line_decorator(row) for row in items]
        sql = 'INSERT INTO ' + table + ' VALUES '

        n, k = len(all_rows) // chunk_size, len(all_rows) % chunk_size
        for i in range(n):
            multi_rows = ', '.join(all_rows[i * chunk_size:(i + 1) * chunk_size])
            cursor.execute(sql + multi_rows)
        if k:
            multi_rows = ', '.join(all_rows[-k:])
            cursor.execute(sql + multi_rows)
        conn.commit()
        print("// %s has been writen to database successfully." % src_file)
        return None


def test_mssql():
    db_config = {'addr': "192.168.0.101",
                 'user': "SA",
                 'password': "Xinger520"}

    props = {'start_date': 20140801,
             'end_date': 20140906,
             'fields': '',
             'view': 'dbo.dbo.ASHAREEODDERIVATIVEINDICATOR',
             'DATE_NAME': 'TRADE_DT'}
    origin = MSSqlOrigin(db_config)
    return origin.read(props=props)
