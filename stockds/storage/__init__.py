import os
class StorageBase(object):
    pass


class FileStorageBase(StorageBase):
    def __init__(self, fp):
        self.fp = fp
        if not os.path.exists(fp):
            os.mkdir(fp)
            with h5py.File(fp + '//sysInfo.h5') as file:
                file.attrs['user'] = 'xinger'
                file.attrs['password'] = 'Xinger520'

    def get_db(self, dbname):
        path = self.fp + '//' + dbname
        if not os.path.exists(path):
            os.mkdir(path)
        #            with h5py.File(path + '//dbInfo.h5') as file:
        #                file.attrs['last_updated_time'] = str(datetime.now())
        return path


class DBStorageBase(StorageBase):
    pass


class HDF5Base(object):
    def __init__(self, path):
        pass

    def update_file(self):


    def read_file(self):
        pass

    def read_folder(self):
        pass




class Hdf5Storage(HDF5Base, StorageBase):
    def __init__(self):
        super(Hdf5Storage, self).__init__()
