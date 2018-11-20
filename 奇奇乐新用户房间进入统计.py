# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import datetime
import time

# 数据分析
df_reg=pd.read_excel('C:\\Users\Administrator\Desktop\\new_reg\\注册12-19.xls')
df_reg['注册时间']=df_reg['注册时间'].apply(lambda x: x.split(' ')[0])

df_reg['on']=df_reg['注册时间']+'|'+df_reg['用户ID'].apply(lambda x:str(x))
df_reg['flag']='new'

df_reg=df_reg[['on','flag']]
print(df_reg.head())
exit()





df = pd.read_hdf('C:\\Users\Administrator\Desktop\\new_reg\\data7.h5', key='data')

df = df.sample(5000)

df['time'] = df['变动时间'].apply(lambda x: x.split(' ')[0])

df = pd.DataFrame(df.groupby(['time', '用户ID', '游戏种类']).size())
df.reset_index(inplace=True)

# print(df)

df_all = pd.DataFrame()
for x, y in df.groupby('time'):
    df = pd.pivot_table(y, values=0, index='用户ID', columns='游戏种类')
    df = (df * 0 + 1).fillna(0)
    df['time'] = x

    df_all = df_all.append(df)

print(df_all)
exit()
