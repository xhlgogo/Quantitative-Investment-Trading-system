## 一、	题目1
### 1.	策略代码见project3_1.py，frequency为10分钟：
![10min](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/10min.PNG)
![15min](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/15min.PNG)
![30min](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/30min.PNG)
![1h](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/1h.PNG)
![2h](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/2h.PNG)
![1d](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/1d.PNG)
### 7.	solution.py，调用TimeScale(path_name)读取回测过程中保存的指标文件后绘图：
![4.1.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.1.1.png)
![4.1.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.1.2.png)
### 8.	可以看到，frequency为15分钟时，shap_ratio和pnl_ratio处于次优，而max_dd最小，随着时间尺度的放大，开仓次数减少。这是因为此前的优化都是在15min Bar上做的。

## 二、	题目2
### 1.	15分钟行情，均线（2，20），时间窗口['14:00:00', '09:45:00']（受限于掘金客户端回测无夜盘）；
### 2.	由于蒙特卡罗模拟只是打乱了每笔交易的顺序，每天的收益率也只是进行了重新排序，因而根据年化收益和标准差（波动率）的计算方式，年化收益和夏普比率并没有发生变化，我们主要研究的是最大回撤和最大回撤回复期的情况
### 3.	Solution.py中，主函数调用Monte_Carlo(path_name)，读取15分钟掘金回测数据（回测-15min.json），使用random扰乱每笔交易的盈亏数据，然后使用matplotlib进行正态分布拟合并绘图：
### 4.	最大回撤拟合，均值150897.07，方差39346.34
![4.2.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.2.1.png)
### 5.	最大回撤时间拟合，均值94.27，方差34.47
![4.2.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.2.2.png)

## 三、	题目3
### 1.	Anchored walk forward analysis：fast=[2，5]，slow=[15，25]，frequency=15min，commission_ratio=0.0001，trade_time_windows=['14:00:00', '09:45:00']
### 2.	Solution.py中，主函数调用copy_file(path_name)，批量生成用于回测的不同fast_slow、相同起始时间、间隔1个月结束时间的回测文件，使用cmd批量运行回测，保存各回测指标;
### 3.	Solution.py中，主函数调用walkforward_analysis(path,walk_name)，读取Anchored walk forward analysis回测指标json文件，生成sharp_ratio、pnl_ratio、max_drawdown统计表格和折线图;
### 4.	回测时间’ 2016-10-20’~’ 2017-11-24’：
### 5.	最优系统参数统计：
End_Time |	17-11	| 17-12	| 18-01	| 18-02	| 18-03	| 18-04	| 18-05
-------- | :----: | :---: |-----: | :---: | :---: | :---: | :---:
Fast	   |    2   |   2   |   2   |    2  |   2   |  2    |  2
Slow	   |    16  |   16  |   17  |    16 |   16  |  17   |  17
### 6.	Out_of_Sample，随后半年为参数测试窗口，调用walkforward_test(path,walk_name)函数统计：
![4.3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.3.png)

## 四、	题目4
### 1.	Rolling walk forward analysis：fast=[2，5]，slow=[15，25]，frequency=15min，commission_ratio=0.0001，trade_time_windows=['14:00:00', '09:45:00']
### 2.	Solution.py中，主函数调用copy_file(path_name)，批量生成用于回测的不同fast_slow、滑动窗口为1年的回测文件，使用cmd批量运行回测，保存各回测指标；
### 3.	Solution.py中，主函数调用walkforward_analysis(path,walk_name)，读取Rolling walk forward analysis回测指标json文件，生成sharp_ratio、pnl_ratio、max_drawdown统计表格和折线图；
### 4.	最优系统参数统计：
End_Time |	17-11	| 17-12	| 18-01	| 18-02	| 18-03	| 18-04	| 18-05
-------- | :----: | :---: |-----: | :---: | :---: | :---: | :---:
Fast	   |    2   |   2   |   2   |    2  |   2   |  2    |  2
Slow	   |    16  |   16  |   17  |    16 |   16  |  17   |  16
### 5.	Out_of_Sample，随后半年为参数测试窗口，调用walkforward_test(path,walk_name)函数统计：
![4.4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.4.png)

## 五、	题目5
### 1.	对比：除最后一个月其他参数均相同（各窗口最优与次优有差异，略去不提）
![4.5.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.5.1.png)
![4.5.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.5.2.png)

## 六、	题目6
### 若将优化窗口缩短为半年，最优系统参数大概率会与优化窗口为1年的不同，绩效指标会可能会变差。
