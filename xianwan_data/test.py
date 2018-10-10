# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


def df_sum(df):
    i = 10000
    df.loc[i, '用户id'] = '汇总：'
    df.loc[i, '昵称'] = df.shape[0]
    df.loc[i, '充值金额'] = df['充值金额'].sum()
    df.loc[i, '兑换金额'] = df['兑换金额'].sum()
    df.loc[i, '单用户盈利'] = df['单用户盈利'].sum()
    df.loc[i, '累计红宝石产出'] = df['累计红宝石产出'].sum()
    df = df.reset_index(drop=True)

    return df


df = pd.read_excel('C:\\Users\Administrator\Desktop\\out1009.xlsx')

df_a = df_sum(df[df['单用户盈利'] > 0])
df_a.sort_values(by='单用户盈利', ascending=0, inplace=True)
df_a.reset_index(drop=True, inplace=True)
df_a[' '] =' '

df_b = df_sum(df[df['单用户盈利'] == 0])
df_a.sort_values(by='单用户盈利', ascending=0, inplace=True)
df_b.reset_index(drop=True, inplace=True)
df_b[' '] =' '

df_c = df_sum(df[df['单用户盈利'] < 0])
df_c.sort_values(by='单用户盈利', inplace=True)
df_c.reset_index(drop=True, inplace=True)


# df3.loc[1, ' '] = ' '

df3 = pd.concat([df_a, df_b], axis=1)
df3 = pd.concat([df3, df_c], axis=1)

df3.to_excel('C:\\Users\Administrator\Desktop\\每日统计.xlsx', index=False)
