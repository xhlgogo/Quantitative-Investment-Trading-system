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
    context.slow = 16
    context.frequency = "900s"
    # context.goods交易的品种
    context.symbol = 'SHFE.AU'
    context.fields = "high,low,close"
    context.period = context.slow + 1                              # 订阅数据滑窗长度
    #TimeFilter优化    
    context.window_now = ['14:00:00', '09:45:00']

    context.maxdd = 0.0
    context.high_level = 1000000.
    
    context.delta = 100000.0
    context.add_position = 1
    
    # 订阅context.goods里面的品种, bar频率为frequency
    subscribe(symbols=context.symbol,frequency=context.frequency,count=context.period,wait_group=True)

def on_bar(context, bars):
    
    date_now = str(context.now)
    #若当前时间在交易窗口内，则交易
    if str(date_now[-8:]) >= str(context.window_now[0]) or str(date_now[-8:]) <= str(context.window_now[1]):
      #获取账户现金字典
      Account_cash = context.account().cash
      #获取账户持仓字典
      Account_positions = context.account().positions()
      
      #获取当前持仓方向
      if len(Account_positions)>0:
        position_side = Account_positions[0]['side']
      else:
        position_side = 0
      #获取当前持仓浮动盈亏
      if len(Account_positions)>0:
        position_fpnl = Account_positions[0]['fpnl']
      
      """
      #更新最高水准线
      context.high_level = max(context.high_level, Account_cash['nav'])
      #更新最大回撤
      context.maxdd = max(context.high_level - Account_cash['nav'], context.maxdd)
      
      if len(Account_positions)>0:
        Target_fixrisk = ((Account_cash['available']+Account_positions[0]['cost']*0.9)/Account_cash['nav'])*(0.02/0.2)
      else:
        Target_fixrisk = 0.1

      #当前调仓比例
      target_MaxDD = ((Account_cash['nav'] - Account_cash['nav']*0.1 - context.maxdd*1.5)/Account_cash['nav'])*0.1
      print(target_MaxDD, Target_fixrisk)
      """

      # 获取数据
      close_prices = context.data(symbol=context.symbol,frequency=context.frequency,
                            count=context.period,fields='close')
      trade_prices = context.data(symbol=context.symbol,frequency=context.frequency,
                            count=context.period,fields='high,low')
      last_price = close_prices['close'][context.slow-1]
      # 计算长短周期均线
      fast_avg = ta.SMA(close_prices.values.reshape(context.period), context.fast)
      slow_avg = ta.SMA(close_prices.values.reshape(context.period), context.slow)
      
      SellStop = trade_prices['low'][context.slow-1] - 0.1
      SellLimit = trade_prices['low'][context.slow-1] - 0.5
      BuyStop = trade_prices['high'][context.slow-1] + 0.1
      BuyLimit = trade_prices['high'][context.slow-1] + 0.5
      # 均线下穿，做空
      if slow_avg[-2] < fast_avg[-2] and slow_avg[-1] >= fast_avg[-1]:
        # 平多仓
          order_target_percent(symbol=context.symbol, percent=0, position_side=1, order_type=2)
        # 开空仓
          #order_target_percent(symbol=context.symbol, percent=Target_fixrisk, position_side=2,
          #                    order_type=OrderType_Limit, price=SellStop)
          order_target_percent(symbol=context.symbol, percent=0.1, position_side=2,
                              order_type=OrderType_Limit, price=SellStop) 
      # 均线上穿，做多
      if fast_avg[-2] < slow_avg[-2] and fast_avg[-1] >= slow_avg[-1]:
        # 平空仓
          order_target_percent(symbol=context.symbol, percent=0, position_side=2, order_type=2) 
        # 开多仓
          #order_target_percent(symbol=context.symbol, percent=Target_fixrisk, position_side=1,
          #                    order_type=OrderType_Limit, price=BuyStop)
          order_target_percent(symbol=context.symbol, percent=0.1, position_side=1,
                              order_type=OrderType_Limit, price=BuyStop)
      #无均线上穿或下穿，衡量是否加仓
      if not (slow_avg[-2] < fast_avg[-2] and slow_avg[-1] >= fast_avg[-1]) \
        and not (fast_avg[-2] < slow_avg[-2] and fast_avg[-1] >= slow_avg[-1]):
        if position_side!=0 and position_fpnl > context.delta*context.add_position:
          order_volume(symbol=context.symbol, volume=100, side=1, order_type=2 ,position_effect=1)
          #记录加仓，下次加仓时浮动盈亏要大一倍
          context.add_position = context.add_position + 1
          print("加仓: 浮动盈亏 %f"%position_fpnl)
      
"""
def on_backtest_finished(context, indicator):
    
    #以下用于在回测结束后保存回测指标
    indicator_data = {}
    indicator_data = indicator
    file_name = 'test_1'
  
    with open('E:/Program Files/other/交易系统作业/代码/作业四/'+file_name+'.json','w',encoding="utf-8") as json_file:
        json.dump(indicator_data, json_file)
    print("WINDOW %s done!"%(file_name))
"""

if __name__ == '__main__':
    run(strategy_id='c7645ff3-f516-11e8-beec-3c970e853b38',
        filename='project4_4.py',
        mode=MODE_BACKTEST,
        token='8401315ba754693611d3bb99131e9cbc527c605f',
        backtest_start_time='2016-10-20 09:15:00',
        backtest_end_time='2018-11-24 15:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0)#.0001)
