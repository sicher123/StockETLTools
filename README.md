# data_service demo
金融数据分析，各类数据源繁多，且调取方法与数据格式也都不同，不同使用者需求也不同。本项目将各种不同的数据源统一接口，输出标准化的数据格式。使用者不需要了解数据获取与规整化的繁杂过程，可以简单地获取到自己需要的数据。目前支持的数据源与数据库有：

| 数据源       | 支持数据    |  说明  |
| --------   | -----:   | :----: |
| Wind       | 免费版支持基础类型数据，机构版支持全类型数据     |  需要先安装wind量化接口，安装方法见 http://www.dajiangzhang.com/document     |
| Jaqs | 股票分钟/日行情,小部分财务数据    |   需要安装jaqs包    |


| 数据库(存储方案)       |说明  |  使用场景  |
| --------   | ----: | :----: |
| 内存      |     |  仅使用小数据量，低频率研究与生产|
| excel      |     |  需要跨平台做研究与生产|
| hdf5   |     |  大批量数据，仅用于研究 |
| mongodb |     |  大批量数据的研究与生产 |

## 1 功能
### 1.1 基础功能
如果仅需要标准格式的数据，可以把data_service当作基本工具

engine.py已经高度封装，根据需要在config.py修改参数并执行，即可对数据进行增删改查操作。 
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

## 2 
