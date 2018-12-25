# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:52:10 2018

@author: xhlgogo
"""

#交易系统设计练习一
import pandas as pd
from gm.api import *

set_token('8401315ba754693611d3bb99131e9cbc527c605f')

gold_data_10min = history(symbol='SHFE.AU',frequency='600s',start_time='2016-11-01',end_time='2018-12-23')
gold_data_15min = history(symbol='SHFE.AU',frequency='900s',start_time='2016-11-01',end_time='2018-12-23')
gold_data_30min = history(symbol='SHFE.AU',frequency='1800s',start_time='2016-11-01',end_time='2018-12-23')
gold_data_1h = history(symbol='SHFE.AU',frequency='3600s',start_time='2016-11-01',end_time='2018-12-23')
gold_data_2h = history(symbol='SHFE.AU',frequency='7200s',start_time='2016-11-01',end_time='2018-12-23')

columns_name = ['amount','bob','close','eob','frequency','high','low','open','position','pre_close','symbol','volume']
Data_10min = pd.DataFrame(columns = columns_name,data = gold_data_10min)
Data_15min = pd.DataFrame(columns = columns_name,data = gold_data_15min)
Data_30min = pd.DataFrame(columns = columns_name,data = gold_data_30min)
Data_1h = pd.DataFrame(columns = columns_name,data = gold_data_1h)
Data_2h = pd.DataFrame(columns = columns_name,data = gold_data_2h)

Data_10min.to_excel('temp_黄金期货主力合约_10分钟.xlsx')
Data_15min.to_excel('temp_黄金期货主力合约_15分钟.xlsx')
Data_30min.to_excel('temp_黄金期货主力合约_30分钟.xlsx')
Data_1h.to_excel('temp_黄金期货主力合约_1小时.xlsx')
Data_2h.to_excel('temp_黄金期货主力合约_2小时.xlsx')