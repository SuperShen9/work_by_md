# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import datetime
import time

# 数据分析
df_new = pd.read_excel('C:\\Users\Administrator\Desktop\\new_reg\\1108.xls')
df_new['注册时间'] = df_new['注册时间'].apply(lambda x: x.split(' ')[0])

df_new['on'] = df_new['注册时间'] + '|' + df_new['用户ID'].apply(lambda x: str(x))
df_new['flag'] = 'new'

df_new = df_new[['on', 'flag']]

df = pd.read_hdf('C:\\Users\Administrator\Desktop\\new_reg\\data1108.h5', key='data')

# df = df.sample(5000)

df['time'] = df['变动时间'].apply(lambda x: x.split(' ')[0])

df = pd.DataFrame(df.groupby(['time', '用户ID', '游戏种类']).size())
df.reset_index(inplace=True)

df['on'] = df['time'] + '|' + df['用户ID'].apply(lambda x: str(x))

df = pd.merge(left=df, right=df_new, on='on', how='left')

# df = df[df['flag'].notnull()]
df = df[df['flag'].isnull()]

df = pd.DataFrame(df.groupby('time').apply(lambda x: pd.pivot_table(x, values=0, index='用户ID', columns='游戏种类')))
df = (df * 0 + 1).fillna(0)
df.reset_index(inplace=True)
df2=df.copy()

df=df.groupby('time').sum()

df.loc['求和'] = df.apply(lambda x: x.sum())
df.reset_index(inplace=True)
del df['用户ID']

writer = pd.ExcelWriter('C:\\Users\Administrator\Desktop\\奇奇乐新用户房间进入统计.xlsx')

df.to_excel(writer, sheet_name='日期汇总', index=False)

df2.to_excel(writer, sheet_name='详细数据', index=False)

writer.save()