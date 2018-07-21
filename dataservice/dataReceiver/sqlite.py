# -*- coding: utf-8 -*-
"""
Created on Thu May 10 18:23:02 2018

@author: xinger
"""
import sqlite3
import pandas as pd
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")
today = int(datetime.strftime(datetime.today(), '%Y%m%d'))

fp = r'C:\Users\xinger\Sync\data'

class sqlite_db(object):
    def __init__(self, fp):
        path = fp + '//' + 'data.sqlite'
        self.fp = fp
        self.path = path
        self.conn = sqlite3.connect(path)

    @property
    def all_table_names(self):
        sql = '''SELECT name FROM sqlite_master WHERE type ='table' ORDER BY name;'''
        c = self.conn.cursor()
        c.execute(sql)
        return [i[0] for i in c.fetchall()]

    def execute(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()

    def set_attr(self, view, attrs):
        if 'attrs' not in self.all_table_names:
            sql = '''CREATE TABLE attrs
                    (
                    view CHAR(20) NOT NULL,
                    updated_date INT NOT NULL
                    );'''
            self.execute(sql)

        try:
            sql = '''UPDATE attrs SET updated_date = %s  WHERE view = "%s";''' % (attrs, view)
            self.execute(sql)
        except:
            sql = '''INSERT INTO attrs(view,updated_date) VALUES("%s",%s);''' % (view, attrs)
            self.execute(sql)

    def get_update_info(self,view):
        sql = '''select updated_date from "attrs" WHERE view = "%s";''' % (view,)
        c = self.conn.cursor()
        try:
            c.execute(sql)
            date = c.fetchall()[0][0]
        except:
            date = None
        return date

    def update_table(self, view, data, if_exists='append', on='index'):
        if on == 'index':
            return self.update_on_index(view, data, if_exists=if_exists)
        if on == 'columns':
            return self.update_on_index(view, data, if_exists=if_exists)

    def update_on_index(self, view, data, if_exists='append'):
        data.to_sql(view, self.conn, if_exists=if_exists, index=False)
        print(view, 'ok!')

    def update_on_columns(self):
        pass

