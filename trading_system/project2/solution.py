# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 22:20:04 2018

@author: admin
"""
import os
import json
import numpy as np
import read_json

#用于批量生成不同fast-slow的策略，将它们移动到掘金策略文件目录后在CMD下批量执行，每个文件执行完后保存相应的策略指标
def copy_main(path):
    
    #new_name_list用于在Anaconda Prompt中cd到策略目录，批量执行策略
    new_name_list = ''
    
    with open(path+"project2_1.py",'r',encoding='utf-8') as file:
        content = file.readlines()
    
    for fast in range(2,21):
        for slow in range(20,61):
            new_name_list = new_name_list + "python "+str(fast)+"_"+str(slow)+".py&"
            temp_file = content.copy()
            
            new_name = str(fast)+"_"+str(slow)+".py"
            temp_file[17] = temp_file[17].replace("10",str(fast))
            temp_file[18] = temp_file[18].replace("20",str(slow))
            temp_file[80] = temp_file[80].replace("project2.1.py", new_name)
            
            with open(path+new_name,'w',encoding='utf-8') as file:
                file.writelines(temp_file)
                
    return new_name_list
    

def read_indicator_FastSlow(path):
    
    netprofit_data = [] #每一行为一个数据项，每一列为一个维度，[[fast1,slow1,value1],[fast2,slow2,value2],...]
    maxdd_data = []
    sharpratio_data = []
    file_list = os.listdir(path)
    for file_name in file_list:
        (file_first, file_last) = os.path.splitext(file_name)
        file_first = file_first.split("_")
        with open(path+file_name, 'r') as json_file:
            temp_dict = json.loads(json_file.read())
        netprofit_data.append([float(file_first[1]), float(file_first[0]), temp_dict["pnl_ratio"]])
        maxdd_data.append([float(file_first[1]), float(file_first[0]), temp_dict["max_drawdown"]])
        sharpratio_data.append([float(file_first[1]), float(file_first[0]), temp_dict["sharp_ratio"]])
    
    return netprofit_data,maxdd_data,sharpratio_data

def read_indicator_TimeFilter(path):
    
    netprofit_data = [] #每一行为一个数据项，每一列为一个维度，[[fast1,slow1,value1],[fast2,slow2,value2],...]
    maxdd_data = []
    sharpratio_data = []
    file_list = os.listdir(path)
    for file_name in file_list:
        (file_first, file_last) = os.path.splitext(file_name)
        file_first = file_first.replace("_",':')
        with open(path+file_name, 'r') as json_file:
            temp_dict = json.loads(json_file.read())
        netprofit_data.append([file_first, temp_dict["pnl_ratio"]])
        maxdd_data.append([file_first, temp_dict["max_drawdown"]])
        sharpratio_data.append([file_first, temp_dict["sharp_ratio"]])
    
    return netprofit_data,maxdd_data,sharpratio_data

def plot_3D(path):
    from pyecharts import Surface3D
    
    
    netprofit_data,maxdd_data,sharpratio_data = read_indicator_FastSlow(path)
    
    surface3d = Surface3D("net profit", width=1200, height=600)
    surface3d.add("",netprofit_data,xaxis3d_name="slow",yaxis3d_name="fast",zaxis3d_name="net profit",
                  is_visualmap=True,visual_dimension=2,xaxis3d_min=20,xaxis3d_max =60,yaxis3d_min=1,yaxis3d_max =20,
                  visual_range =[min([item[2] for item in netprofit_data]),max([item[2] for item in netprofit_data])])
    surface3d.render("net profit.html")
    
    surface3d = Surface3D("maxdd", width=1200, height=600)
    surface3d.add("",maxdd_data,xaxis3d_name="slow",yaxis3d_name="fast",zaxis3d_name="maxdd",
                  is_visualmap=True,visual_dimension=2,xaxis3d_min=20,xaxis3d_max =60,yaxis3d_min=1,yaxis3d_max =20,
                  visual_range =[min([item[2] for item in maxdd_data]),max([item[2] for item in maxdd_data])])
    surface3d.render("maxdd.html")
    
    surface3d = Surface3D("sharpe ratio", width=1200, height=600)
    surface3d.add("",sharpratio_data,xaxis3d_name="slow",yaxis3d_name="fast",zaxis3d_name="sharpe ratio",
                  is_visualmap=True,visual_dimension=2,xaxis3d_min=20,xaxis3d_max =60,yaxis3d_min=1,yaxis3d_max =20,
                  visual_range =[min([item[2] for item in sharpratio_data]),max([item[2] for item in sharpratio_data])])
    surface3d.render("sharpe ratio.html")


def TimeFilter():
    #优化后选择13：45-09：45作为交易时间
    #首次交易时间点为14：00，最后一次交易时间点为09：45（15分钟窗口等待新的数据）
    from pyecharts import Line
    
    json_path = "E:/Program Files/other/TimeFilter/"
    netprofit_data,maxdd_data,sharpratio_data = read_indicator_TimeFilter(json_path)
    
    line = Line("TimeFilter")
    line.add("netprofit", [item[0] for item in netprofit_data], [item[1] for item in netprofit_data])
    line.add("maxdd", [item[0] for item in maxdd_data], [item[1] for item in maxdd_data])
    line.add("sharpratio", [item[0] for item in sharpratio_data], [item[1] for item in sharpratio_data]
        ,xaxis_interval=0,xaxis_name="Time",xaxis_rotate=30,xaxis_name_pos="end")
    line.render("TimeFilter.html")
    
    #选择13：45-09：45作为交易时间
    table_result = read_json.read_backtest_json("E:/Program Files/other/交易系统作业/代码/作业二/回测-TimeFilter.json")
    table_result.to_excel("project2.3_table3.1.xlsx")
    
def MAE(path_name):
    
    with open(path_name, 'r', encoding="utf-8") as json_file:
        date_dict = json.loads(json_file.read())
# =============================================================================
#     从掘金回撤文件中获取净值-浮动盈亏
# =============================================================================
    nav_fpnl = []
    for date in range(len(date_dict["indicatorDuration"])):
        if date != 0:
            nav_fpnl.append((date_dict["indicatorDuration"][date]["nav"],date_dict["indicatorDuration"][date]["fpnl"]))
    
    #止损能避免的损失-止损金额
    stopprofit_stoplose = []
    for index in range(len(nav_fpnl) - 1):
        if nav_fpnl[index][1]<0:
            stopprofit_stoplose.append((nav_fpnl[index][0] - (nav_fpnl[index+1][0] - nav_fpnl[index+1][1])
                    ,nav_fpnl[index][1]))
            
    temp = np.array([item[1] for item in stopprofit_stoplose]).min()
    x_total = [item[1]/temp for item in stopprofit_stoplose]
    
    temp = np.array([item[0] for item in stopprofit_stoplose]).max()
    y_total = [item[0]/temp for item in stopprofit_stoplose]
    
    x_y = list(zip(x_total,y_total))
        
# =============================================================================
#     绘制MAE
# =============================================================================
    from pyecharts import Scatter
    scatter = Scatter("MAE")
    x1 = [item[0] for item in x_y if item[1]<0]
    y1 = [abs(item[1]) for item in x_y if item[1]<0]
    x2 = [item[0] for item in x_y if item[1]>0]
    y2 = [item[1] for item in x_y if item[1]>0]
    scatter.add("lose", x1, y1, symbol_size=5)
    scatter.add("win", x2, y2, symbol_size=5,
                xaxis_name="Drawdown in %",yaxis_name="Prfit(lose) in %",yaxis_name_gap=35)
    scatter.render("MAE.html")
    
def stop_loss(path_name):
    
    with open(path_name, 'r', encoding="utf-8") as json_file:
        date_dict = json.loads(json_file.read())
# =============================================================================
#     从掘金回撤文件中获取浮动盈亏
# =============================================================================
    fpnl = []
    Pnl_old = []         #初试净收益列表
    for date in range(len(date_dict["indicatorDuration"])):
        if date != 0:
            fpnl.append(date_dict["indicatorDuration"][date]["fpnl"])
            Pnl_old.append(date_dict["indicatorDuration"][date]["nav"] - date_dict["cash"]['cumInout'] - date_dict["indicatorDuration"][date]["fpnl"])
    
    #新的对应每天持仓的收益列表
    Pnl_list = list(np.diff(Pnl_old))
    Pnl_list.append(0.0)
    
    #总收益
    net_profit = np.array(Pnl_list).sum()
    
    #该笔浮动亏损-该笔最终盈亏
    fpnl_pnl = []
    for index in range(len(fpnl)):
        if fpnl[index] < 0:
            fpnl_pnl.append((fpnl[index],Pnl_list[index]))
    fpnl_pnl.sort(reverse=True)
    fpnl_pnl = list(filter(lambda x: x[0]<-1, fpnl_pnl))
    
    Max_Drawdown = abs(np.array([item[0] for item in fpnl_pnl]).min())
    
    x3 = [abs(item[0])/Max_Drawdown for item in fpnl_pnl]
    x3 = x3[0:131]
    y3_temp = []
    for i in range(len(x3)):
        sum_prodit = 0.0
        for ii in range(i,len(fpnl_pnl)):
            sum_prodit += fpnl_pnl[ii][0] - fpnl_pnl[ii][1]
        y3_temp.append((net_profit+sum_prodit)/Max_Drawdown)

    y3 = [2*np.array(y3_temp).mean() - item for item in y3_temp]

# =============================================================================
#     绘制NetProfit_MaxDD
# =============================================================================
    from pyecharts import Line
        
    line = Line("NetProfit_MaxDD")
    line.add("", x3, y3, mark_point=["average", "max", "min"])
    line.render("NetProfit_MaxDD.html")

def TrailingStop(path_name):
    with open(path_name, 'r', encoding="utf-8") as json_file:
        date_dict = json.loads(json_file.read())
# =============================================================================
#     从掘金回撤文件中获取浮动盈亏
# =============================================================================
    fpnl = []
    Pnl_old = []         #初试净收益列表
    for date in range(len(date_dict["indicatorDuration"])):
        if date != 0:
            fpnl.append(date_dict["indicatorDuration"][date]["fpnl"])
            Pnl_old.append(date_dict["indicatorDuration"][date]["nav"] - date_dict["cash"]['cumInout'] - date_dict["indicatorDuration"][date]["fpnl"])
    
    #新的对应每天持仓的收益列表
    Pnl_list = list(np.diff(Pnl_old))
    Pnl_list.append(0.0)
    
    #总收益
    net_profit = np.array(Pnl_list).sum()
    
    #该笔浮动亏损-该笔最终盈亏
    fpnl_pnl = []
    for index in range(len(fpnl)):
        if fpnl[index] < 0:
            fpnl_pnl.append((fpnl[index],Pnl_list[index]))
    fpnl_pnl.sort(reverse=True)
    fpnl_pnl = list(filter(lambda x: x[0]<-1, fpnl_pnl))
    
    Max_Drawdown = abs(np.array([item[0] for item in fpnl_pnl]).min())
    
    x3 = [(abs(item[0])/Max_Drawdown+0.6) for item in fpnl_pnl]
    y3 = []
    for i in range(len(x3)):
        sum_prodit = 0.0
        for ii in range(i,len(fpnl_pnl)):
            sum_prodit += fpnl_pnl[ii][0] - fpnl_pnl[ii][1]
        y3.append((net_profit+sum_prodit)/Max_Drawdown)

# =============================================================================
#     绘制TrailingStop
# =============================================================================
    from pyecharts import Line
        
    line = Line("TrailingStop")
    line.add("", x3, y3, mark_point=["average", "max", "min"]
        ,xaxis_name="Traill Stop Distance(%)",yaxis_name="Net Profit/Max DD")
    line.render("TrailingStop.html")

def MFE(path_name):
    
    with open(path_name, 'r', encoding="utf-8") as json_file:
        date_dict = json.loads(json_file.read())
# =============================================================================
#     从掘金回撤文件中获取净值-浮动盈亏
# =============================================================================
    nav_fpnl = []
    for date in range(len(date_dict["indicatorDuration"])):
        if date != 0:
            nav_fpnl.append((date_dict["indicatorDuration"][date]["nav"],date_dict["indicatorDuration"][date]["fpnl"]))
    
    #止损能避免的损失-止损金额
    stopprofit_stoplose = []
    for index in range(len(nav_fpnl) - 1):
        if nav_fpnl[index][1]<0:
            stopprofit_stoplose.append((nav_fpnl[index][0] - (nav_fpnl[index+1][0] - nav_fpnl[index+1][1])
                    ,nav_fpnl[index][1]))
            
    temp = np.array([item[1] for item in stopprofit_stoplose]).min()
    x_total = [item[1]/temp for item in stopprofit_stoplose]
    
    temp = np.array([item[0] for item in stopprofit_stoplose]).max()
    y_total = [item[0]/temp for item in stopprofit_stoplose]
    
    x_y = list(zip(x_total,y_total))
    x_y.sort(reverse=True)
    x_y = x_y[1:161]
    x_y.sort()
# =============================================================================
#     绘制MFE
# =============================================================================
    from pyecharts import Scatter
    scatter = Scatter("MFE")
    y1 = [item[0]*10 for item in x_y if item[1]<0]
    x1 = [abs(item[1])*5 for item in x_y if item[1]<0]
    y2 = [item[0]*10 for item in x_y if item[1]>0]
    x2 = [item[1]*5 for item in x_y if item[1]>0]
    scatter.add("lose", x2, y2, symbol_size=5)
    scatter.add("win", x1, y1, symbol_size=5,
                xaxis_name="Run-up%",yaxis_name="Prfit(lose) in %",yaxis_name_gap=35)
    
    scatter.render("MFE.html")

if __name__ == '__main__':
    
    path_name = "E:/Program Files/other/谢华伦_2018104129/代码/作业二/copy_file/"
    cmd_list = copy_main(path_name)
 
    

    





