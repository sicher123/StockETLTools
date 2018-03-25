# data_service demo
## 1 quickstart
```
prop = {'start_date': 20170520,
        'end_date': 20170601,
        'symbol':'ALL' ,
        'fields': 'open,close,high,low,volume',
        'dtype':'list',
        'freq':'1M',
        'index':'ALL'}
        
conf = {}
conf['origin'] = 'wind'
conf['database'] = 'excel'
conf['data_form'] = 'daily'
conf['prop'] = prop
conf['dtype'] = 'daily'
conf['root'] = r'C:\Users\siche\Desktop\ext'

from engine import data_engine
de = data_engine(conf)
de.insert()
```
## 2 概述
金融数据的数据源繁多，其接口与数据格式也都不同，不同使用者需求也不同，往往需要花费很多资源去维护。
本项目统一了接口与数据格式，使得使用者只需要关注其需要的数据而不必在意技术细节。目前支持的数据源与数据库有：

| 数据源       | 支持数据    |   是否收费  |说明  |
| --------   | -----:   |  -----:   |:----: |
| Tushare-Pro | 股票分钟行情/日行情/财务数据    | 免费  |需要安装jaqs包 ,见https://github.com/quantOS-org/JAQS   |
| Wind       | 免费版支持基础行情数据，机构版支持金融市场全数据 | 基础版免费/机构版收费   |  需要先安装wind量化接口，安装方法见 http://www.dajiangzhang.com/document     |
| choice | 全市场数据   | 付费 | 需要安装东方财富choice接口，见http://quantapi.eastmoney.com/   |

| 数据库(存储方案)       |说明  |  使用场景  |
| --------   | ----: | :----: |
| 内存      |     |  仅使用小数据量，低频率研究与生产|
| excel      |     |  需要跨平台做研究与生产|
| hdf5   |     |  大批量数据，仅用于研究 |
| mongodb |     |  大批量数据的研究与生产 |

## 3 功能
根据需求划分不同等级的功能
### 2.1 将数据存储到本地文件
在config.py修改参数并执行，即可对数据进行增删改查操作。 
具体参数格式如下：

#### conf参数

<table>
   <tr>
      <td>中文名</td>
      <td>字段</td>
      <td>可选字段</td>
   </tr>
   <tr>
      <td>数据源</td>
      <td>origin</td>
      <td>wind/jaqs</td>
   </tr>
   <tr>
      <td>数据库</td>
      <td>database</td>
      <td>mongodb/excel/hdf5</td>
   </tr>
   <tr>
      <td>配置项</td>
      <td>prop</td>
      <td>见下表</td>
   </tr>
</table>

#### prop参数

<table>
   <tr>
      <td>中文名</td>
      <td>字段</td>
      <td>类型</td>
      <td>例</td>
      <td>说明</td>
   </tr>
   <tr>
      <td>开始日期</td>
      <td>start_date</td>
      <td>int</td>
      <td>20170101</td>
      <td></td>
   </tr>
   <tr>
      <td>截止日期</td>
      <td>end_date</td>
      <td>int</td>
      <td>20180101</td>
      <td></td>
   </tr>
   <tr>
      <td>合约代码</td>
      <td>symbol</td>
      <td>str</td>
      <td>'000001.SZ'</td>
      <td>单个或多个股票</td>
   </tr>
   <tr>
      <td>字段</td>
      <td>fields</td>
      <td>str</td>
      <td>'open,high,low,close'</td>
      <td></td>
   </tr>
   <tr>
      <td>返回数据的类型</td>
      <td>dtype</td>
      <td>str</td>
      <td>'list'</td>
      <td>list 或 dataframe</td>
   </tr>
   <tr>
      <td>分钟数据频率</td>
      <td>freq</td>
      <td>str</td>
      <td>‘1M’</td>
      <td></td>
   </tr>
</table>

```
from engine import data_engine
de = data_engine(conf)
#新建
de.insert()
#更新
de.update()
#查找
de.find()
#删除
de.delete()
```

## 2 
