# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np
import datetime

today = datetime.date.today()
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\\text.xlsx')

df_a = df[df.columns[1:]].fillna(0)
df_b = df[df.columns[1:]].shift(1).fillna(0)

df_c = (df_a - df_b) / df_b
df_c['登入时间'] = df['登入时间']

df_c = df_c[['登入时间'] + list(df_c.columns[:-1])]

df_c.replace(np.inf, np.nan, inplace=True)

print(df_c)
# df_c.to_excel('C:\\Users\Administrator\Desktop\\text2.xlsx')
exit()
