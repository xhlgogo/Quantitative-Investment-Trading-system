# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 21:17:14 2018

@author: xhlgogo
"""

import json
import numpy as np
import pandas as pd
from gm.api import *

def read_backtest_json(path_name):
# =============================================================================
# if __name__ == '__main__':
#     
#     path_name = "E:/Program Files/other/交易系统作业/代码/作业二/回测-TrailingStop.json"
# =============================================================================
# =============================================================================
#     获取交易所日历,读取回测文件,start
# =============================================================================
    start_time='2016-10-20'
    end_time='2018-11-24'
    set_token('8401315ba754693611d3bb99131e9cbc527c605f')
    calendar_list = get_trading_dates(exchange="SHFE", start_date=start_time, end_date=end_time) 
    
    with open(path_name, 'r', encoding="utf-8") as json_file:
        date_dict = json.loads(json_file.read())
# =============================================================================
#     获取交易所日历,读取回测文件,end
# =============================================================================
    
# =============================================================================
#     从掘金回撤文件中获取持仓方向、净收益、交易时间三个列表,start
# =============================================================================
    Position_list = []   #持仓方向列表
    Pnl_old = []         #初试净收益列表
    time_list = []
    for date in range(len(date_dict["indicatorDuration"])):
        if date == 0:
            Pnl_old.append(0.0)
            time_list.append(date_dict["indicatorDuration"][date]["createdAt"])
            if len(date_dict["indicatorDuration"][date]["positions"]) < 1:
                Pnl_old.append(0.0)
                Position_list.append(0)
            else:
                Position_list.append(date_dict["indicatorDuration"][0]["positions"][0]["side"])
        else:
            if len(date_dict["indicatorDuration"][date]["positions"]) < 1:
                continue
            positon = date_dict["indicatorDuration"][date]["positions"][0]["side"]
            pnl = date_dict["indicatorDuration"][date]["nav"] - date_dict["cash"]['cumInout'] - date_dict["indicatorDuration"][date]["fpnl"]
            if positon != Position_list[-1]:
                Position_list.append(positon)
                Pnl_old.append(pnl)
                time_list.append(date_dict["indicatorDuration"][date]["createdAt"])
    
    #新的对应每天持仓的收益列表
    Pnl_list = list(np.diff(Pnl_old))
    Pnl_list.append(0.0)
# =============================================================================
#     从掘金回撤文件中获取持仓方向、净收益、交易时间三个列表,end
# =============================================================================
      
    
# =============================================================================
#     <Trading Systems> page45, table3.1 计算,start
# =============================================================================
    table_result = pd.DataFrame(index = ["Total_Net_Profit","Gross_Profit","Gross_Loss","Profit_Factor","Total_Number_of_Trades",
        "Percent_Profitable","Winning_Trades","Losing_Trades","Avg_Trade_Net_Profit","Avg_Winning_Trade",
        "Avg_Losing_Trade","Ratio_Avg_Win:Avg_Loss","Largest_Winning_Trade","Largest_Losing_Trade",
        "Max_Consecutive_Winning_Trades","Max_Consecutive_Losing_Trades","Avg_Bars_in_Total_Trades",
        "Avg_Bars_in_Winning_Trades","Avg_Bars_in_Losing_Trades","Max_Drawdown"] ,
        columns=['All_Trades', 'Long_Trades', "Short_Trades"])
    table_result = table_result.fillna(0)

    #遍历持仓方向、净收益、交易时间三个列表，开始
    count_dic = {"win_long":0,"win_short":0,"lose_long":0,"lose_short":0,"win_total":0,"lose_total":0,
                 "maxdd_long":0,"maxdd_short":0,"maxdd_total":0}  #中间变量
    for date in range(len(Position_list)):        
        if Position_list[date] == 1:
            table_result["Long_Trades"]["Total_Net_Profit"] += Pnl_list[date]
            if Pnl_list[date] > 0:
                table_result["Long_Trades"]["Gross_Profit"] += Pnl_list[date]
                table_result["Long_Trades"]["Winning_Trades"] += 1
                table_result["Long_Trades"]["Largest_Winning_Trade"] = max(Pnl_list[date],
                       table_result["Long_Trades"]["Largest_Winning_Trade"])
                
                count_dic["win_long"] = 1 + count_dic["win_long"]   #连胜累加
                #判断当前连败是否为最大连败
                if count_dic["lose_long"] > table_result["Long_Trades"]["Max_Consecutive_Losing_Trades"]:
                    table_result["Long_Trades"]["Max_Consecutive_Losing_Trades"] = count_dic["lose_long"]
                count_dic["lose_long"] = 0   #由胜转败，清零
                
                if date != 0:              
                    table_result["Long_Trades"]["Avg_Bars_in_Winning_Trades"] += \
                    (calendar_list.index(time_list[date][:10])
                                                - calendar_list.index(time_list[date-1][:10]))
                
            else:
                table_result["Long_Trades"]["Gross_Loss"] -= Pnl_list[date]
                table_result["Long_Trades"]["Losing_Trades"] += 1
                table_result["Long_Trades"]["Largest_Losing_Trade"] = max((-1)*(Pnl_list[date]),
                       table_result["Long_Trades"]["Largest_Losing_Trade"])
                
                count_dic["lose_long"] = 1 + count_dic["lose_long"]   #连败累加
                #判断当前连胜是否为最大连胜
                if count_dic["win_long"] > table_result["Long_Trades"]["Max_Consecutive_Winning_Trades"]:
                    table_result["Long_Trades"]["Max_Consecutive_Winning_Trades"] = count_dic["win_long"]
                count_dic["win_long"] = 0    #由败转胜，清零
                
                if date != 0:               
                    table_result["Long_Trades"]["Avg_Bars_in_Losing_Trades"] += \
                    (calendar_list.index(time_list[date][:10])
                                                - calendar_list.index(time_list[date-1][:10]))
            #统计交易次数
            table_result["Long_Trades"]["Total_Number_of_Trades"] += 1
            #统计平均持有周期，先加总后面再除以交易次数
            if date != 0:              
                table_result["Long_Trades"]["Avg_Bars_in_Total_Trades"] += \
                (calendar_list.index(time_list[date][:10])
                                            - calendar_list.index(time_list[date-1][:10]))
            #统计最大回撤资金，将每次净收益乘取反相加，大于当前最大回撤则替换
            count_dic["maxdd_long"] += (-1)*Pnl_list[date]
            if count_dic["maxdd_long"] > table_result["Long_Trades"]["Max_Drawdown"]:
                table_result["Long_Trades"]["Max_Drawdown"] = count_dic["maxdd_long"]
            
                
        elif Position_list[date] == 2:
            table_result["Short_Trades"]["Total_Net_Profit"] += Pnl_list[date]
            if Pnl_list[date] > 0:
                table_result["Short_Trades"]["Gross_Profit"] += Pnl_list[date]
                table_result["Short_Trades"]["Winning_Trades"] += 1
                table_result["Short_Trades"]["Largest_Winning_Trade"] = max(Pnl_list[date],
                       table_result["Short_Trades"]["Largest_Winning_Trade"])
                
                count_dic["win_short"] = 1 + count_dic["win_short"]   #连胜累加
                #判断当前连败是否为最大连败
                if count_dic["lose_short"] > table_result["Long_Trades"]["Max_Consecutive_Losing_Trades"]:
                    table_result["Short_Trades"]["Max_Consecutive_Losing_Trades"] = count_dic["lose_short"]
                count_dic["lose_short"] = 0   #由胜转败，清零
                
                if date != 0:              
                    table_result["Short_Trades"]["Avg_Bars_in_Winning_Trades"] += \
                    (calendar_list.index(time_list[date][:10])
                                                - calendar_list.index(time_list[date-1][:10]))
                
            else:
                table_result["Short_Trades"]["Gross_Loss"] -= Pnl_list[date]
                table_result["Short_Trades"]["Losing_Trades"] += 1
                table_result["Short_Trades"]["Largest_Losing_Trade"] = max((-1)*(Pnl_list[date]),
                       table_result["Short_Trades"]["Largest_Losing_Trade"])
                
                count_dic["lose_short"] = 1 + count_dic["lose_short"]   #连败累加
                #判断当前连胜是否为最大连胜
                if count_dic["win_short"] > table_result["Long_Trades"]["Max_Consecutive_Winning_Trades"]:
                    table_result["Short_Trades"]["Max_Consecutive_Winning_Trades"] = count_dic["win_short"]
                count_dic["win_short"] = 0    #由败转胜，清零
                
                if date != 0:              
                    table_result["Short_Trades"]["Avg_Bars_in_Losing_Trades"] += \
                    (calendar_list.index(time_list[date][:10])
                                                - calendar_list.index(time_list[date-1][:10]))
            #统计交易次数    
            table_result["Short_Trades"]["Total_Number_of_Trades"] += 1
            #统计平均持有周期，先加总后面再除以交易次数
            if date != 0:              
                table_result["Short_Trades"]["Avg_Bars_in_Total_Trades"] += \
                (calendar_list.index(time_list[date][:10])
                                            - calendar_list.index(time_list[date-1][:10]))
            #统计最大回撤资金，将每次净收益乘取反相加，大于当前最大回撤则替换
            count_dic["maxdd_short"] += (-1)*Pnl_list[date]
            if count_dic["maxdd_short"] > table_result["Short_Trades"]["Max_Drawdown"]:
                table_result["Short_Trades"]["Max_Drawdown"] = count_dic["maxdd_short"]
        
        #统计总的最大回撤资金，将每次净收益乘取反相加，大于当前最大回撤则替换
        count_dic["maxdd_total"] += (-1)*Pnl_list[date]
        if count_dic["maxdd_total"] > table_result["All_Trades"]["Max_Drawdown"]:
            table_result["All_Trades"]["Max_Drawdown"] = count_dic["maxdd_total"]
            table_result.loc["Date_of_MaxDD"] = time_list[date][:10]
        
        #总的连胜、连败纪录，不考虑持仓方向，需排除盈利为0
        if Pnl_list[date] > 0:
            count_dic["win_total"] = 1 + count_dic["win_total"]   #连胜累加s
            if count_dic["lose_total"] > table_result["All_Trades"]["Max_Consecutive_Losing_Trades"]:
                table_result["All_Trades"]["Max_Consecutive_Losing_Trades"] = count_dic["lose_total"]
            count_dic["lose_total"] = 0    #由败转胜，清零
            
        elif Pnl_list[date] < 0:
            count_dic["lose_total"] = 1 + count_dic["lose_total"]   #连败累加
            if count_dic["win_total"] > table_result["All_Trades"]["Max_Consecutive_Winning_Trades"]:
                table_result["All_Trades"]["Max_Consecutive_Winning_Trades"] = count_dic["win_total"]
            count_dic["win_total"] = 0    #由败转胜，清零
    #遍历持仓方向、净收益、交易时间三个列表，结束
    
    for strname in ["Largest_Winning_Trade","Largest_Losing_Trade"]:
        table_result["All_Trades"][strname] = max(table_result["Long_Trades"][strname], table_result["Short_Trades"][strname])
    
    #重复计算可以循环
    add_list = ["Total_Net_Profit","Gross_Profit","Gross_Loss","Total_Number_of_Trades","Winning_Trades",
                "Losing_Trades","Avg_Bars_in_Total_Trades","Avg_Bars_in_Winning_Trades","Avg_Bars_in_Losing_Trades"]
    for strname in add_list:
        table_result["All_Trades"][strname] = table_result["Long_Trades"][strname] + table_result["Short_Trades"][strname]

    #重复计算可以循环
    div_list = [ ["Profit_Factor","Gross_Profit","Gross_Loss"],
                ["Percent_Profitable","Winning_Trades","Total_Number_of_Trades"],
                ["Avg_Trade_Net_Profit","Total_Net_Profit","Total_Number_of_Trades"],
                ["Avg_Winning_Trade","Gross_Profit","Winning_Trades"],
                ["Avg_Losing_Trade","Gross_Loss","Losing_Trades"],
                ["Ratio_Avg_Win:Avg_Loss","Avg_Winning_Trade","Avg_Losing_Trade"]]
    
    for strname in ["All_Trades","Long_Trades","Short_Trades"]:
        for div_name in div_list:
            table_result["All_Trades"][div_name[0]] = table_result["All_Trades"][div_name[1]] / table_result["All_Trades"][div_name[2]]
            table_result["Long_Trades"][div_name[0]] = table_result["Long_Trades"][div_name[1]] / table_result["Long_Trades"][div_name[2]]
            table_result["Short_Trades"][div_name[0]] = table_result["Short_Trades"][div_name[1]] / table_result["Short_Trades"][div_name[2]]
        table_result[strname]["Avg_Bars_in_Total_Trades"] = table_result[strname]["Avg_Bars_in_Total_Trades"] \
            / table_result[strname]["Total_Number_of_Trades"]
        table_result[strname]["Avg_Bars_in_Winning_Trades"] = table_result[strname]["Avg_Bars_in_Winning_Trades"] \
            / table_result[strname]["Winning_Trades"]
        table_result[strname]["Avg_Bars_in_Losing_Trades"] = table_result[strname]["Avg_Bars_in_Losing_Trades"] \
            / table_result[strname]["Losing_Trades"]
# =============================================================================
#     <Trading Systems> page45, table3.1 计算,end
# =============================================================================

# =============================================================================
#   表格格式化处理,涉及修改元素(类型)，需用中间变量,start
# =============================================================================
    form_list = ["Total_Net_Profit","Gross_Profit","Gross_Loss","Avg_Trade_Net_Profit","Avg_Winning_Trade",
                 "Avg_Losing_Trade","Largest_Winning_Trade","Largest_Losing_Trade","Max_Drawdown"]
    for strname in ["All_Trades","Long_Trades","Short_Trades"]:
        for form in form_list:
            temp = float(table_result[strname][form])
            table_result[strname][form]  = "￥"+str(round(temp))

    for strname in ["All_Trades","Long_Trades","Short_Trades"]:
        for form in ["Profit_Factor","Ratio_Avg_Win:Avg_Loss","Avg_Bars_in_Total_Trades",
                     "Avg_Bars_in_Winning_Trades","Avg_Bars_in_Losing_Trades"]:
            temp = float(table_result[strname][form])
            table_result[strname][form]  = round(temp,2)
            
    for strname in ["All_Trades","Long_Trades","Short_Trades"]:
        temp = float(table_result[strname]["Percent_Profitable"])*100
        table_result[strname]["Percent_Profitable"]  = str(round(temp,2))+"%"
        for form in ["Gross_Loss","Avg_Losing_Trade","Largest_Losing_Trade","Max_Drawdown"]:
            table_result[strname][form]  = "("+table_result[strname][form]+")"
    
    table_result["Long_Trades"]["Date_of_MaxDD"] = ''
    table_result["Short_Trades"]["Date_of_MaxDD"] = ''
# =============================================================================
#   表格格式化处理,涉及修改元素(类型)，需用中间变量,end
# =============================================================================
    return table_result

path_name = "E:/Program Files/other/谢华伦_2018104129/代码/作业二/"
json_list = ['回测_fast10_slow20_无手续费.json','回测_fast10_slow20_有手续费.json','回测_fast2_slow20.json'
             ,'回测-TimeFilter.json','回测-TrailingStop.json']
tabel_list = ['project2.1.a_table3.1.xlsx','project2.1.b_table3.1.xlsx','project2.2_table3.1.xlsx'
              ,'project2.3_table3.1.xlsx','project2.5_table3.1.xlsx']

for index in range(2):
    temp = read_backtest_json(path_name+json_list[index])
    temp.to_excel(tabel_list[index])

