###2020.05.12 修改

###如果可转债内容太少，单元格内容=="证监会核准批文"，跳出循环。

###if sg_date =="证监会核准批文":
###    break

###2020.08.24 修改

###如果可转债内容太少，单元格内容=="证监会核准/同意注册"，跳出循环。

###if sg_date =="证监会核准/同意注册":
###    break

import requests
from lxml import etree
import json
import pandas as pd
from datetime import datetime
import time

start = time.time()

def parse_ymd(s):#日期字符串转换为日期格式，便于计算
    year_s, mon_s, day_s = s.split("-")
    return datetime(int(year_s), int(mon_s), int(day_s)).date()

url = 'https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t=1583893701702'    
d = {'rp': '22','page':'1'}
r = requests.post(url, data=d)    
#获取可转债即时的数据，传给变量r
all_data = r.json()
#r为json格式数据，转换为可读的列表形式
#print(all_data)
contents = all_data['rows']


kzz =[] #存储申购可转债信息的列表
kzz_ss =[] #存储上市可转债信息的列表

for i in range(20):
	
    today_date = datetime.today().date()#今天的日期
    sg_date=contents[i]['cell']['progress_nm'][:10]#提取转债日期，字符类型
    if sg_date =="证监会核准/同意注册":
        break
    flag="申购"
    flag1="上市"
    #c=datetime.strptime(sg_date, "%Y-%m-%d").date()#转换为日期格式
    c=parse_ymd(sg_date)
    
    if (c-today_date).days>=0:
        if (flag in contents[i]['cell']['progress_nm']):
            #判断日期是否在今日日期之后，以及是否有“申购”字样
            sg_data_kzz = {
                    "申购日期":sg_date,
                    "可转债代码":contents[i]['cell']['bond_id']+"\n"+contents[i]['cell']['stock_id'],
                    "可转债名称":contents[i]['cell']['bond_nm']+"\n"+contents[i]['cell']['stock_nm']
    
            }
            #每一条可转债申购信息
            
            kzz.append(sg_data_kzz)#添加至申购可转债信息列表

        if (flag1 in contents[i]['cell']['progress_nm']):
                            #判断日期是否在今日日期之后，以及是否有“上市”字样
            ss_data_kzz = {
                    "上市日期":sg_date,
                    "可转债代码":contents[i]['cell']['bond_id']+"\n"+contents[i]['cell']['stock_id'],
                    "可转债名称":contents[i]['cell']['bond_nm']+"\n"+contents[i]['cell']['stock_nm']
    
            }
            #每一条可转债上市信息
            
            kzz_ss.append(ss_data_kzz)#添加至可转债上市信息列表

def pd_format(a,order):

    '''
    #a:list类型
    #order:排序的标签
    
    '''
    df=pd.DataFrame(a) #用pandas库生成一个对象kzz为list类型其中的每一个元素为字典类型
    df=df.sort_values(by=order) #按"申购日期"升序排列
    df=df.reset_index(drop=True) #重建索引

    return df
    


if kzz:#判断申购的是否为空
    if kzz_ss:#判断上市的是否为空
        
        df=pd.DataFrame(kzz)#用pandas库生成一个对象，kzz为list类型，其中的每一个元素为字典类型
        df=df.sort_values(by="申购日期")#按"申购日期"升序排列
        df=df.reset_index(drop=True)#重建索引

        df1=pd.DataFrame(kzz_ss)
        df1=df1.sort_values(by="上市日期")#按"上市日期"升序排列
        df1=df1.reset_index(drop=True)#重建索引

        new=pd.concat([df, df1], axis=1)
        new.to_csv('kzz.csv',encoding='utf-8-sig')#生成csv文件
    else:
        #没有上市的，只处理有申购的可转债
        df=pd_format(kzz,"申购日期")
        df.to_csv('kzz.csv',encoding='utf-8-sig')#生成csv文件
else:
    if kzz_ss: #没有申购的，只处理有上市的可转债       
        df1=pd.DataFrame(kzz_ss)
        df1=df1.sort_values(by="上市日期")#按"上市日期"升序排列
        df1=df1.reset_index(drop=True)#重建索引
        df1.to_csv('kzz.csv',encoding='utf-8-sig')#生成csv文件
    else:
        print("没有申购或者上市的可转债。")


end = time.time()

print('Total Time:' + str(end - start) + 's')



