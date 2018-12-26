## 一、	题目1
### 1.	设置为每次交易1手，fast-slow=2-16，frequency=15min，window=['14:00:00', '09:45:00']，commission_ratio=0.0001，start_time='2016-10-20’， end_time='2018-11-24’
### 2.	Solution.py主函数调用nav_line(path_name,figure_name)读取掘金回测文件绘制净值线和高水平线如图:
![4.1.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.1.1.png)
### 3.	各指标为：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
176.8%  |   84.35%  |   3.27 |   3.79%  |    435   | 52.33% 
### 4.	调用read_json.read_backtest_json(path_name)读取回测文件得：
![4.1.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.1.2.png)

## 二、	题目2
### 1.	策略代码见project4_2.py，每次交易调仓比例： 0.1 *（（当前净值 - 保证金 - 最大回撤*1.5）/当前净值）
### 2.	在掘金客户端回测中，保证金比例粗略使用当前净值*10%，最大回测使用context.account().cash实时获取当前净值计算得到；
### 3.	Solution.py主函数调用nav_line(path_name,figure_name)读取掘金回测文件（绘制净值线和持仓情况如图
![4.2.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.2.1.png)
![4.2.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.2.2.png)
![4.2.3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.2.3.png)
### 4.	各指标为：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
132.85% |   63.38%  |   3.24 |   3.12%  |    432   | 52.33% 
### 降低了最大回撤，同时收益减小。

## 三、	题目3
### 1.	每次止损时损失的总资金的比例有限，即最大风险比例，策略代码见project4_3.py；
### 2.	每次调仓买入比例为：（最大风险比例/止损比例）*（（当前现金+持仓成本*0.9）/当前净值）
### 3.	不同最大风险比例：
#### 1)	固定最大风险金额比例为 2%
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
172.85% |   82.45%  |   3.27 |   3.70%  |    434   | 52.33% 

![4.3.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.1.png)
![4.3.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.2.png)
![4.3.3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.3.png)
#### 2)	固定最大风险金额比例为 5%
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
224.84% |  116.82%  |   3.19 |   4.73%  |    436   | 52.33% 

![4.3.4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.4.png)
![4.3.5](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.5.png)
![4.3.6](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.6.png)
#### 3)	固定最大风险金额比例为 10%
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
988.41% |  471.59%  |   2.86 |   9.31%  |    434   | 51.84% 

![4.3.7](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.7.png)
![4.3.8](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.8.png)
![4.3.9](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.9.png)
#### 4.	随着容忍损失的增大，收益率上升、夏普率下降、最大回撤增加

## 四、	题目4
### 1.	书上对于两种仓位管理的比较是：＜/br＞
Ralph Vince, fixed fractional lots = constant * account-size ＜/br＞
Ryan Jones, fixed ratio lots = constant * squareroot(account-size)
### 2.	固定盈利额比例资金管理时交易手数的推导：
![4.4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.png)
###   即我们只需根据累计盈利 P 和初始手数 N0 以及增加 1 手交易所需的盈利额delta即可确定交易手数。这里我们的 N0 设为初始资金 100 万的10%仓位，即 7手。Delta 可随时调整，决定了加仓速率的快慢。
### 3.	加仓逻辑：＜/br＞
持仓总资金只有在获利给定比例时（浮动盈亏>delta），才会继续加仓一手。＜/br＞
策略代码见project持仓总资金只有在获利给定比例时（浮动盈亏>delta），才会继续加仓一手。
### 5.	project4_4.py，使用context.account().positions()获取当前持仓方向和浮动盈亏，在没有均线上穿或下穿时，判断是否达到加仓条件，每次加仓100股；
#### 1)	权益增加1000（1千）：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
184.75% |  88.15%   |   3.19 |   3.75%  |    434   | 51.84% 

![4.4.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.1.png)
![4.4.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.2.png)
![4.4.3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.3.png)
#### 2)	权益增加10000（1万）：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
172.07% |  82.10%   |   3.17 |   3.72%  |    430   | 52.33% 

![4.4.4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.4.png)
![4.4.5](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.5.png)
![4.4.6](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.6.png)
#### 3)	权益增加100000（十万）：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
176.79% |  84.35%   |   3.27 |   3.79%  |    435   | 52.33% 

![4.4.7](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.7.png)
![4.4.8](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.8.png)
![4.4.9](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.4.9.png)
#### 5.	策略在执行过程中，加仓后会增大一倍下次加仓的浮动盈亏要求，因此与固定盈利额比例资金管理稍显不同（放大的要求平仓后下次开仓未还原）。
