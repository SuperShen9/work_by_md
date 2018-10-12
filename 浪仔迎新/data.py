# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔迎新\全部充值.xlsx')

df_map = df[df['product_id'] == 21]
df_map = df_map[['player_id', 'amount']]
df_map.rename(columns={'amount': 'flag'}, inplace=True)
df_map['flag'] = 'new'

df = pd.DataFrame(df.groupby(['player_id', 'nickname'])['amount'].sum())
df.reset_index(inplace=True)
df.rename(columns={'nickname': '昵称', 'amount': '总充值'}, inplace=True)

df = pd.merge(left=df, right=df_map, on='player_id', how='left')

df_dui = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔迎新\全部兑换.xlsx')
df_dui = pd.DataFrame(df_dui.groupby(['用户id'])['金额'].sum())
df_dui.reset_index(inplace=True)
df_dui.rename(columns={'用户id': 'player_id', '金额': '总兑换金额'}, inplace=True)
# print(df_dui.head())
# exit()

df = pd.merge(left=df, right=df_dui, on='player_id', how='left')

# print(df.head())
# exit()

df_yx = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔迎新\迎新日志.xlsx')
df_yx = pd.DataFrame(df_yx.groupby('player_id')['add_value'].sum())
df_yx.reset_index(inplace=True)
df_yx['add_value'] = abs(df_yx['add_value']) / 10
df_yx.rename(columns={'add_value': '迎新兑换'}, inplace=True)

# print(df_yx.head())

df = pd.merge(left=df, right=df_yx, on='player_id', how='left')
df.fillna(0, inplace=True)

df['个人收益'] = df['总充值'] - df['总兑换金额']

df = df[['flag', 'player_id', '昵称', '总充值', '总兑换金额', '迎新兑换', '个人收益']]

df.to_excel('C:\\Users\Administrator\Desktop\\迎新数据.xlsx')

print(df.head())
exit()
