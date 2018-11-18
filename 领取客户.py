# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\\变动日志.xls')

df['变动时间'] = df['变动时间'].apply(lambda x: pd.to_datetime(x))

df.sort_values('变动时间', inplace=True)

print(df)

f1 = pd.DataFrame()
count = 0

df1 = pd.DataFrame()
for x, y in df.groupby('用户ID'):
    y.reset_index(drop=True, inplace=True)
    # print(y.loc[0, '变动时间'])
    # print(y.loc[y.shape[0] - 1, '变动时间'])

    # list去重
    # print(y.groupby('用户ID')['变动原因'].apply(lambda x: list(set(list(x)))))
    # print(y.groupby('用户ID')['变动原因'].apply(lambda x: list(x)))

    yy=pd.DataFrame([y.groupby('用户ID')['变动原因'].apply(lambda x: list(set(list(x)))),y.groupby('用户ID')['变动原因'].apply(lambda x: list(x))]).T
    yy['开始时间']=y.loc[0, '变动时间']
    yy['结束时间'] = y.loc[y.shape[0] - 1, '变动时间']

    df1 = df1.append(yy)

# print(df1)

df1.to_excel('C:\\Users\Administrator\Desktop\\T1114.xlsx')
