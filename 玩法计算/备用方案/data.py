# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

p1 = 776
p2 = 6984
p3 = 27160

h1 = 2
h2 = 20
h3 = 100

# c1 = 0.1104
# c2 = 1.104
# c3 = 3.968

c1 = 0.1104
c2 = 0.904
c3 = 1.768

df = pd.read_excel('C:\\Users\Administrator\Desktop\闲玩4期.xlsx')


def fx(x):
    if (x % 2) == 0:
        return x
    else:
        return x + 1


df['次数'] = (df['数量'].apply(lambda x: int(fx(x))) / h1).apply(lambda x: int(x))

df['炮数'] = df['次数'] * p1
df['金币'] = df['炮数'] * 100

df2 = df.copy()

df['收入'] = df['次数'] * c1
df['收入'] = round(df['收入'].cumsum(), 2)

df['支出'] = df['广告主单价'].cumsum()

df['利润'] = round(df['收入'] - df['支出'], 2)

df['累加利润'] = round(df['利润'].cumsum(), 2)

# df2['收入'] = df2['次数'] * c1*df2['人数']
# df2['支出'] = df2['广告主单价'].cumsum()*df2['人数']
# df2['利润'] = df2['收入'] - df2['支出']
#
# df2['累加利润'] = df2['利润'].cumsum()
# print(df2)


df.to_excel('C:\\Users\Administrator\Desktop\闲玩4期_1档_new.xlsx', index=False)


