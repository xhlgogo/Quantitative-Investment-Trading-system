# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import sys
import json
import numpy as np
import pandas as pd
import talib as ta
from gm.api import *

def init(context):
    #MA快线与慢线
    context.fast = 2
    context.slow = 20
    context.frequency = "900s"
    # context.goods交易的品种
    context.symbol = 'SHFE.AU'
    context.fields = "high,low,close"
    context.period = context.slow + 1                              # 订阅数据滑窗长度
    #TimeFilter优化
    context.date_window = ['09:15:00', '09:30:00', '09:45:00', '10:00:00', '10:15:00', '10:30:00', '10:45:00', 
            '11:00:00', '11:15:00', '11:30:00', '13:45:00', '14:00:00',
            '14:15:00', '14:30:00', '14:45:00', '15:00:00', '09:00:00']
    trade_window = [
      ['09:15:00', '09:30:00', '09:45:00', '10:00:00', '10:15:00', '10:30:00', '10:45:00', '11:00:00'],
      ['09:30:00', '09:45:00', '10:00:00', '10:15:00', '10:30:00', '10:45:00', '11:00:00', '11:15:00'],
      ['09:45:00', '10:00:00', '10:15:00', '10:30:00', '10:45:00', '11:00:00', '11:15:00', '11:30:00'],
      ['10:00:00', '10:15:00', '10:30:00', '10:45:00', '11:00:00', '11:15:00', '11:30:00', '13:45:00'],
      ['10:15:00', '10:30:00', '10:45:00', '11:00:00', '11:15:00', '11:30:00', '13:45:00', '14:00:00'],
      ['10:30:00', '10:45:00', '11:00:00', '11:15:00', '11:30:00', '13:45:00', '14:00:00', '14:15:00'],
      ['10:45:00', '11:00:00', '11:15:00', '11:30:00', '13:45:00', '14:00:00', '14:15:00', '14:30:00'],
      ['11:00:00', '11:15:00', '11:30:00', '13:45:00', '14:00:00', '14:15:00', '14:30:00', '14:45:00'],
      ['11:15:00', '11:30:00', '13:45:00', '14:00:00', '14:15:00', '14:30:00', '14:45:00', '15:00:00'],
      ['11:30:00', '13:45:00', '14:00:00', '14:15:00', '14:30:00', '14:45:00', '15:00:00', '09:15:00'],
      ['13:45:00', '14:00:00', '14:15:00', '14:30:00', '14:45:00', '15:00:00', '09:15:00', '09:30:00'],
      ['14:00:00', '14:15:00', '14:30:00', '14:45:00', '15:00:00', '09:15:00', '09:30:00', '09:45:00'],
      ['14:15:00', '14:30:00', '14:45:00', '15:00:00', '09:15:00', '09:30:00', '09:45:00', '10:00:00'],
      ['14:30:00', '14:45:00', '15:00:00', '09:15:00', '09:30:00', '09:45:00', '10:00:00', '10:15:00'],
      ['14:45:00', '15:00:00', '09:15:00', '09:30:00', '09:45:00', '10:00:00', '10:15:00', '10:30:00'],
      ['15:00:00', '09:15:00', '09:30:00', '09:45:00', '10:00:00', '10:15:00', '10:30:00', '10:45:00']]
    
    context.window_now = trade_window[1]
    
    # 订阅context.goods里面的品种, bar频率为15min
    subscribe(symbols=context.symbol,frequency=context.frequency,count=context.period,wait_group=True)

def on_bar(context, bars):
    
    date_now = str(context.now)
    #若当前时间在交易窗口内，则交易
    if date_now[-8:] in context.window_now:
      print(date_now[-8:])
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
          SellStop = trade_prices['low'][context.slow-1] - 0.1
          SellLimit = trade_prices['low'][context.slow-1] - 0.5
        # 平多仓
          order_target_percent(symbol=context.symbol, percent=0, position_side=1, order_type=2)
        # 开空仓
          order_target_percent(symbol=context.symbol, percent=0.1, position_side=2,
                              order_type=OrderType_Limit, price=SellStop) 
      # 均线上穿，做多
      if fast_avg[-2] < slow_avg[-2] and fast_avg[-1] >= slow_avg[-1]:
          BuyStop = trade_prices['high'][context.slow-1] + 0.1
          BuyLimit = trade_prices['high'][context.slow-1] + 0.5
        # 平空仓
          order_target_percent(symbol=context.symbol, percent=0, position_side=2, order_type=2) 
        # 开多仓
          order_target_percent(symbol=context.symbol, percent=0.1, position_side=1,
                              order_type=OrderType_Limit, price=BuyStop) 

def on_backtest_finished(context, indicator):
    
    #以下用于在回测结束后保存回测指标
    indicator_data = {}
    indicator_data = indicator
    temp = context.window_now[0]
    index = context.date_window.index(temp)
    temp = context.date_window[index-1]
    
    file_name = temp.replace(":",'_')
  
    with open('E:/Program Files/other/TimeFilter/'+file_name+'.json','w',encoding="utf-8") as json_file:
        json.dump(indicator_data, json_file)
    print("WINDOW %s done!"%(file_name))


if __name__ == '__main__':
    run(strategy_id='c7645ff3-f516-11e8-beec-3c970e853b38',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='8401315ba754693611d3bb99131e9cbc527c605f',
        backtest_start_time='2016-10-20 09:15:00',
        backtest_end_time='2018-11-24 15:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0)#.0001)
