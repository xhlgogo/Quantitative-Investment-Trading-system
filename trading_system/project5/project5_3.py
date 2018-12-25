# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import sys
import json
import numpy as np
import pandas as pd
import talib as ta
from gm.api import *

def init(context):

    #context.avglen = 3                                # 布林均线周期参数
    context.disp = 20                                 # 布林平移参数
    #ontext.sdlen = 13                                # 布林标准差参数
    context.sdev = 1.03                                # 布林通道倍数参数

    context.frequency = "900s"
    # context.goods交易的品种
    context.symbol = 'SHFE.AU'
    context.fields = "high,low,close"
    context.period = context.disp + 1                              # 订阅数据滑窗长度
    #TimeFilter优化    
    #context.window_now = ['14:00:00', '09:45:00']

    # 订阅context.goods里面的品种, bar频率为frequency
    subscribe(symbols=context.symbol,frequency=context.frequency,count=context.period,wait_group=True)

def on_bar(context, bars):
    
    # 获取数据
    close_prices = context.data(symbol=context.symbol,frequency=context.frequency,
                            count=context.period,fields='close')
    trade_prices = context.data(symbol=context.symbol,frequency=context.frequency,
                            count=context.period,fields='high,low')
    last_price = close_prices['close'][context.disp-1]

    avgval = ta.MA(np.array(close_prices['close']), context.disp-13)         
    sdmult = ta.STDDEV(np.array(close_prices['close']), context.disp-3)*context.sdev
    #布林带上线
    disptop = avgval[context.disp-1] + sdmult[-1]
    #布林带下线
    dispup = avgval[context.disp-1] - sdmult[-1]

    #print("last_price: ",last_price, "avgval: ",avgval[context.disp-1],"disptop: ",disptop,"dispup",dispup)
    HigherBand = disptop
    LowerBand = dispup

    #获取账户持仓字典
    Account_positions = context.account().positions()
    #当前持仓方向
    if len(Account_positions)>0:
      position_side = Account_positions[0]['side']
    else:
      position_side = 0
    
    #上穿布林带上带且未持仓
    if trade_prices['high'][context.disp-1] > disptop and position_side==0:
      print(str(context.now),"做多")
      # 开多仓
      order_target_percent(symbol=context.symbol, percent=0.1, position_side=1,
                              order_type=OrderType_Limit, price=HigherBand)
    #下穿布林带均线且持多头仓
    if trade_prices['low'][context.disp-1] < avgval[context.disp-1] and position_side == 1:
      print(str(context.now),"平多")
      # 平多仓
      order_target_percent(symbol=context.symbol, percent=0, position_side=1, order_type=2)

    #下穿布林带下带且未持仓
    if trade_prices['low'][context.disp-1] < dispup and position_side==0:
      print(str(context.now),"做空")
      # 开空仓
      order_target_percent(symbol=context.symbol, percent=0.1, position_side=2,
                              order_type=OrderType_Limit, price=LowerBand)
    #上穿布林带均线且持空头仓
    if trade_prices['high'][context.disp-1] > avgval[context.disp-1] and position_side == 2:
      print(str(context.now),"平空")
      # 平空仓
      order_target_percent(symbol=context.symbol, percent=0, position_side=2, order_type=2)
    
"""     
def on_backtest_finished(context, indicator):
    
    #以下用于在回测结束后保存回测指标
    indicator_data = {}
    indicator_data = indicator
    file_name = '20_0_95'
  
    if indicator_data["sharp_ratio"]>0:
      with open('E:/Program Files/other/交易系统作业/代码/作业五/indicator/'+file_name+'.json','w',encoding="utf-8") as json_file:
        json.dump(indicator_data, json_file)
    
    print("WINDOW %s done!"%(file_name))
"""

if __name__ == '__main__':
    run(strategy_id='cc314c5e-0598-11e9-abd7-3c970e853b38',
        filename='project5_3.py',
        mode=MODE_BACKTEST,
        token='8401315ba754693611d3bb99131e9cbc527c605f',
        backtest_start_time='2016-10-20 09:15:00',
        backtest_end_time='2018-11-24 15:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0002,
        backtest_slippage_ratio=0)#.0001)
