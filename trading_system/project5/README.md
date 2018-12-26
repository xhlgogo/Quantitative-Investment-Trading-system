### 1.	选择布林带通道系统；
### 2.	布林带指标：＜/br＞
将移动平均线前移length个周期后形成布林中轨，在此中轨加减distance倍标准差，形成指标通道；
### 3.	开平仓信号：＜/br＞
	最高价向上突破通道上轨时开多仓；＜/br＞
	多仓时，最低价向下突破中轨平多仓；＜/br＞
	最低价向下突破通道下轨时开空仓；＜/br＞
	空仓时，最高价向上突破中轨平空仓.
### 4.	交易价格：＜/br＞
	买入做多：突破时布林上轨值＜/br＞
	买入做空：突破时布林下轨值＜/br＞
	卖出平仓：市价平仓
### 5.	初始版本掘金策略代码见’project5_1.py’；
#### 1)	Length=range(15,18)，Distance=np.arange(1.5,3.51,0.01)，solution.py调用copy_file(path_name)函数，批量修改策略文件的context.disp(length布林带平移参数)、context.sdev (distance布林带通道倍数参数)、策略文件名、回测结果文件名，将文件拷贝至掘金策略文件夹后，命令行“python file_name.py”使用cmd方式批量运行不同length-distance的策略文件；
#### 2)	solution.py调用length_distance(path_name)函数，统计回测结果中sharp_ratio > 0的回测指标json文件，绘图如下：
![5.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.1.png)
#### 3)	选取length=16，distance=2.33，统计指标如下：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
3.47%   |  1.66%    |   0.60 |   2.24%  |    9     | 66.67% 

![5.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.2.png)
![5.3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.3.png)
![5.4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.4.png)
#### 4)	使用frequence=[0.5h，23.5h]，间隔0.5小时的区间，生成回测文件进行批量回测，回测结果中并没有sharp_ratio > 0.6的，数据频率的放缓使得交易信号大幅减小。接下来先提高交易数据频率，使用批量回测文件找到length、distance大体区间；
#### 5)	先假定使用15分钟线，生成不同length in range(10,21)、distance in np.arange(1.0,3.1,0.1)的回测文件，不考虑交易成本，保存sharp_ratio>0的指标，统计如下：
![5.5](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.5.png)
#### 6.	考虑手续费commission_ratio=0.0001，对length=20，distance in np.arange(0.95，1.10，0.01)，保存sharp_ratio>0的指标，统计如下：
![5.6](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.6.png)
#### 7.	选择length = 20，distance = 1.03，调整手续费为万二（commission_ratio=0.0002），策略代码见’project5.3.py’，统计指标如下：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
94.15%  |  44.92%   |   2.37 |   12.75% |    915   | 56.67% 

![5.7](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.7.png)
![5.8](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.8.png)
![5.9](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.9.png)
