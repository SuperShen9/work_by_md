# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('D:\MD_DATA\\1011数据_2\浪仔全部充值.xlsx')

# 求出日期
df['日期'] = df['pay_time'].apply(lambda x: x.split(' ')[0])
df['日期'] = pd.to_datetime(df['日期'])

# 求出每天每个人的消费金额
df = df.groupby(['日期', 'player_id', 'nickname', 'channel_number'])['amount'].sum()
df = df.reset_index()

# 设置切割区间
bins = [5, 100, 200, 500, 1000, 2000, 100000]

# 切割金额[转化list从而得到Categories]
cats = pd.cut(list(df['amount']), bins, right=False)

# 区间赋值到df
df['区间'] = cats
df['Flag'] = cats.codes

# # 查看区间人数
# print(pd.value_counts(cats))

# # 按数字筛选区间
# print(df[df['Flag'] == 5])

df.to_excel('D:\MD_DATA\\1012数据\\浪仔充值数据.xlsx',index=False)
