# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 15:50:52 2018

@author: xhlgogo
"""

import numpy as np
import pandas as pd
from gm.api import *
from pyecharts import Line
from pyecharts import Bar

def handle_data(his_data):
    #市场对数相对回报
    his_data['strategy_ret'] = float(0)
    his_data.loc[1:,'strategy_ret'] = np.diff(np.log(his_data.close))
    
    #市场净值
    his_data['market_index'] = 1+np.cumsum(his_data['strategy_ret'])
    
    #最高净值,最大回撤时间
    his_data['highwaterlevel'] = float(0)
    his_data['maxdd_day'] = float(0)
    for i in his_data.index:
        if i == his_data.index[0]:
            his_data.loc[i,'highwaterlevel'] = 1.0
        else:
            his_data.loc[i,'highwaterlevel'] = np.maximum(his_data['highwaterlevel'][i-1],his_data['market_index'][i])
        
            if his_data['highwaterlevel'][i] > his_data['market_index'][i]:
                his_data.loc[i, 'maxdd_day'] = his_data['maxdd_day'][i-1] + 1
        
    #计算回撤比率
    his_data['drawdown_rate']  = (his_data['highwaterlevel'] - his_data['market_index']) / his_data['highwaterlevel'] 
 

def evaluation(his_data,timescale):
    ret         = his_data.strategy_ret
#计算平均回报率
    mean_ret    = np.mean(ret)
#计算风险（标准差）
    std_ret     = np.std(ret)
#计算夏普率
    sr          = mean_ret*np.sqrt(timescale)/std_ret
#计算收益
    ar          = timescale*mean_ret
#计算最大回撤率
    maxdd_rate  = np.max(his_data.drawdown_rate)
#计算最大回撤期(从最大回撤到回到无回撤的时间)
    maxdd_day =  np.max(his_data.maxdd_day)
            
    return sr,ar,maxdd_rate,maxdd_day  


def plot_with_pyecharts(his_data):
    """
       以下使用pyecharts绘制净值收益曲线图
    """    
    line = Line("SHFE.AU-净值曲线图")
    line.add("SHFE.AU-市场净值", pd.Series(his_data['bob']).astype(str)
        , his_data['market_index'], yaxis_min = 1)
    line.add("SHFE.AU-最大净值", pd.Series(his_data['bob']).astype(str)
        , his_data['highwaterlevel'], yaxis_min = 1)
    line.render("黄金期货主力合约-净值曲线图.html")
    
    bar = Bar("SHFE.AU-回测比例柱状图")
    bar.add("SHFE.AU-回测比例", pd.Series(his_data['bob']).astype(str),
            his_data['drawdown_rate'])
    bar.render("黄金期货主力合约-回测比例柱状图.html")
    
    
if __name__ == '__main__':
    
    set_token('8401315ba754693611d3bb99131e9cbc527c605f')
    symbol = 'SHFE.AU'
    frequen = '1d'
    starttime = '2016-01-01'
    endtime = '2018-11-24'
    gold_data_1day = history(symbol, frequency=frequen, start_time=starttime, end_time=endtime, skip_suspended=True, adjust=1, df=True)
    
    #将获取的list数据转为DataFrame类型
    columns_name = ['amount','bob','close','eob','frequency','high','low','open','position','pre_close','symbol','volume']
    his_data = pd.DataFrame(columns = columns_name,data = gold_data_1day)
    
    #计算对数回报、净值、回撤和回撤时间
    handle_data(his_data)
    #调用pyecharts绘制净值曲线图和最大回撤比例图，为html文件
    plot_with_pyecharts(his_data)
    #夏普比率、计算年化收益率、最大回撤率和最大回撤期
    SR, AR, MaxDD_rate, MaxDD_time = evaluation(his_data,252)
    print(SR, AR, MaxDD_rate, MaxDD_time)
    
    

