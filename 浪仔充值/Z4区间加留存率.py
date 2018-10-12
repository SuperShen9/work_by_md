# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取数据
df = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔充值用户数据_1012.xlsx')

df['未上线时间'] = df['登录时间'].apply(lambda x: str(pd.to_datetime('2018/10/12') - x).split(' ')[0])
df['未上线时间'].replace('NaT', '0', inplace=True)

df['未上线时间'] =df['未上线时间'].apply(lambda x: int(x))



print(df.head())
exit()

df = df.groupby(['充值日期', '区间', 'Flag']).size()
df = df.reset_index()
df.sort_values('Flag', inplace=True)
df = df.reset_index(drop=True)
df.rename(columns={0: '人数'}, inplace=True)

df = pd.pivot_table(df, values='人数', index='充值日期', columns='区间')
df = df.reset_index()
df.fillna(0, inplace=True)

df.to_excel('C:\\Users\Administrator\Desktop\浪仔充值区间分布.xlsx', index=False)
