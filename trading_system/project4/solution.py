# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 22:20:04 2018

@author: admin
"""
import json
from pyecharts import Line
from pyecharts import Bar
import read_json

def nav_line(path_name,figure_name):
    
    with open(path_name, 'r', encoding='utf-8') as json_file:
        temp_dict = json.loads(json_file.read())
    
    nav_list = []
    high_level = []
    time_list = []
    for date in range(len(temp_dict["indicatorDuration"])):
        nav_list.append(temp_dict["indicatorDuration"][date]["nav"])
        time_list.append(temp_dict["indicatorDuration"][date]["createdAt"][:10])
        if len(high_level)<1:
            high_level.append(nav_list[-1])
        else:
            high_level.append(max(nav_list[-1],high_level[-1]))
            
    line = Line(figure_name)
    line.add("净值线", time_list, nav_list)
    line.add("高水平线", time_list, high_level,xaxis_name="Time"
             ,xaxis_rotate=30, xaxis_interval=30,xaxis_name_pos="end")
    line.render(figure_name+".html")
    
def position_bar(path_name,figure_name):
    
    with open(path_name, 'r', encoding='utf-8') as json_file:
        date_dict = json.loads(json_file.read())
    
    postion_volume = []
    time_list = []
    for date in range(len(date_dict["indicatorDuration"])):
        #跳过没有持仓的日期
        if len(date_dict["indicatorDuration"][date]["positions"])<1:
            continue
        #添加做多仓位每日持仓，记为正值
        if date_dict["indicatorDuration"][date]["positions"][0]["side"]==1:
            postion_volume.append(date_dict["indicatorDuration"][date]["positions"][0]["volume"])
        #添加做空仓位每日持仓，记为负值
        elif date_dict["indicatorDuration"][date]["positions"][0]["side"]==2:
            postion_volume.append(-1*date_dict["indicatorDuration"][date]["positions"][0]["volume"])
        #添加持仓日期
        time_list.append(date_dict["indicatorDuration"][date]["createdAt"][:10])
    
    bar = Bar(figure_name)   
    bar.add("做多仓位", time_list, [postion_volume[index] if postion_volume[index]>0 else 0 for index in range(len(postion_volume))] )
    bar.add("做空仓位", time_list, [postion_volume[index] if postion_volume[index]<0 else 0 for index in range(len(postion_volume))]
            ,xaxis_name="Time",yaxis_name="Position",xaxis_rotate=30, xaxis_interval=30,xaxis_name_pos="end")
    bar.render(figure_name+".html")

if __name__ == '__main__':
    
    path_name = "E:/Program Files/other/交易系统作业/代码/作业四/回测-4.4.1.json"
    
    nav_line(path_name,"nav_delta_1千")
    position_bar(path_name,"position_delta_1千")
# =============================================================================
#     table = read_json.read_backtest_json(path_name)
#     table.to_excel("回测-4.4.2.xlsx")
# =============================================================================
