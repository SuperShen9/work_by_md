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
    if x >= 20:
        if (x % 20) == 0:
            return x
        else:
            return x + 10
    else:
        return 20


df['次数'] = (df['数量'].apply(lambda x: int(fx(x))) / h2).apply(lambda x: int(x))

df['炮数'] = df['次数'] * p2
df['金币'] = df['炮数'] * 100

df['收入'] = df['次数'] * c2
df['收入'] = round(df['收入'].cumsum(), 2)

df['支出'] = df['广告主单价'].cumsum()

df['利润'] = round(df['收入'] - df['支出'], 2)

df['累加利润'] = round(df['利润'].cumsum(), 2)

df.to_excel('C:\\Users\Administrator\Desktop\闲玩4期_2档_new.xlsx', index=False)
