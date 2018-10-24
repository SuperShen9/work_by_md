# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

try:
    # 读取数据
    df = pd.read_excel('C:\\Users\Administrator\Desktop\每日数据分析\奖品发放.xlsx')
except FileNotFoundError:
    print('\n缺少运行数据，请先下载……')
    exit()

df['奖励'] = df['金额'].apply(lambda x: str(x) + '元') + df['类型']

df['日期'] = df['兑换日期'].apply(lambda x: x[:10])

df = pd.DataFrame(df.groupby(['日期', '奖励']).size())
df.reset_index(inplace=True)

df = pd.pivot_table(df, values=0, index='日期', columns='奖励')

df = df[['2元红包', '5元红包', '8元红包', '10元红包', '10元话费', '100元话费']]
df.fillna(0,inplace=True)

df['总和'] = df.apply(lambda x: x.sum(), axis=1)


df.to_excel('C:\\Users\Administrator\Desktop\表格提取源\奖品发放.xlsx')