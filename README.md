# Quantitative-Investment-Trading-system
用于中国人民大学财政金融学院刘振亚教授的“金融计量与量化策略分析”与“量化投资交易策略分析与系统设计”两门课程的课程作业和笔记记录。

## 一、《PPT_4.Momentum Crashes.pdf》为“金融计量与量化策略分析”课程我所在的3人小组论文研讨报告，对动量崩溃Momentum Crash(见paper文件夹)做了小组论文研读报告。
### 其他论文研读报告为其他小组做的，不便上传，有需要请邮件联系我。以下为部分截图：
![MC1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/paper/picture/MC1.PNG)
![MC2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/paper/picture/MC2.PNG)
![MC3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/paper/picture/MC3.PNG)
![MC4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/paper/picture/MC4.PNG)
![MC5](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/paper/picture/MC5.PNG)

## 二、“量化投资交易策略分析与系统设计”
### 0. 为实现\<trading system>中的量化交易系统,trading_system文件夹下，子文件夹内有相应README.md和数据文件；
### 1. 实现思路为：使用掘金客户端，批量生成不同参数的策略文件，代码中使用函数在回测结束时保存回测指标json用于筛选参数，具体的某一个回测详细结果json文件在客户端查看回测时手动下载用于分析最优结果详细数据；
#### 以下为部分结果：
#### 1）Fast=10，Slow=20，frequency = "900s"，考虑交易成本0.0005：
![2.1.b](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.1.b.png)
#### 2）Fast=2, Slow，TimeFilter时间窗口过滤：
![2.3.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project2/2.3.1.png)
#### 3）TimeScale数据频率选取：
![4.1.1](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.1.1.png)
![4.1.2](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.1.2.png)
#### 4）Anchored walk forward analysis，连续窗口最优参数训练期、测试期分析：
训练期最优参数：
End_Time |	17-11	| 17-12	| 18-01	| 18-02	| 18-03	| 18-04	| 18-05
-------- | :----: | :---: |-----: | :---: | :---: | :---: | :---:
Fast	   |    2   |   2   |   2   |    2  |   2   |  2    |  2
Slow	   |    16  |   16  |   17  |    16 |   16  |  17   |  17
测试期结果：
![4.3](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.3.png)
#### 5）Rolling walk forward analysis，滚动窗口最优参数训练期、测试期分析：
训练期最优参数：
End_Time |	17-11	| 17-12	| 18-01	| 18-02	| 18-03	| 18-04	| 18-05
-------- | :----: | :---: |-----: | :---: | :---: | :---: | :---:
Fast	   |    2   |   2   |   2   |    2  |   2   |  2    |  2
Slow	   |    16  |   16  |   17  |    16 |   16  |  17   |  16

![4.4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project3/4.4.png)
#### 6)Ralph Vince仓位管理，固定最大风险金额比例为 5%：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
224.84% |  116.82%  |   3.19 |   4.73%  |    436   | 52.33% 

![4.3.4](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.4.png)
![4.3.5](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.5.png)
![4.3.6](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project4/4.3.6.png)

#### 7）布林带交易策略，length = 20，distance = 1.03，手续费为万二：
累加收益 |	年化收益	| 夏普率	| 最大回撤	| 开仓次数	| 胜率
------- | :-------: | :----: |--------: | :------: | :-----:
94.15%  |  44.92%   |   2.37 |   12.75% |    915   | 56.67% 

![5.7](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.7.png)
![5.8](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.8.png)
![5.9](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/trading_system/project5/5.9.png)
