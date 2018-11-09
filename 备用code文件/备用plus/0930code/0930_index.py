# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('D:\MD_DATA\\0930数据_2\\2期对比.xlsx')

df['获客成本'] = round(df['推广费'] / df['注册用户数/月'], 2)
df['有效用户占比'] = round(df['有效用户数/月'] / df['注册用户数/月'], 2)
df['Arpu值'] = round(df['充值金额'] / df['付费用户数/月'], 2)

df = df.sort_values(by='期数')

del df['渠道id']
del df['ID']
del df['日期']

i = 5
df1 = pd.DataFrame()
for x, y in df.groupby('渠道名'):
    y = y.reset_index(drop=True)

    for col in y.columns[2:]:
        y.loc[i, col] = y.loc[1, col] - y.loc[0, col]
        y.loc[i, '期数'] = '差值'

        y.loc[i + 1, col] = str(round(y.loc[i, col] / y.loc[0, col] * 100, 2)) + '%'
        y.loc[i + 1, '期数'] = '差值比例'
        y.fillna(method='ffill', inplace=True)
    # print(y)
    # exit()

    df1 = df1.append(y, ignore_index=True)

df1.to_excel('C:\\Users\Administrator\Desktop\\result21.xlsx', index=False)
