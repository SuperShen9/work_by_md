# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('D:\MD_DATA\\0930数据_2\\2期对比.xlsx')

df = df.sort_values(by='期数')

del df['渠道id']
del df['ID']
del df['日期']

i = 500
df1 = pd.DataFrame()
for x, y in df.groupby('期数'):
    y = y.reset_index(drop=True)

    for col in y.columns[2:]:
        y.loc[i, col] = y[col].sum()
        y.loc[i, '期数'] = '总和'

        y.loc[i+1, col] = y[col].mean()
        y.loc[i+1, '期数'] = '平均值'

        # y.fillna(method='ffill', inplace=True)

    # print(y)
    # exit()

    df1 = df1.append(y, ignore_index=True)

# print(df1)
# exit()

df1.to_excel('C:\\Users\Administrator\Desktop\\周期对比.xlsx', index=False)
