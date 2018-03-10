# data_service

## 1 直接使用
data_engine.py已经高度封装，在config.py修改参数即可执行数据的增删改查操作。 
具体参数格式如下：



### conf

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
      <td></td>
   </tr>
</table>

### prop

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
