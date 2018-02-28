

# Stock_D

| 序号 |field | type | 中文名 | 更新频率 | 数据起始时间 |  数据来源 |描述 |
| - | :-: | :-: | :-: |:-: | :-: | :-: | -: |
| 1 | open | float |开盘价 | 日 |  |  |  |
| 2 | high | float |最高价 | 日 | | |  |
| 3 | low |float | 最低价 | 日 |  | |  |
| 4 | close |float| 收盘价| 日 |  | |  |
| 5 | volume |float | 最低价 | 日 |  | |  |
| 6 | turnover |float| 收盘价| 日 |  | | 1 |
| 6 | datetime |datetime.datetime| 收盘价| 日 |  | | 1 |

# Stock_1min

| 序号 |field | type | 中文名 | 更新频率 | 数据起始时间 |  数据来源 |描述 |
| - | :-: | :-: | :-: |:-: | :-: | :-: | -: |
| 1 | open | float |开盘价 | 日 |  |  |  |
| 2 | high | float |最高价 | 日 | | |  |
| 3 | low |float | 最低价 | 日 |  | |  |
| 4 | close |float| 收盘价| 日 |  | |  |
| 5 | volume |float | 最低价 | 日 |  | |  |
| 6 | turnover |float| 收盘价| 日 |  | | 1 |
| 6 | datetime |datetime.datetime| 收盘价| 日 |  | | 1 |

# 财务数据



# factor

