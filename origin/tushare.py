import tushare as ts


TOKEN = '0e3b219dbfbbe497afe0650997c189bbc211afa4a2a38f37023483de'
TUSHARE_DATE_FORMAT = 'YYYY-MM-DD'
TUSHARE_PRO_DATE_FORMAT = 'YYYYMMDD'


tushare_map = {'start_date': 'start',
               'end_date': 'start'}


class TsSource(object):
    api = None
    __api_type = None

    def __init__(self):
        try:
            api = ts.pro_api(TOKEN)
            api.trade_cal(exchange='',
                          start_date='20180901',
                          end_date='20181001',
                          fields='exchange,cal_date,is_open,pretrade_date',
                          is_open='0')
            self.api = api
            self.__api_type = 'tushare pro'
            print('pro接口不可用，尝试转到普通接口')
        except Exception as e:
            if e == '抱歉，您输入的TOKEN无效！':
                self.api = ts
                self.__api_type = 'tushare'
            else:
                raise ('未知错误')

    def _ts_query(self):
        pass

    def _tspro_query(self):
        pass

    def query(self):
        pass

