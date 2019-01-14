import os
import json


class LocalFileSystem(object):
    def __init__(self, fp):
        dic = {'user': 'xinger',
               'password': 'Xinger520'
               }
        text = json.dumps(dic)

        if not os.path.exists(fp):
            os.mkdir(fp)
            with open('sysInfo.json', 'w') as file:
                file.write(text)

        self.is_registed = []

    def __getitem__(self, dbname):
        if dbname in self.is_registed:
            storage = self.sysInfo[dbname]['storage']
            return storage('dbname', self.folder_path)
        else:
            raise NotImplementedError('unregisted dbname')

    @property
    def sysInfo(self):
        with open('sysInfo.json', 'w') as file:
            return file.write(text)

    @property
    def folder_path(self):
        with open('sysInfo.json', 'w') as file:
            return file.write(text)

    def is_support(self, storage_type):
        pass

    def register(self, dbname, storage):
        if self.is_support(storage):
            with open('sysInfo.json', 'w') as file:
                pass
        else:
            print('storage - %s is not supported!' % (storage, ))


class StorageBase(object):
    def is_connected(self):
        pass


class FileStorageBase(StorageBase):
    def __init__(self, fp):
        self.fp = fp
        if not os.path.exists(fp):
            os.mkdir(fp)

    def get_db(self, dbname):
        path = self.fp + '//' + dbname
        if not os.path.exists(path):
            os.mkdir(path)
        #            with h5py.File(path + '//dbInfo.h5') as file:
        #                file.attrs['last_updated_time'] = str(datetime.now())
        return path


class DBStorageBase(StorageBase):
    def __init__(self, db_config):
        self.conn  = self.connection(db_config)

    def connection(self):
        return


class SqlBase(object):
    def source_path(self):
        return

    @property
    def cursor(self):
        return self.conn.cursor()

    def execute(self, sql):
        cursor = self.cursor
        cursor.execute(sql)
        if 'select' in sql or 'SELECT' in sql:
            return cursor.fetchall()
        else:
            self.conn.commit()
            cursor.close()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_all_table_names(self):
        pass


class HDF5Base(object):
    def __init__(self, path):
        pass

    def update_file(self):
        pass

    def read_file(self):
        pass

    def read_folder(self):
        pass


class Hdf5Storage(HDF5Base, StorageBase):
    def __init__(self):
        super(Hdf5Storage, self).__init__()



import blaze