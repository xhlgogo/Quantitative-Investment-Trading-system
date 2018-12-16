# Quantitative-Investment-Trading-system
用于中国人民大学财政金融学院刘振亚教授的“金融计量与量化策略分析”与“量化投资交易策略分析与系统设计”两门课程的课程作业和笔记记录。

## 一、《PPT_4.Momentum Crashes.pdf》为“金融计量与量化策略分析”课程我所在的3人小组论文研讨报告，对动量崩溃Momentum Crash(见paper文件夹)做了小组论文研读报告。
### 0.其他论文研读报告为其他小组做的，不便上传，有需要请邮件联系我。
### 1.Momentum Strategies：业绩好的股票会继续保持其上涨的势头，业绩差的股票会保持其下跌的势头。每次调仓将股票按照前一段时间的累计收益率排序并分组，做多历史累计收益最高的那一组并做空历史累计收益最低的那一组。
### 2.Momentum Crashes：在市场萧条的熊市和震荡反弹的行情中，静态的动量交易策略收益会有明显下滑，出现负收益。
### 3.Dynamic Momentum Strategy：针对动量交易策略失效时的解决方案为构建动态权重的动量交易策略，基于原静态动量交易策略的均值和方差的预测，对原策略的Alpha和Sharpe Ratio有了近两倍的提高。

## 二、“量化投资交易策略分析与系统设计”课程作业
### 0.作业内容为实现\<trading system>中的量化交易系统
### 1.上海黄金期货主力合约净值曲线图
![净值曲线图](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/picture/SHFE.AU-%E5%87%80%E5%80%BC%E6%9B%B2%E7%BA%BF%E5%9B%BE.png)
### 2.上海黄金期货主力合约回撤比例柱状图
![回撤比例柱状图](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/picture/SHFE.AU-%E5%9B%9E%E6%B5%8B%E6%AF%94%E4%BE%8B%E6%9F%B1%E7%8A%B6%E5%9B%BE.png)
### 3.Luxor交易系统时间窗口优化图
![TimeFilter](https://github.com/xhlgogo/Quantitative-Investment-Trading-system/blob/master/picture/TimeFilter.png)

