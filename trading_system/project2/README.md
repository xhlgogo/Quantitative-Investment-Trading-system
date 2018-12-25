## 一、	题目1
### 1.	代码文件为project2_1.py，将spyder工作路径设置到掘金策略路径，运行后通过掘金客户端下载回测结果的json文件；
### 2.	read_backtest_json(path_name)函数用于读取掘金客户端回撤结果的json文件，统计题目要求的各项指标；
### 3.	回测时间为'2016-10-20 09:15:00'~ '2018-11-24 15:00:00'，手续费用通过backtest_commission_ratio设置；
### 4.	Fast=10，Slow=20，frequency = "900s"，不考虑交易成本：
![2.1.a](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.1.a.png)
### 5.	Fast=10，Slow=20，frequency = "900s"，考虑交易成本0.0005：
![2.1.b](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.1.b.png)

## 二、	题目2
### 1.	题目1中的策略代码，on_backtest_finished(context, indicator)函数在掘金客户端回测结束后保存主要回测指标net profit、maxdd、sharpe ratio；
### 2.	solution.py中，调用copy_main()函数读取掘金回测project2_1.py文件，修改context.fast、context.slow、filename后生成Fast（1-20）和Slow（20-60）回测文件复制到掘金策略路径（见copy_file.zip）；
### 3.	使用安装了掘金SDK的Anaconda Prompt终端cd到掘金策略路径，使用cmd命令行“python + 文件名.py”批量执行不同的回测文件，得到相应的回测指标（见indicator.zip）；
### 4.	solution.py中，调用read_indicator_FastSlow(path)函数读取回测指标，得到netprofit_data,maxdd_data,sharpratio_data用于绘图；
### 5.	solution.py中，调用plot_3D(path)函数绘制3D曲面图，最终选择fast=2,slow=20，详细回测文件为“回测_fast2_slow20.json”，指标统计使用read_backtest_json(path_name)函数结果如下：
![2.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.2.png)

## 三、	题目3
### 1.	代码文件为project2_3.py，使用不同的时间窗口列表，每次执行策略函数时先判断当前时间是否在交易窗口内；
### 2.	手动修改、运行每日交易2小时、时间窗间隔15分钟的不同时间窗口，on_backtest_finished(context, indicator)函数记录每个窗口的指标；
### 3.	TimeFilter()函数中，调用read_indicator_TimeFilter(path)函数读取保存的不同时间窗口的回测结果json文件（TimeFilter.zip），然后绘制netprofit，maxdd和sharperatio交易窗口变化图在一张图中：
![2.3.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.3.1.png)
### 4.	选取时间交易窗口为13：45-09：45，此时sharpratio和netprofit接近高点、maxdd接近最低点，且左右相邻时间窗口有缓冲，此窗口详细回测文件为”回测-TimeFilter.json”；
### 5.	指标统计使用read_backtest_json(path_name)函数结果如下：
![2.3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.3.png)

## 四、	题目4
### 1.	solution.py中，调用MAE(path_name)函数，读取回测文件”回测-TimeFilter.json”，绘制MAE如图：
![2.4.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.4.1.png)
### 2.	solution.py中，调用stop_loss(path_name)，读取回测文件”回测-TimeFilter.json”，绘制不同止损比例下NetProfit/MaxDD的变化图：
![2.4.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.4.2.png)
### 3.	确定每次交易的StopLoss比例为0.15%

## 五、	题目5
### 1.	solution.py中，调用TrailingStop (path_name)，读取回测文件”回测- TrailingStop.json”， 绘制NetProfit/MaxDD变化图：
![2.5.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.5.1.png)
### 2.	确定每次交易的TrailingStop比例为0.62%
### 3.	指标统计使用read_backtest_json(path_name)函数结果如下：
![2.5](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.5.png)

## 六、	题目6
### 1.	solution.py中，调用MFE(path_name)函数，读取回测文件”回测-TrailingStop.json”，绘制MFE如图：
![2.6](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.6.png)
