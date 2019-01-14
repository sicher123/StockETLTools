import bcolz


class BcolzStorage(object):
    def __init__(self, path):
        self.path = path
        self.file = bcolz.open(path)
