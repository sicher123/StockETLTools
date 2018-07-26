from jaqs_fxdayu.data.dataservice import LocalDataService

dataview_folder = r'C:\Users\xinger\Sync\data'
ds = LocalDataService(fp=dataview_folder)
start = 20180201
end = 20180405
symbol = '000001.SZ,600000.SH'
fields = 'open'
adjust_mode=None

ds.daily('000001.SH',start_date=start,end_date=end,fields='open,vwap',adjust_mode='post')