<table>
   <tr>
      <td>名称</td>
      <td>类型</td>
      <td>描述</td>
   </tr>
   <tr>
      <td>symbol</td>
      <td>str</td>
      <td>股票代码</td>
   </tr>
   <tr>
      <td>datetime</td>
      <td>datetime.datetime</td>
      <td>交易日期</td>
   </tr>
   <tr>
      <td>AccountsPayablesTDays</td>
      <td>float</td>
      <td>应付账款周转天数（Accounts payable turnover days）。计算方法：应付账款周转天数=360/应付账款周转率。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>AccountsPayablesTRate</td>
      <td>float</td>
      <td>应付账款周转率（Accounts payable turnover rate）。计算方法：应付账款周转率=营业成本（TTM）/应付账款+应付票据+预付款项。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>AdminiExpenseRate</td>
      <td>float</td>
      <td>管理费用与营业总收入之比（Administrative expense rate）。计算方法：管理费用与营业总收入之比=管理费用（TTM）/营业总收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ARTDays</td>
      <td>float</td>
      <td>应收账款周转天数（Accounts receivable turnover days）。计算方法：应收账款周转天数=360/应收账款周转率。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ARTRate</td>
      <td>float</td>
      <td>应收账款周转率（Accounts receivable turnover rate）。计算方法：应收账款周转率=营业收入（TTM）/应收账款+应收票据+预收账款。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ASSI</td>
      <td>float</td>
      <td>对数总资产（Natural logarithm of total assets）。计算方法：对数总资产=总资产的对数。属于基础科目与衍生类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>BLEV</td>
      <td>float</td>
      <td>账面杠杆（Book leverage）。计算方法：账面杠杆=非流动负债合计/股东权益。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>BondsPayableToAsset</td>
      <td>float</td>
      <td>应付债券与总资产之比（Bonds payable to total assets）。计算方法：应付债券与总资产之比=应付债券/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CashRateOfSales</td>
      <td>float</td>
      <td>经营活动产生的现金流量净额与营业收入之比（Cash rate of sales）。计算方法：经营活动产生的现金流量净额与营业收入之比=经营活动产生的现金流量净额（TTM）/营业收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CashToCurrentLiability</td>
      <td>float</td>
      <td>现金比率（Cash to current liability）。计算方法：现金比率=期末现金及现金等价物余额（TTM）/流动负债合计。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CMRA</td>
      <td>float</td>
      <td>24月累计收益（Monthly cumulative return range over the past 24 months）。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>CTOP</td>
      <td>float</td>
      <td>现金流市值比（Cash flow to price）。计算方法：现金流市值比=每股派现（税前）×分红前总股本/总市值。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CTP5</td>
      <td>float</td>
      <td>5年平均现金流市值比（Five-year average cash flow to price）。计算方法：5年平均现金流市值比=近五年每股派现（税前）×分红前总股本/近五年总市值。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CurrentAssetsRatio</td>
      <td>float</td>
      <td>流动资产比率（Current assets ratio）。计算方法：流动资产比率=流动资产合计/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CurrentAssetsTRate</td>
      <td>float</td>
      <td>流动资产周转率（Current assets turnover rate）计算方法：流动资产周转率=营业收入（TTM）/流动资产合计。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CurrentRatio</td>
      <td>float</td>
      <td>流动比率（Current ratio），计算方法：流动比率=流动资产合计/流动负债合计。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>DAVOL10</td>
      <td>float</td>
      <td>10日平均换手率与120日平均换手率（Turnover Rate）之比。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>DAVOL20</td>
      <td>float</td>
      <td>20日平均换手率与120日平均换手率（Turnover Rate）之比。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>DAVOL5</td>
      <td>float</td>
      <td>5日平均换手率与120日平均换手率（Turnover Rate）之比。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>DDNBT</td>
      <td>float</td>
      <td>下跌贝塔（Downside beta），过往12个月中，市场组合日收益为负时，个股日收益关于市场组合日收益的回归系数。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>DDNCR</td>
      <td>float</td>
      <td>下跌相关系数（Downside correlation），过往12个月中，市场组合日收益为负时，个股日收益关于市场组合日收益的相关系数。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>DDNSR</td>
      <td>float</td>
      <td>下跌波动（Downside standard deviations ratio），过往12个月中，市场组合日收益为负时，个股日收益标准差和市场组合日收益标准差之比。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>DebtEquityRatio</td>
      <td>float</td>
      <td>产权比率（Debt equity ratio），计算方法：产权比率=负债合计/归属母公司所有者权益合计。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>DebtsAssetRatio</td>
      <td>float</td>
      <td>债务总资产比（Debt to total assets）。计算方法：债务总资产比=负债合计/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>DHILO</td>
      <td>float</td>
      <td>波幅中位数（median of volatility），每日对数最高价和对数最低价差值的3月内中位数。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>DilutedEPS</td>
      <td>float</td>
      <td>稀释每股收益（Diluted earnings per share）。属于每股指标类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>DVRAT</td>
      <td>float</td>
      <td>收益相对波动（Daily returns variance ratio-serial dependence in daily returns）。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>EBITToTOR</td>
      <td>float</td>
      <td>息税前利润与营业总收入之比。计算方法: 息税前利润与营业总收入之比=(利润总额+利息支出-利息收入)/ 营业总收入，如果没有利息支出，用财务费用代替，以上科目使用的都是TTM的数值。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>EGRO</td>
      <td>float</td>
      <td>5年收益增长率（Five-year earnings growth）。计算方法：5年收益增长率= 5年收益关于时间（年）进行线性回归的回归系数/5年收益均值的绝对值。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>EMA10</td>
      <td>float</td>
      <td>10日指数移动均线（Exponential moving average）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EMA120</td>
      <td>float</td>
      <td>120日指数移动均线（Exponential moving average）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EMA20</td>
      <td>float</td>
      <td>20日指数移动均线（Exponential moving average）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EMA5</td>
      <td>float</td>
      <td>5日指数移动均线（Exponential moving average）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EMA60</td>
      <td>float</td>
      <td>60日指数移动均线（Exponential moving average）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EPS</td>
      <td>float</td>
      <td>基本每股收益（Earnings per share）。属于每股指标类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>EquityFixedAssetRatio</td>
      <td>float</td>
      <td>股东权益与固定资产比率（Equity fixed assets ratio）。计算方法：股东权益与固定资产比率=股东权益/(固定资产+工程物资+在建工程)。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>EquityToAsset</td>
      <td>float</td>
      <td>股东权益比率（Equity to total assets）。计算方法：股东权益比率=股东权益/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>EquityTRate</td>
      <td>float</td>
      <td>股东权益周转率（Equity turnover rate） 计算方式：股东权益周转率=营业收入/股东权益。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ETOP</td>
      <td>float</td>
      <td>收益市值比（Earnings to price）。计算方法：收益市值比=净利润（TTM）/总市值。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ETP5</td>
      <td>float</td>
      <td>5年平均收益市值比（Five-year average earnings to price）。计算方法：5年平均收益市值比=近五年净利润（TTM）/近五年总市值。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>FinancialExpenseRate</td>
      <td>float</td>
      <td>财务费用与营业总收入之比（Financial expense rate）。计算方法：财务费用与营业总收入之比=财务费用（TTM）/营业总收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>FinancingCashGrowRate</td>
      <td>float</td>
      <td>筹资活动产生的现金流量净额增长率。计算方法：筹资活动产生的现金流量净额增长率=(今年筹资活动产生的现金流量净额（TTM）/去年筹资活动产生的现金流量净额（TTM）)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>FixAssetRatio</td>
      <td>float</td>
      <td>固定资产比率（Fixed assets ratio）。计算方法：固定资产比率=(固定资产+工程物资+在建工程)/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>FixedAssetsTRate</td>
      <td>float</td>
      <td>固定资产周转率（Fixed assets turnover rate）。计算方法：固定资产周转率=营业收入（TTM）/固定资产+工程物资+在建工程。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>GrossIncomeRatio</td>
      <td>float</td>
      <td>销售毛利率（Gross income ratio），计算方法：销售毛利率=(营业收入（TTM）-营业成本（TTM）)/营业收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>HBETA</td>
      <td>float</td>
      <td>历史贝塔（Historical daily beta），过往12个月中，个股日收益关于市场组合日收益的三阶自回归，市场组合日收益的系数。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>HSIGMA</td>
      <td>float</td>
      <td>历史波动（Historical daily sigma），过往12个月中，个股日收益关于市场组合日收益的三阶自回归，市场组合日收益的残差标准差。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>IntangibleAssetRatio</td>
      <td>float</td>
      <td>无形资产比率（Intangible assets ratio）。计算方法：无形资产比率=(无形资产+研发支出+商誉)/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>InventoryTDays</td>
      <td>float</td>
      <td>存货周转天数（Inventory turnover days）。计算方法：存货周转天数=360/存货周转率。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>InventoryTRate</td>
      <td>float</td>
      <td>存货周转率（Inventory turnover rate）。计算方法：存货周转率=营业成本（TTM）/存货。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>InvestCashGrowRate</td>
      <td>float</td>
      <td>投资活动产生的现金流量净额增长率（Growth rate of cash flows from investments）。计算方法：投资活动产生的现金流量净额增长率=(今年投资活动产生的现金流量净额（TTM）/去年投资活动产生的现金流量净额 （TTM）)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>LCAP</td>
      <td>float</td>
      <td>对数市值（Natural logarithm of total market values）。计算方法：对数市值=市值的对数。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>LFLO</td>
      <td>float</td>
      <td>对数流通市值（Natural logarithm of float market values）。计算方法：对数流通市值=流通市值的对数。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>LongDebtToAsset</td>
      <td>float</td>
      <td>长期借款与资产总计之比（Long term loan to total assets）。计算方法：长期借款与资产总计之比=长期借款/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>LongDebtToWorkingCapital</td>
      <td>float</td>
      <td>长期负债与营运资金比率（Long term debt to working capital）。计算方法：长期负债与营运资金比率=非流动负债合计/(流动资产合计-流动负债合计)。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>LongTermDebtToAsset</td>
      <td>float</td>
      <td>长期负债与资产总计之比（Long term debt to total assets）。计算方法：长期负债与资产总计之比=非流动负债合计/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>MA10</td>
      <td>float</td>
      <td>10日移动均线（Moving average）。取最近N天的前复权价格的均值。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MA120</td>
      <td>float</td>
      <td>120日移动均线（Moving average）。取最近N天的前复权价格的均值。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MA20</td>
      <td>float</td>
      <td>20日移动均线（Moving average）。取最近N天的前复权价格的均值。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MA5</td>
      <td>float</td>
      <td>5日移动均线（Moving average）。取最近N天的前复权价格的均值。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MA60</td>
      <td>float</td>
      <td>60日移动均线（Moving average）。取最近N天的前复权价格的均值。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MAWVAD</td>
      <td>float</td>
      <td>因子WVAD的6日均值。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>MFI</td>
      <td>float</td>
      <td>资金流量指标（Money Flow Index），该指标是通过反映股价变动的四个元素：上涨的天数、下跌的天数、成交量增加幅度、成交量减少幅度来研判量能的趋势，预测市场供求关系和买卖力道。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MLEV</td>
      <td>float</td>
      <td>市场杠杆（Market leverage）。计算方法：市场杠杆=非流动负债合计/(非流动负债合计+总市值)。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>NetAssetGrowRate</td>
      <td>float</td>
      <td>净资产增长率（Net assets growth rate）。计算方法：净资产增长率=(今年股东权益/去年股东权益)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>NetProfitGrowRate</td>
      <td>float</td>
      <td>净利润增长率（Net profit growth rate）。计算方法：净利润增长率=(今年净利润（TTM）/去年净利润（TTM）)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>NetProfitRatio</td>
      <td>float</td>
      <td>销售净利率（Net profit ratio），计算方法：销售净利率=净利润（TTM）/营业收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>NOCFToOperatingNI</td>
      <td>float</td>
      <td>经营活动产生的现金流量净额与经营活动净收益之比。计算方法：经营活动产生的现金流量净额与经营活动净收益之比=经营活动产生的现金流量净额（TTM）/(营业总收入（TTM）-营业总成本（TTM）)。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>NonCurrentAssetsRatio</td>
      <td>float</td>
      <td>非流动资产比率（Non-current assets ratio）。计算方法：非流动资产比率=非流动资产合计/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>NPParentCompanyGrowRate</td>
      <td>float</td>
      <td>归属母公司股东的净利润增长率。计算方法：归属母公司股东的净利润增长率=(今年归属于母公司所有者的净利润（TTM）/去年归属于母公司所有者的净利润（TTM）)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>NPToTOR</td>
      <td>float</td>
      <td>净利润与营业总收入之比（Net profit to total operating revenues），计算方法：净利润与营业总收入之比=净利润（TTM）/营业总收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>OperatingExpenseRate</td>
      <td>float</td>
      <td>营业费用与营业总收入之比（Operating expense rate）。计算方法：营业费用与营业总收入之比=销售费用（TTM）/营业总收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>OperatingProfitGrowRate</td>
      <td>float</td>
      <td>营业利润增长率（Operating profit growth rate）。计算方法：营业利润增长率=(今年营业利润（TTM）/去年营业利润（TTM）)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>OperatingProfitRatio</td>
      <td>float</td>
      <td>营业利润率（Operating profit ratio），计算方法：营业利润率=营业利润（TTM）/营业收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>OperatingProfitToTOR</td>
      <td>float</td>
      <td>营业利润与营业总收入之比（Operating profit to total operating revenues），计算方法：营业利润与营业总收入之比=营业利润（TTM）/营业总收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>OperatingRevenueGrowRate</td>
      <td>float</td>
      <td>营业收入增长率（Operating revenue growth rate）。计算方法：营业收入增长率=（今年营业收入（TTM）/去年营业收入（TTM））-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>OperCashGrowRate</td>
      <td>float</td>
      <td>经营活动产生的现金流量净额增长率。计算方法：经营活动产生的现金流量净额增长率=(今年经营活动产生的现金流量净额（TTM）/去年经营活动产生的现金流量净额（TTM）)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>OperCashInToCurrentLiability</td>
      <td>float</td>
      <td>现金流动负债比（Cash provided by operations to current liability）。计算方法：现金流动负债比=经营活动产生的现金流量净额（TTM）/流动负债合计。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>PB</td>
      <td>float</td>
      <td>市净率（Price-to-book ratio）。计算方法：市净率=总市值/归属于母公司所有者权益合计。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>PCF</td>
      <td>float</td>
      <td>市现率（Price-to-cash-flow ratio）。计算方法：总市值/经营活动产生的现金流量净额（TTM）。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>PE</td>
      <td>float</td>
      <td>市盈率（Price-earnings ratio）。使用TTM算法。市盈率=总市值/归属于母公司所有者的净利润（TTM）。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>PS</td>
      <td>float</td>
      <td>市销率（Price-to-sales ratio）。市销率=总市值/营业总收入（TTM）。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>PSY</td>
      <td>float</td>
      <td>心理线指标（Psychological line index），是一定时期内投资者趋向买方或卖方的心理事实转的数值度量，用于判断股价的未来趋势。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>QuickRatio</td>
      <td>float</td>
      <td>速动比率（Quick ratio）。计算方法：速动比率=(流动资产合计-存货)/ 流动负债合计。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>REVS10</td>
      <td>float</td>
      <td>股票的10日收益。属于动量类因子。</td>
   </tr>
   <tr>
      <td>REVS20</td>
      <td>float</td>
      <td>股票的20日收益。属于动量类因子。</td>
   </tr>
   <tr>
      <td>REVS5</td>
      <td>float</td>
      <td>股票的5日收益。属于动量类因子。</td>
   </tr>
   <tr>
      <td>ROA</td>
      <td>float</td>
      <td>资产回报率（Return on assets）。计算方法：资产回报率=净利润（TTM）/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ROA5</td>
      <td>float</td>
      <td>5年资产回报率（Five-year average return on assets）。计算方法：5年资产回报率=净利润（TTM）/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ROE</td>
      <td>float</td>
      <td>权益回报率（Return on equity）。计算方法：权益回报率=净利润（TTM）/股东权益。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ROE5</td>
      <td>float</td>
      <td>5年权益回报率（Five-year average return on equity） 计算方式：5年权益回报率=净利润/股东权益。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>RSI</td>
      <td>float</td>
      <td>相对强弱指标（Relative Strength Index），通过比较一段时期内的平均收盘涨数和平均收盘跌数来分析市场买沽盘的意向和实力，据此预测趋势的持续或者转向。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>RSTR12</td>
      <td>float</td>
      <td>12月相对强势（Relative strength for the last 12 months）。属于动量类因子。</td>
   </tr>
   <tr>
      <td>RSTR24</td>
      <td>float</td>
      <td>24月相对强势（Relative strength for the last 24 months）。属于动量类因子。</td>
   </tr>
   <tr>
      <td>SalesCostRatio</td>
      <td>float</td>
      <td>销售成本率（Sales cost ratio），计算方法：销售成本率=营业成本（TTM）/营业收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>SaleServiceCashToOR</td>
      <td>float</td>
      <td>销售商品提供劳务收到的现金与营业收入之比（Sale service cash to operating revenues）。计算方法：销售商品提供劳务收到的现金与营业收入之比=销售商品和提供劳务收到的现金（TTM）/营业收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>SUE</td>
      <td>float</td>
      <td>未预期盈余（Standardized unexpected earnings）。计算方法：未预期盈余=(最近一年净利润-除去最近一年的过往净利润均值)/ 除去最近一年的过往净利润标准差。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>TaxRatio</td>
      <td>float</td>
      <td>销售税金率（Tax ratio），计算方法：销售税金率=营业税金及附加（TTM）/营业收入（TTM）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>TOBT</td>
      <td>float</td>
      <td>超额流动（Liquidity-turnover beta）。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>TotalAssetGrowRate</td>
      <td>float</td>
      <td>总资产增长率（Total assets growth rate）。计算方法：总资产增长率=(今年总资产/去年总资产)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>TotalAssetsTRate</td>
      <td>float</td>
      <td>总资产周转率（Total assets turnover rate） 计算方式：总资产周转率=营业收入/总资产。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>TotalProfitCostRatio</td>
      <td>float</td>
      <td>成本费用利润率（Total profit cost ratio）。计算方法：成本费用利润率=利润总额/(营业成本+财务费用+销售费用+管理费用)，以上科目使用的都是TTM的数值。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>TotalProfitGrowRate</td>
      <td>float</td>
      <td>利润总额增长率（Total profit growth rate）。计算方法：利润总额增长率=(今年利润总额（TTM）/去年利润总额（TTM）)-1。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>VOL10</td>
      <td>float</td>
      <td>10日平均换手率（Turnover Rate）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VOL120</td>
      <td>float</td>
      <td>120日平均换手率（Turnover Rate）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VOL20</td>
      <td>float</td>
      <td>20日平均换手率（Turnover Rate）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VOL240</td>
      <td>float</td>
      <td>240日平均换手率（Turnover Rate）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VOL5</td>
      <td>float</td>
      <td>5日平均换手率（Turnover Rate）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VOL60</td>
      <td>float</td>
      <td>60日平均换手率（Turnover Rate）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>WVAD</td>
      <td>float</td>
      <td>威廉变异离散量（William's variable accumulation distribution），是一种将成交量加权的量价指标，用于测量从开盘价至收盘价期间，买卖双方各自爆发力的程度。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>REC</td>
      <td>float</td>
      <td>分析师推荐评级（Recommended rating score by analyst）。属于分析师类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>DAREC</td>
      <td>float</td>
      <td>分析师推荐评级变化（Changes of recommended rating score by analyst），相比于60个交易日前。属于动量类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>GREC</td>
      <td>float</td>
      <td>分析师推荐评级变化趋势（Change tendency of recommended rating score by analyst），过去60个交易日内的DAREC 符号加和。属于动量类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>FY12P</td>
      <td>float</td>
      <td>分析师盈利预测（Forecast earnings by analyst to market values）。属于价值类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>DAREV</td>
      <td>float</td>
      <td>分析师盈利预测变化（Changes of forecast earnings by analyst），相比于60个交易日前。属于动量类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>GREV</td>
      <td>float</td>
      <td>分析师盈利预测变化趋势（Change tendency of forecast earnings by analyst），过去60个交易日内的DAREV符号加和。属于动量类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>SFY12P</td>
      <td>float</td>
      <td>分析师营收预测（Forecast sales by analyst to market values）。属于价值类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>DASREV</td>
      <td>float</td>
      <td>分析师盈收预测变化（Changes of forecast sales by analyst），相比于60个交易日前。属于动量类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>GSREV</td>
      <td>float</td>
      <td>分析师盈收预测变化趋势（Change tendency of forecast sales by analyst），过去60个交易日内的DASREV 符号加和。属于动量类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>FEARNG</td>
      <td>float</td>
      <td>未来预期盈利增长（Growth of forecast earnings）。属于成长类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>FSALESG</td>
      <td>float</td>
      <td>未来预期盈收增长（Growth of forecast sales）。属于成长类因子。数据更新时间：T+1日04点00分。</td>
   </tr>
   <tr>
      <td>TA2EV</td>
      <td>float</td>
      <td>资产总计与企业价值之比（Assets to enterprise value）。属于价值类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>CFO2EV</td>
      <td>float</td>
      <td>经营活动产生的现金流量净额与企业价值之比（Cash provided by operations to enterprise value）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>ACCA</td>
      <td>float</td>
      <td>现金流资产比和资产回报率之差（Cash flow assets ratio minus return on assets）。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>DEGM</td>
      <td>float</td>
      <td>毛利率增长（Growth rate of gross income ratio），去年同期相比。计算方法：毛利率增长=(今年毛利率（TTM）/去年毛利率（TTM）)-1。属于质量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>SUOI</td>
      <td>float</td>
      <td>未预期毛利（Standardized unexpected gross income）。属于成长类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>EARNMOM</td>
      <td>float</td>
      <td>八季度净利润变化趋势（Change tendency of net profit in the past eight quarters），前8个季度的净利润，如果同比（去年同期）增长记为+1，同比下滑记为-1，再将8个值相加。属于动量类因子。数据更新时间：T日21点30分。</td>
   </tr>
   <tr>
      <td>FiftyTwoWeekHigh</td>
      <td>float</td>
      <td>当前价格处于过去1年股价的位置（Price level during the pasted 52 weeks）。属于动量类因子。</td>
   </tr>
   <tr>
      <td>Volatility</td>
      <td>float</td>
      <td>换手率相对波动率（Volatility of daily turnover during the last N days）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>Skewness</td>
      <td>float</td>
      <td>股价偏度（Skewness of price during the last N days），过去20个交易日股价的偏度。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>ILLIQUIDITY</td>
      <td>float</td>
      <td>收益相对金额比（Daily return to turnover value during the last N days），过去20个交易日收益相对金额的比例。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>BackwardADJ</td>
      <td>float</td>
      <td>股价向后复权因子，复权是对股价和成交量进行权息修复。属于收益和风险类因子。</td>
   </tr>
   <tr>
      <td>MACD</td>
      <td>float</td>
      <td>平滑异同移动平均线（Moving Average Convergence Divergence）,又称移动平均聚散指标。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ADTM</td>
      <td>float</td>
      <td>动态买卖气指标，用开盘价的向上波动幅度和向下波动幅度的距离差值来描述人气高低的指标。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>ATR14</td>
      <td>float</td>
      <td>14日均幅指标（Average TRUE Ranger），取一定时间周期内的股价波动幅度的移动平均值，是显示市场变化率的指标，主要用于研判买卖时机。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>ATR6</td>
      <td>float</td>
      <td>6日均幅指标（Average TRUE Ranger），取一定时间周期内的股价波动幅度的移动平均值，是显示市场变化率的指标，主要用于研判买卖时机。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>BIAS10</td>
      <td>float</td>
      <td>10日乖离率，简称Y值，是移动平均原理派生的一项技术指标，表示股价偏离趋向指标斩百分比值。属于动量类因子。</td>
   </tr>
   <tr>
      <td>BIAS20</td>
      <td>float</td>
      <td>20日乖离率，简称Y值，是移动平均原理派生的一项技术指标，表示股价偏离趋向指标斩百分比值。属于动量类因子。</td>
   </tr>
   <tr>
      <td>BIAS5</td>
      <td>float</td>
      <td>5日乖离率，简称Y值，是移动平均原理派生的一项技术指标，表示股价偏离趋向指标斩百分比值。属于动量类因子。</td>
   </tr>
   <tr>
      <td>BIAS60</td>
      <td>float</td>
      <td>60日乖离率，简称Y值，是移动平均原理派生的一项技术指标，表示股价偏离趋向指标斩百分比值。属于动量类因子。</td>
   </tr>
   <tr>
      <td>BollDown</td>
      <td>float</td>
      <td>下轨线（布林线）指标（Bollinger Bands），它是研判股价运动趋势的一种中长期技术分析工具。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>BollUp</td>
      <td>float</td>
      <td>上轨线（布林线）指标（Bollinger Bands），它是研判股价运动趋势的一种中长期技术分析工具。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>CCI10</td>
      <td>float</td>
      <td>10日顺势指标（Commodity Channel Index），专门测量股价是否已超出常态分布范围。属于动量类因子。</td>
   </tr>
   <tr>
      <td>CCI20</td>
      <td>float</td>
      <td>20日顺势指标（Commodity Channel Index），专门测量股价是否已超出常态分布范围。属于动量类因子。</td>
   </tr>
   <tr>
      <td>CCI5</td>
      <td>float</td>
      <td>5日顺势指标（Commodity Channel Index），专门测量股价是否已超出常态分布范围。属于动量类因子。</td>
   </tr>
   <tr>
      <td>CCI88</td>
      <td>float</td>
      <td>88日顺势指标（Commodity Channel Index），专门测量股价是否已超出常态分布范围。属于动量类因子。</td>
   </tr>
   <tr>
      <td>KDJ_K</td>
      <td>float</td>
      <td>随机指标。它综合了动量观念、强弱指标及移动平均线的优点，用来度量股价脱离价格正常范围的变异程度。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>KDJ_D</td>
      <td>float</td>
      <td>随机指标。它综合了动量观念、强弱指标及移动平均线的优点，用来度量股价脱离价格正常范围的变异程度。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>KDJ_J</td>
      <td>float</td>
      <td>随机指标。它综合了动量观念、强弱指标及移动平均线的优点，用来度量股价脱离价格正常范围的变异程度。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ROC6</td>
      <td>float</td>
      <td>6日变动速率（Price Rate of Change），以当日的收盘价和N天前的收盘价比较，通过计算股价某一段时间内收盘价变动的比例，应用价格的移动比较来测量价位动量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>ROC20</td>
      <td>float</td>
      <td>20日变动速率（Price Rate of Change），以当日的收盘价和N天前的收盘价比较，通过计算股价某一段时间内收盘价变动的比例，应用价格的移动比较来测量价位动量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>SBM</td>
      <td>float</td>
      <td>计算ADTM因子的中间变量。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>STM</td>
      <td>float</td>
      <td>计算ADTM因子的中间变量。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>UpRVI</td>
      <td>float</td>
      <td>计算RVI因子的中间变量。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>DownRVI</td>
      <td>float</td>
      <td>计算RVI因子的中间变量。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>RVI</td>
      <td>float</td>
      <td>相对离散指数（Relative Volatility Index），又称“相对波动性指标”，用于测量价格的发散趋势，主要用作辅助的确认指标，即配合均线系统、动量指标或其它趋势指标使用。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>SRMI</td>
      <td>float</td>
      <td>修正动量指标。属于动量类因子。</td>
   </tr>
   <tr>
      <td>ChandeSD</td>
      <td>float</td>
      <td>计算CMO因子的中间变量，SD是今日收盘价与昨日收盘价（下跌日）差值的绝对值加总。若当日上涨，则增加值为0。属于动量类因子。</td>
   </tr>
   <tr>
      <td>ChandeSU</td>
      <td>float</td>
      <td>计算CMO因子的中间变量，SU是今日收盘价与昨日收盘价（上涨日）差值加总。若当日下跌，则增加值为0。属于动量类因子。</td>
   </tr>
   <tr>
      <td>CMO</td>
      <td>float</td>
      <td>钱德动量摆动指标（Chande Momentum Osciliator），与其他动量指标摆动指标如相对强弱指标（RSI）和随机指标（KDJ）不同，钱德动量指标在计算公式的分子中采用上涨日和下跌日的数据。属于动量类因子。</td>
   </tr>
   <tr>
      <td>DBCD</td>
      <td>float</td>
      <td>异同离差乖离率，先计算乖离率BIAS，然后计算不同日的乖离率之间的离差，最后对离差进行指数移动平滑处理。优点是能够保持指标的紧密同步，并且线条光滑，信号明确，能够有效的过滤掉伪信号。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ARC</td>
      <td>float</td>
      <td>变化率指数均值，股票的价格变化率RC指标的均值，用以判断前一段交易周期内股票的平均价格变化率。属于动量类因子。</td>
   </tr>
   <tr>
      <td>OBV</td>
      <td>float</td>
      <td>能量潮指标（On Balance Volume，OBV），以股市的成交量变化来衡量股市的推动力，从而研判股价的走势。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>OBV6</td>
      <td>float</td>
      <td>6日能量潮指标（On Balance Volume，OBV），以股市的成交量变化来衡量股市的推动力，从而研判股价的走势。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>OBV20</td>
      <td>float</td>
      <td>20日能量潮指标（On Balance Volume，OBV），以股市的成交量变化来衡量股市的推动力，从而研判股价的走势。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>TVMA20</td>
      <td>float</td>
      <td>20日成交金额的移动平均值（Turnover Value Moving Average）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>TVMA6</td>
      <td>float</td>
      <td>6日成交金额的移动平均值（Turnover Value Moving Average）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>TVSTD20</td>
      <td>float</td>
      <td>20日成交金额的标准差（Turnover Value Standard Deviation）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>TVSTD6</td>
      <td>float</td>
      <td>6日成交金额的标准差（Turnover Value Standard Deviation）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VDEA</td>
      <td>float</td>
      <td>计算VMACD因子的中间变量（Volume Difference Exponential Average）。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VDIFF</td>
      <td>float</td>
      <td>计算VMACD因子的中间变量。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VEMA10</td>
      <td>float</td>
      <td>成交量的10日指数移动平均。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VEMA12</td>
      <td>float</td>
      <td>成交量的12日指数移动平均。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VEMA26</td>
      <td>float</td>
      <td>成交量的26日指数移动平均。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VEMA5</td>
      <td>float</td>
      <td>成交量的5日指数移动平均。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VMACD</td>
      <td>float</td>
      <td>成交量量指数平滑异同移动平均线（Volume Moving Average Convergence and Divergence），VMACD的意义和MACD基本相同, 但VMACD取用的数据源是成交量，MACD取用的数据源是成交价格。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VOSC</td>
      <td>float</td>
      <td>成交量震荡（Volume Oscillator），又称移动平均成交量指标，但它并非仅仅计算成交量的移动平均线，而是通过对成交量的长期移动平均线和短期移动平均线之间的比较，分析成交量的运行趋势和及时研判趋势转变方向。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VR</td>
      <td>float</td>
      <td>成交量比率（Volume Ratio），通过分析股价上升日成交额（或成交量，下同）与股价下降日成交额比值，从而掌握市场买卖气势的中期技术指标。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VROC12</td>
      <td>float</td>
      <td>12日量变动速率指标（Volume Rate of Change），以今天的成交量和N天前的成交量比较，通过计算某一段时间内成交量变动的幅度，应用成交量的移动比较来测量成交量运动趋向，达到事先探测 成交量供需的强弱，进而分析成交量的发展趋势及其将来是否有转势的意愿，属于成交量的反趋向指标。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VROC6</td>
      <td>float</td>
      <td>6日量变动速率指标（Volume Rate of Change），以今天的成交量和N天前的成交量比较，通过计算某一段时间内成交量变动的幅度，应用成交量的移动比较来测量成交量运动趋向，达到事先探测 成交量供需的强弱，进而分析成交量的发展趋势及其将来是否有转势的意愿，属于成交量的反趋向指标。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VSTD10</td>
      <td>float</td>
      <td>10日成交量标准差（Volume Standard Deviation），考察成交量的波动程度。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>VSTD20</td>
      <td>float</td>
      <td>20日成交量标准差（Volume Standard Deviation），考察成交量的波动程度。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>KlingerOscillator</td>
      <td>float</td>
      <td>成交量摆动指标，该指标在决定长期资金流量趋势的同时保持了对于短期资金流量的敏感性，因而可以用于预测短期价格拐点。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>MoneyFlow20</td>
      <td>float</td>
      <td>20日资金流量，用收盘价、最高价及最低价的均值乘以当日成交量即可得到该交易日的资金流量。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>AD</td>
      <td>float</td>
      <td>累积/派发线（Accumulation / Distribution Line，该指标将每日的成交量通过价格加权累计，用以计算成交量的动量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>AD20</td>
      <td>float</td>
      <td>累积/派发线（Accumulation / Distribution Line)的20日均线。属于动量类因子。</td>
   </tr>
   <tr>
      <td>AD6</td>
      <td>float</td>
      <td>累积/派发线（Accumulation / Distribution Line)的6日均线。属于动量类因子。</td>
   </tr>
   <tr>
      <td>CoppockCurve</td>
      <td>float</td>
      <td>估波指标（Coppock Curve），又称“估波曲线”，该指标通过计算月度价格的变化速率的加权平均值来测量市场的动量，属于长线指标，这里我们改为日间的指标。属于动量类因子。</td>
   </tr>
   <tr>
      <td>ASI</td>
      <td>float</td>
      <td>累计振动升降指标（Accumulation Swing Index），又称实质线，ASI企图以开盘、最高、最低、收盘价构筑成一条幻想线，以便取代目前的走势，形成最能表现当前市况的真实市场线（Real Market）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ChaikinOscillator</td>
      <td>float</td>
      <td>佳庆指标（Chaikin Oscillator），该指标基于AD曲线的指数移动均线而计算得到。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ChaikinVolatility</td>
      <td>float</td>
      <td>佳庆离散指标（Chaikin Volatility，简称CVLT，VCI，CV），又称“佳庆变异率指数”，是通过测量一段时间内价格幅度平均值的变化来反映价格的离散程度。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EMV14</td>
      <td>float</td>
      <td>简易波动指标（Ease of Movement Value），EMV将价格与成交量的变化结合成一个波动指标来反映股价或指数的变动状况，由于股价的变化和成交量的变化都可以引发该指标数值的变动，EMV实际上也是一个量价合成指标。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EMV6</td>
      <td>float</td>
      <td>简易波动指标（Ease of Movement Value），EMV将价格与成交量的变化结合成一个波动指标来反映股价或指数的变动状况，由于股价的变化和成交量的变化都可以引发该指标数值的变动，EMV实际上也是一个量价合成指标。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>plusDI</td>
      <td>float</td>
      <td>上升指标，DMI因子的构成部分。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>minusDI</td>
      <td>float</td>
      <td>下降指标，DMI因子的构成部分。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ADX</td>
      <td>float</td>
      <td>平均动向指数，DMI因子的构成部分。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ADXR</td>
      <td>float</td>
      <td>相对平均动向指数，DMI因子的构成部分。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>Aroon</td>
      <td>float</td>
      <td>Aroon通过计算自价格达到近期最高值和最低值以来所经过的期间数，帮助投资者预测证券价格从趋势到区域区域或反转的变化，Aroon指标分为Aroon、AroonUp和AroonDown3个具体指标。属于动量类因子。</td>
   </tr>
   <tr>
      <td>AroonDown</td>
      <td>float</td>
      <td>计算Aroon因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>AroonUp</td>
      <td>float</td>
      <td>计算Aroon因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>DEA</td>
      <td>float</td>
      <td>计算MACD因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>DIFF</td>
      <td>float</td>
      <td>计算MACD因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>DDI</td>
      <td>float</td>
      <td>方向标准离差指数，观察一段时间内股价相对于前一天向上波动和向下波动的比例，并对其进行移动平均分析，DDI指标倾向于显示一种长波段趋势的方向改变。属于动量类因子。</td>
   </tr>
   <tr>
      <td>DIZ</td>
      <td>float</td>
      <td>计算DDI因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>DIF</td>
      <td>float</td>
      <td>计算DDI因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>MTM</td>
      <td>float</td>
      <td>动量指标（Momentom Index），动量指数以分析股价波动的速度为目的，研究股价在波动过程中各种加速，减速，惯性作用以及股价由静到动或由动转静的现象。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MTMMA</td>
      <td>float</td>
      <td>因子MTM的10日均值。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>PVT</td>
      <td>float</td>
      <td>价量趋势（Price and Volume Trend）指标，把能量变化与价格趋势有机地联系到了一起，从而构成了量价趋势指标。属于动量类因子。</td>
   </tr>
   <tr>
      <td>PVT6</td>
      <td>float</td>
      <td>因子PVT的6日均值。属于动量类因子。</td>
   </tr>
   <tr>
      <td>PVT12</td>
      <td>float</td>
      <td>因子PVT的12日均值。属于动量类因子。</td>
   </tr>
   <tr>
      <td>TRIX5</td>
      <td>float</td>
      <td>5日收盘价三重指数平滑移动平均指标（Triple Exponentially Smoothed Average），TRIX根据移动平均线理论，对一条平均线进行三次平滑处理，再根据这条移动平均线的变动情况来预测股价的长期走势。属于动量类因子。</td>
   </tr>
   <tr>
      <td>TRIX10</td>
      <td>float</td>
      <td>10日收盘价三重指数平滑移动平均指标（Triple Exponentially Smoothed Average），TRIX根据移动平均线理论，对一条平均线进行三次平滑处理，再根据这条移动平均线的变动情况来预测股价的长期走势。属于动量类因子。</td>
   </tr>
   <tr>
      <td>UOS</td>
      <td>float</td>
      <td>终极指标（Ultimate Oscillator），现行使用的各种振荡指标，对于周期参数的选择相当敏感，不同市况、不同参数设定的振荡指标，产生的结果截然不同，因此，选择最佳的参数组合，成为使用振荡指标之前最重要的一道手续。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MA10RegressCoeff12</td>
      <td>float</td>
      <td>10日价格平均线12日线性回归系数。属于动量类因子。</td>
   </tr>
   <tr>
      <td>MA10RegressCoeff6</td>
      <td>float</td>
      <td>10日价格平均线6日线性回归系数。属于动量类因子。</td>
   </tr>
   <tr>
      <td>PLRC6</td>
      <td>float</td>
      <td>6日收盘价格线性回归系数（Price Linear Regression Coefficient）。属于动量类因子。</td>
   </tr>
   <tr>
      <td>PLRC12</td>
      <td>float</td>
      <td>12日收盘价格价格线性回归系数（Price Linear Regression Coefficient）。属于动量类因子。</td>
   </tr>
   <tr>
      <td>SwingIndex</td>
      <td>float</td>
      <td>振动升降指标，计算ASI因子的中间变量。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>Ulcer10</td>
      <td>float</td>
      <td>由Peter Martin于1987年提出，1989年发表于Peter Martin和Byron McCann的著作The Investors Guide to Fidelity Funds，用于考察向下的波动性。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>Ulcer5</td>
      <td>float</td>
      <td>由Peter Martin于1987年提出，1989年发表于Peter Martin和Byron McCann的著作The Investors Guide to Fidelity Funds，用于考察向下的波动性。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>Hurst</td>
      <td>float</td>
      <td>赫斯特指数（Hurst exponent）。是由英国水文专家H．E．Hurst提出了用重标极差(R/S)分析方法来建立赫斯特指数(H)，作为判断时间序列数据遵从随机游走还是有偏的随机游走过程的指标。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>ACD6</td>
      <td>float</td>
      <td>6日收集派发指标（Accumulative Distribution）。将市场分为两股收集（买入）及派发（估出）的力量。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>ACD20</td>
      <td>float</td>
      <td>20日收集派发指标（Accumulative Distribution），将市场分为两股收集（买入）及派发（估出）的力量。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>EMA12</td>
      <td>float</td>
      <td>12日指数移动均线（Exponential moving average）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>EMA26</td>
      <td>float</td>
      <td>26日指数移动均线（Exponential moving average）。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>APBMA</td>
      <td>float</td>
      <td>绝对偏差移动平均（Absolute Price Bias Moving Average）。考察一段时期内价格偏离均线的移动平均。属于动量类因子。</td>
   </tr>
   <tr>
      <td>BBI</td>
      <td>float</td>
      <td>多空指数（Bull and Bear Index）。是一种将不同日数移动平均线加权平均之后的综合指标。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>BBIC</td>
      <td>float</td>
      <td>因子BBI除以收盘价得到。属于动量类因子。</td>
   </tr>
   <tr>
      <td>TEMA10</td>
      <td>float</td>
      <td>10日三重指数移动平均线（Triple Exponential Moving Average），取时间N内的收盘价分别计算其一至三重指数加权平均。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>TEMA5</td>
      <td>float</td>
      <td>5日三重指数移动平均线（Triple Exponential Moving Average），取时间N内的收盘价分别计算其一至三重指数加权平均。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MA10Close</td>
      <td>float</td>
      <td>均线价格比。由于股票的成交价格有响起均线回归的趋势，计算均线价格比可以预测股票在未来周期的运动趋势。属于动量类因子。</td>
   </tr>
   <tr>
      <td>AR</td>
      <td>float</td>
      <td>人气指标，是以当天开市价为基础，即以当天市价分别比较当天最高，最低价，通过一定时期内开市价在股价中的地位，反映市场买卖人气。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>BR</td>
      <td>float</td>
      <td>意愿指标，是以昨日收市价为基础，分别与当日最高，最低价相比，通过一定时期收市收在股价中的地位，反映市场买卖意愿的程度。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>ARBR</td>
      <td>float</td>
      <td>人气指标（AR）和意愿指标（BR）都是以分析历史股价为手段的技术指标，ARBR使用AR减去BR得到的值。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>CR20</td>
      <td>float</td>
      <td>CR指标以上一个计算周期（这里为20日）的中间价比较当前周期的最高价、最低价，计算出一段时期内股价的“强弱”。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>MassIndex</td>
      <td>float</td>
      <td>梅斯线（Mass Index），本指标是Donald Dorsey累积股价波幅宽度之后所设计的震荡曲线。其最主要的作用，在于寻找飙涨股或者极度弱势股的重要趋势反转点。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>BearPower</td>
      <td>float</td>
      <td>空头力道，是计算Elder因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>BullPower</td>
      <td>float</td>
      <td>多头力道，是计算Elder因子的中间变量。属于动量类因子。</td>
   </tr>
   <tr>
      <td>Elder</td>
      <td>float</td>
      <td>艾达透视指标（Elder-ray Index），交易者可以经由该指标，观察市场表面之下的多头与空头力道。属于常用技术指标类因子。</td>
   </tr>
   <tr>
      <td>NVI</td>
      <td>float</td>
      <td>负成交量指标（Negative Volume Index），本指标的主要作用是辨别目前市场行情是处于多头行情还是空头行情，并追踪市场资金流向。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>PVI</td>
      <td>float</td>
      <td>正成交量指标（Positive Volume Index），本指标的主要作用是辨别目前市场行情是处于多头行情还是空头行情，并追踪市场资金流向。属于情绪类因子。</td>
   </tr>
   <tr>
      <td>RC12</td>
      <td>float</td>
      <td>12日变化率指数（Rate of Change），类似于动力指数，如果价格始终是上升的，则变化率指数始终在100%线以上，且如果变化速度指数在向上发展时，说明价格上升的速度在加快。属于动量类因子。</td>
   </tr>
   <tr>
      <td>RC24</td>
      <td>float</td>
      <td>24日变化率指数（Rate of Change），类似于动力指数，如果价格始终是上升的，则变化率指数始终在100%线以上，且如果变化速度指数在向上发展时，说明价格上升的速度在加快。属于动量类因子。</td>
   </tr>
   <tr>
      <td>JDQS20</td>
      <td>float</td>
      <td>阶段强势指标，该指标计算一定周期N日内，大盘下跌时，个股上涨的比例。属于情绪类因子。</td>
   </tr>

</table>
