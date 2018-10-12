# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取数据
df = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔充值用户数据_1012.xlsx')

df['未上线时间'] = df['登录时间'].apply(lambda x: str(pd.to_datetime('2018/10/12 23:59:59') - x).split(' ')[0])
df['未上线时间'].replace('NaT', '0', inplace=True)

df['未上线时间'] = df['未上线时间'].apply(lambda x: int(x))

df.loc[df['未上线时间'] > 5, '标记'] = 0
df.loc[df['未上线时间'] <= 5, '标记'] = 1

df.to_excel('C:\\Users\Administrator\Desktop\TTT.xlsx', index=False)
exit()

df = df.groupby(['充值日期', '区间'])['标记'].sum()
df = df.reset_index()

df.rename(columns={0: '遗留'}, inplace=True)

df = pd.pivot_table(df, values='标记', index='充值日期', columns='区间')

df = df.reset_index()
df.fillna(0, inplace=True)

df.to_excel('C:\\Users\Administrator\Desktop\浪仔充值区间分布_遗留版.xlsx', index=False)
