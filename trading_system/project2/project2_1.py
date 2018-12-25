# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import sys
import json
import numpy as np
import pandas as pd
import talib as ta
from gm.api import *

'''
本策略为中国人民大学财政金融学院量化交易系统课程作业
实现<Trading System>书中的日线相交策略Luxor
'''

def init(context):
    #MA快线与慢线
    context.fast = 10
    context.slow = 20
    context.frequency = "900s"
    # context.goods交易的品种
    context.symbol = 'SHFE.AU'
    context.fields = "high,low,close"
    context.period = context.slow + 1                              # 订阅数据滑窗长度
    
    # 订阅context.goods里面的品种, bar频率为15min
    subscribe(symbols=context.symbol,frequency=context.frequency,count=context.period,wait_group=True)

def on_bar(context, bars):    
    # 获取数据
    close_prices = context.data(symbol=context.symbol,frequency=context.frequency,
                          count=context.period,fields='close')
    trade_prices = context.data(symbol=context.symbol,frequency=context.frequency,
                          count=context.period,fields='high,low')
    # 计算长短周期均线
    fast_avg = ta.SMA(close_prices.values.reshape(context.period), context.fast)
    slow_avg = ta.SMA(close_prices.values.reshape(context.period), context.slow)
    
    # 均线下穿，做空
    if slow_avg[-2] < fast_avg[-2] and slow_avg[-1] >= fast_avg[-1]:
        SellStop = trade_prices['high'][context.slow-1] + 0.1
        SellLimit = trade_prices['high'][context.slow-1] + 0.5
      # 平多仓
        order_target_percent(symbol=context.symbol, percent=0, position_side=1, order_type=2)
      # 开空仓
        order_target_percent(symbol=context.symbol, percent=0.1, position_side=2,
                             order_type=OrderType_Limit, price=SellStop) 
    # 均线上穿，做多
    if fast_avg[-2] < slow_avg[-2] and fast_avg[-1] >= slow_avg[-1]:
        BuyStop = trade_prices['low'][context.slow-1] - 0.1
        BuyLimit = trade_prices['low'][context.slow-1] - 0.5
      # 平空仓
        order_target_percent(symbol=context.symbol, percent=0, position_side=2, order_type=2) 
      # 开多仓
        order_target_percent(symbol=context.symbol, percent=0.1, position_side=1,
                             order_type=OrderType_Limit, price=BuyStop) 
    
def on_backtest_finished(context, indicator):
    
    #以下用于在回测结束后保存回测指标
    indicator_data = {}
    indicator_data = indicator
    with open('F:/量化交易/交易系统练习二/'+str(context.fast)+'_'+str(context.slow)+'.json','w',encoding="utf-8") as json_file:
        json.dump(indicator_data, json_file)
    print("FAST %d - SLOW %d done!"%(context.fast,context.slow))

if __name__ == '__main__':
    '''
    strategy_id策略ID,由系统生成
    filename文件名,请与本文件名保持一致
    mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
    token绑定计算机的ID,可在系统设置-密钥管理中生成
    backtest_start_time回测开始时间
    backtest_end_time回测结束时间
    backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
    backtest_initial_cash回测初始资金
    backtest_commission_ratio回测佣金比例
    backtest_slippage_ratio回测滑点比例
    '''
    run(strategy_id='c7645ff3-f516-11e8-beec-3c970e853b38',
        filename='project2.1.py',
        mode=MODE_BACKTEST,
        token='8401315ba754693611d3bb99131e9cbc527c605f',
        backtest_start_time='2016-10-20 09:15:00',
        backtest_end_time='2018-11-24 15:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0005,
        backtest_slippage_ratio=0)#.0001)
    
