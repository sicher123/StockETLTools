import pandas


class BaseView(object):
    def __init__(self):
        self.data = None
        self.type = None
        self.view_name = None

    def __str__(self):
        return self.name

    def __call__(self):
        return self.data

    def __setattr__(self, key, value):
        object.__setattr__(self, key ,value)

    def __getattr__(self, item):
        return item


class SeriesView(BaseView):
    def __init__(self):
        self.name = self.data.name


def check_contain_digit(check_str):
    for ch in check_str:
        if ch.isdigit():
            return True
    return False


class DFView(BaseView):
    def __init__(self, data):
        self.data = data
        self.index = data.index
        self.columns = data.columns

    def __call__(self):
        if self.index._typ == 'multiindex':
            data = self.data.reset_index()
            index_token = 'CrossDFView'

        if self.columns._typ == 'multiindex':
            data = self.data.stack(0).reset_index()
            index_token = 'CrossDFView'

        if False not in [check_contain_digit(i) for i in self.index.values] and data.index_typ in ['datetimeindex','int64index']:
            self.data.index.values.astype('int')
            index_token = 'TSDFView'

        return index_token



class panel_view(BaseView):
    def __init__(self):
        pass
