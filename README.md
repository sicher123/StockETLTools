# DataSync-数据同步服务

## 1.


## 2. 本地数据同步

### 2.1 脚本目录
```angularjs
cd DataSync/datasync/sync
python xxx_sync.py
```
| 脚本名    |说明  |  
| --------    | :----: |   
| gonjin_sync.py |  用于国金服务器的基础数据同步  |  
| jaqs_sync.py |  从jaqs同步数据到本地hdf5  |  
| jaqs_mongo_sync.py |  从mongodb同步数据到本地hdf5  |  
| dyfactor.py |  从mongodb同步数据到本地hdf5  |

### 2.2 配置信息 

| 名称      |说明  | 
| --------  | :----: |   
| fp     |  本地文件目录   | 
| mongo_db_config |  mongodb配置信息   | 
| jaqs_config |  jaqs登陆信息   |
| lb_update_type |  lb数据全量（replace）或增量（add）更新   |
| default_start_date | 默认数据起始日期 |
 |default_furture_date | 默认数据未来日期取到X日 |
 

