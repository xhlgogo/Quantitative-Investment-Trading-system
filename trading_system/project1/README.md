## 1.	通过掘金数据，见project1.1.py
### 通过掘金的python SDK，history函数，获取上海黄金期货连续主力合约'SHFE.AU'日数据和5分钟数据；
### 开始时间为'2016-01-01'，结束时间为'2018-09-03'；
### 通过DataFrame .to_excel()储存数据为excel格式.

## 2.	净值表现分析，见project1.2.py
### 主函数，获取掘金日线数据、调用子函数完成计算并绘图；
### handle_data(his_data)函数，对DataFrame格式的交易数据计算市场相对回报、市场净值、高水准线、回撤时间及回撤比例；
### evaluation(his_data,timescale)函数，计算平均回报、风险、夏普率、最大回撤率、最大回撤期；
### plot_with_pyecharts(his_data)函数，使用pyecharts库绘制收益率的净值曲线图和回撤比例柱状图，结果为html文件（可进一步保存为其他格式）.
### 计算结果：
年化收益率	夏普比率	最大回撤率	最大回撤期
0.056007075	0.496067537	-0.094596142	548
![净值曲线图](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project1/SHFE.AU-%E5%87%80%E5%80%BC%E6%9B%B2%E7%BA%BF%E5%9B%BE.png)
![回撤比例柱状图](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project1/SHFE.AU-%E5%9B%9E%E6%B5%8B%E6%AF%94%E4%BE%8B%E6%9F%B1%E7%8A%B6%E5%9B%BE.png)

