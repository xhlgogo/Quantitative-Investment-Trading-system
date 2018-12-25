import numpy as np
import json
import os
from pyecharts import Line
from pyecharts import Bar
import read_json

def copy_file(path_name):
    with open(path_name+"project5.py",'r',encoding='utf-8') as file:
        content = file.readlines()
    
    new_name_list = ''
    for disp in range(10,21):
        for sdev in np.arange(1.0,3.1,0.1):
            new_name_list = new_name_list + "python "+str(disp)+"_"+str(round(sdev,2)).replace('.','_')+".py&"
            temp_file = content.copy()
            
            new_name = str(disp)+"_"+str(round(sdev,2)).replace('.','_')
            temp_file[13] = temp_file[13].replace("16",str(disp))
            temp_file[15] = temp_file[15].replace("2.33",str(round(sdev,2)))
            temp_file[86] = temp_file[86].replace("use_this",new_name)
            temp_file[96] = temp_file[96].replace("main", new_name)
            
            with open(path_name+new_name+'.py','w',encoding='utf-8') as file:
                file.writelines(temp_file)

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
             ,xaxis_rotate=30, xaxis_interval=30,xaxis_name_pos="end",yaxis_min=1000000)
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
            ,xaxis_name="Time",yaxis_name="Position",xaxis_rotate=30, xaxis_interval=5,xaxis_name_pos="end")
    bar.render(figure_name+".html")
    
def length_distance(path_name):
    sharp_ratio = []
    pnl_ratio = []
    max_dd = []
    name_list = []
    
    file_list = os.listdir(path_name)
    for file_name in file_list:        
        with open(path_name+file_name, 'r', encoding='utf-8') as json_file:
            date_dict = json.loads(json_file.read())
            
        sharp_ratio.append(date_dict["sharp_ratio"])
        pnl_ratio.append(date_dict["pnl_ratio"])
        max_dd.append(date_dict["max_drawdown"])
        
        file = file_name.replace('.json','')    
        name_list.append(file[:2]+'_'+file[3:].replace('_','.'))
    
    line = Line("Bollinger Band 3")
    line.add("sharp_ratio", name_list, sharp_ratio, mark_point=["max"])
    line.add("pnl_ratio", name_list, [item for item in pnl_ratio])
    line.add("max_dd*10", name_list, [item*10 for item in max_dd],xaxis_name="length-distance"
             ,xaxis_rotate=90, xaxis_interval=0,xaxis_name_pos="end")
    line.render("Bollinger Band 3.html")


if __name__ == '__main__':
    
    path_name = "E:/Program Files/other/交易系统作业/代码/作业五/回测-5.3.json"
    nav_line(path_name,"Bollinger Band Nav3")
    position_bar(path_name,"Bollinger Band Position3")
    table = read_json.read_backtest_json(path_name)
    table.to_excel("回测-5.3.xlsx")
# =============================================================================
#     path_name = "E:/Program Files/other/交易系统作业/代码/作业五/indicator/"
#     length_distance(path_name)
# =============================================================================

# =============================================================================
#     with open(path_name+"project5.py",'r',encoding='utf-8') as file:
#         content = file.readlines()
#     
#     new_name_list = ''
#     for frequence in np.arange(0.5,24,0.5):
#         new_name_list = new_name_list + "python "+str(frequence).replace('.','_')+"hour"+".py&"
#         temp_file = content.copy()
#         
#         new_name = str(frequence).replace('.','_')+"hour"
#         temp_file[17] = temp_file[17].replace("7200s",str(int(frequence*60*60))+'s')
#         temp_file[86] = temp_file[86].replace("use_this",new_name)
#         temp_file[96] = temp_file[96].replace("main", new_name)
#         
#         with open(path_name+new_name+'.py','w',encoding='utf-8') as file:
#             file.writelines(temp_file)
# =============================================================================
    

 
    
