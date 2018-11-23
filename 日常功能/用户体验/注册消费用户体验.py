# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from build.database import url1, date, url7
from build.Func import or_path, gb

# # 导出数据
date(url7).to_excel(or_path('注册充值用户'))
date(url1).to_excel(or_path('变动日志'))

# # 读取充值新用户
df_reg = pd.read_excel(or_path('注册充值用户'))
df_reg = gb(df_reg, '用户id', '充值金额')
df_reg.rename(columns={'用户id': '用户ID'}, inplace=True)


# 读取变动日志

df = pd.read_excel(or_path('变动日志'))

# 数据分析
df['变动时间'] = df['变动时间'].apply(lambda x: pd.to_datetime(x))

df.sort_values('变动时间', inplace=True)

df = pd.DataFrame(df.groupby(['用户ID', '变动属性'])['差值'].sum())
df.reset_index(inplace=True)

df = pd.pivot_table(df, values='差值', index='用户ID', columns='变动属性')
df.reset_index(inplace=True)

df = df[['用户ID', '金币', '红宝石']]
df.fillna(0, inplace=True)

df['金币赢取'] = df['金币'] / 20000
df['宝石赚取'] = df['红宝石'] / 10
df['求和'] = df['金币赢取'] + df['宝石赚取']

df=pd.merge(left=df,right=df_reg,on='用户ID',how='left')
df=df[df['充值金额'].notnull()]

df.to_excel(or_path('用户行为'))

