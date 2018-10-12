# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('D:\MD_DATA\\1011数据\浪仔1001_1010充值.xlsx')

df['日期'] = df['pay_time'].apply(lambda x: x.split(' ')[0])
df['日期'] = pd.to_datetime(df['日期'])

df = df.groupby(['日期', 'player_id'])['amount'].sum()
df = df.reset_index()

df.sort_values(by='amount', ascending=0, inplace=True)


df_all = pd.DataFrame()
for x, y in df.groupby('日期'):
    y = y.head(7)
    y.reset_index(drop=True,inplace=True)


    df_all = pd.concat([df_all, y], axis=1)

print(df_all)

