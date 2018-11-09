# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('D:\MD_DATA\\0930数据_2\\2期对比.xlsx')

df = df.sort_values(by='期数')


i = 5
df1 = pd.DataFrame()
for x, y in df.groupby('渠道名'):
    y = y.reset_index(drop=True)

    for col in y.columns[1:]:
        y.loc[i, col] = y.loc[1, col] - y.loc[0, col]
        y.loc[i, '渠道名'] = '差值'

        y.loc[i + 1, col] = str(round(y.loc[i, col] / y.loc[0, col] * 100, 2))+'%'
        y.loc[i + 1, '渠道名'] = '增长比例'
    # print(y)
    # exit()

    df1 = df1.append(y, ignore_index=True)

df1.to_excel('C:\\Users\Administrator\Desktop\\result1.xlsx',index=False)
