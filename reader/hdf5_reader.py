import jaqs_fxdayu.data.dataservice
class HDF5Base(object):
    def __init__(self,fp,dbname):
        super(DailyDB, self).__init__(fp)
        self.path = self.get_db(dbname)

    def get_info(self,field):
        with h5py.File(self.path + '//dbInfo.h5') as file:
            data = file.attrs[field]
            return data

    def get_attr(self,field,name = 'dbInfo'):
        with h5py.File(self.path + '//%s.h5'%(name)) as file:
            if field in file.attrs.keys():
                return file.attrs[field]
            else:
                return None

    def get_file(self,colname):
        return h5py.File(self.path + '//' + colname + '.hd5')

    @staticmethod
    def _convert_string_array(dt, encoding, itemsize=None):
        from pandas._libs import lib
        from pandas.core.dtypes.common import _ensure_object

        if dt.dtype.name == 'object':
            # encode if needed
            if encoding is not None and len(dt):
                dt = pd.Series(dt.ravel()).str.encode(encoding).values.reshape(dt.shape)

            # create the sized dtype
            if itemsize is None:
                itemsize = lib.max_len_string_array(_ensure_object(dt.ravel()))

            dt = np.asarray(dt, dtype="S%d" % itemsize)
            return dt
        else:
            return dt

class HDF5DailyReader(HDF5Base):
    def __init__(self,fp,dbname):
        super(HDF5DailyReader, self).__init__(fp,dbname)

    def query_by_field(field):
        _dir = self.path + '//' + field + '.hd5'
        dset = h5py.File(_dir)['data']
        data = dset[start_index:end_index, symbol_index]

        if field not in ['float', 'float32', 'float16', 'int']:
            data = data.astype(str)
        if field == 'trade_date':
            data = data.astype(float).astype(int)
        return data


data = [query_by_field(f) for f in fld]
df = pd.DataFrame(np.concatenate(data, axis=1))

df.columns = cols_multi
df.index.name = 'trade_date'
df = df.stack().reset_index(drop=True)

def daily(self, props = None,sql = None):
    fields = props['fields']

    if isinstance(fields, str):
        fields = fields.split(',')
    if isinstance(symbol, str):
        symbol = symbol.split(',')

    daily_fp = self.fp + '//' + 'daily'

    exist_field = [i[:-4] for i in os.listdir(daily_fp)]
    dset = h5py.File(daily_fp + '//' + 'symbol.hd5')
    exist_symbol = dset['symbol_flag'][:, 0].astype(str)
    _symbol = [x for x in symbol if x in exist_symbol]
    exist_dates = dset['date_flag'][:, 0].astype(int)

    fld = [i for i in fields if i in exist_field] + ['symbol', 'trade_date']
    fld = list(set(fld))

    need_dates = self.query_trade_dates(start_date, end_date)
    start = need_dates[0]
    end = need_dates[-1]

    if start not in exist_dates or end not in exist_dates:
        raise ValueError('起止日期超限')

        # --------------------------query index----------------------------
    df, msg = self.query(view="jz.instrumentInfo",
                         fields="symbol,market",
                         filter="inst_type=100",
                         data_format='pandas')

    df = df[(df['market'] == 'SZ') | (df['market'] == 'SH')]
    all_univ = df['symbol'].values

    # --------------------------adjust----------------------------
    if adjust_mode == 'post' and symbol[0] not in all_univ:
        fld.extend(['open_adj', 'high_adj', 'low_adj', 'close_adj', 'vwap_adj'])
        fld = list(set(fld) - set(['open', 'high', 'low', 'close', 'vwap']))

    # --------------------------query&trans----------------------------
    symbol_index = [np.where(exist_symbol == i)[0][0] for i in _symbol]
    symbol_index.sort()
    start_index = np.where(exist_dates == start)[0][0]
    end_index = np.where(exist_dates == end)[0][0] + 1

    sorted_symbol = [exist_symbol[i] for i in symbol_index]
    cols_multi = pd.MultiIndex.from_product([fld, sorted_symbol], names=['fields', 'symbol'])



    for i in df.columns:
        if i == 'trade_date':
            df[i] = df[i].astype(int)
        elif i == 'symbol':
            df[i] = df[i].astype(str)
        else:
            df[i] = df[i].astype(float)

    return df.sort_values(by=['symbol', 'trade_date']), "0,"