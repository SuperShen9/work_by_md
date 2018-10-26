# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_excel

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = du_excel('回收比')
df['time'] = df['时间'].apply(lambda x: str(x)[:10])

df = df.groupby('time').sum()

df['回收比'] = ((df['金币产出'] + df['红宝石产出'] * 2000) / df['金币消耗']).apply(lambda x: '%.2f%%' % (x * 100))

df.reset_index(inplace=True)

df.rename(columns={'time': '日期'}, inplace=True)

df.tail(2).to_excel('C:\\Users\Administrator\Desktop\表格提取源\回收比_OUT.xlsx',index=False)

# print(df)
