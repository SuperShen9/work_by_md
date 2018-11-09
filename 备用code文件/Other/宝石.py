# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from data import data, df_t

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df_map = pd.read_excel('C:\\Users\Administrator\Desktop\\map.xlsx')
df_map = df_map[['reason', 'Flag_jew']]
df_map.dropna(inplace=True)

df123 = data()

# 读取宝石数据
df_jew = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\\{}{}红宝石.xlsx'.format(yue, ri_y))
# df_jew = df_t(df_jew, 'gen_time')

# 标记reason属性
df_jew = pd.merge(left=df_jew, right=df_map, on='reason', how='left')

# print(df_jew.groupby(['player_id','Flag_jew'])['add_value'].sum())

# 计算宝石累计
df = pd.DataFrame(df_jew.groupby(['player_id', 'Flag_jew'])['add_value'].sum())
df.reset_index(inplace=True)

# 新增变动列
df['具体变动'] = df['Flag_jew'] + ':' + df['add_value'].apply(lambda x: str(x))

# 计算道具变动情况
df_add = pd.DataFrame()
for x, y in df.groupby('player_id'):
    df_add = df_add.append(pd.DataFrame(y.groupby('player_id')['具体变动'].apply(lambda x: list(x.T))).reset_index(), ignore_index=True)

df_add.rename(columns={'player_id': '用户id'}, inplace=True)

# 清理红宝石数据
df4 = pd.DataFrame(df_jew.groupby(['player_id'])['add_value'].sum())
df4.sort_values(by='add_value', ascending=0, inplace=True)
df4.reset_index(inplace=True)
df4.rename(columns={'player_id': '用户id', 'add_value': '累计红宝石产出'}, inplace=True)

# 合并红宝石产出
df1234 = pd.merge(left=df123, right=df4, on='用户id', how='left')

# 合并总体数据
df = pd.merge(left=df1234, right=df_add, on='用户id', how='left')


df.to_excel('C:\\Users\Administrator\Desktop\out1009.xlsx',index=False)
