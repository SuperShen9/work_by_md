# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取数据库数据
df_c = pd.read_hdf('D:\MD_DATA\\data_base\qiqile_cz.h5', key='qiqi')
df_l = pd.read_excel('D:\MD_DATA\\data_base\浪仔充值.xlsx', key='lang')


# 自定义转置功能
def zhuan(df_c):
    df_m = df_c.groupby('player_id').size()
    df_m2 = df_c.groupby('player_id')['amount'].sum()
    df_m = pd.DataFrame([df_m, df_m2]).T
    df_m = df_m.reset_index()
    df_m.rename(columns={'Unnamed 0': '充值次数', 'amount': '充值金额'}, inplace=True)
    return df_m


# ----------- 数据转置----------------
df_m = zhuan(df_c)
df_m2 = zhuan(df_l)


def fill1(df):
    # 转化时间序列
    df['关系建立时间'] = pd.to_datetime(df['关系建立时间'])
    # 切割时间(浪仔时间短，以浪仔为准)
    df = df[df['关系建立时间'] > pd.to_datetime('2018-09-11 17:41:20')]
    # 排序，重置索引
    df = df.sort_values('关系建立时间')
    df = df.reset_index(drop=True)
    return df


# 读取推广数据
df = pd.read_excel('D:\MD_DATA\\1015数据\奇奇乐推广.xlsx')
df2 = pd.read_excel('D:\MD_DATA\\1015数据\浪仔推广.xlsx')

df = fill1(df)
df2 = fill1(df2)

i = 0


# 定义合并函数
def r_index(df, df_m):
    # 被推广玩家ID清洗
    df['被推广玩家ID'] = df['被推广玩家'].apply(lambda x: int(x.split('(')[0]))
    df.rename(columns={'被推广玩家ID': 'player_id'}, inplace=True)
    # 合并数据
    df = pd.merge(left=df, right=df_m, on='player_id', how='left')
    # 中间步骤检测数据
    df.to_excel('C:\\Users\Administrator\Desktop\TTT{}.xlsx'.format(i), index=False)
    # 重新标记完成/未完成
    df['奖励一状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    df['奖励二状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    df['奖励三状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    # 填充空白值
    df.fillna(0, inplace=True)
    # gb求出新的df
    c1 = df.groupby('奖励一状态')['充值金额'].sum()
    c2 = df.groupby('奖励二状态')['充值金额'].sum()
    c3 = df.groupby('奖励三状态')['充值金额'].sum()

    df_all = pd.DataFrame([c1, c2, c3]).T
    df_all = df_all.reset_index()
    df_all.columns = ['状态', '奖励一', '奖励二', '奖励三']

    return df_all


# 进行填充
df = r_index(df, df_m)
i += 1
df2 = r_index(df2, df_m2)

df = df.append(df2, ignore_index=True)

df.loc[0, '状态'] = '奇奇乐-未完成'
df.loc[1, '状态'] = '奇奇乐-完成'

df.loc[2, '状态'] = '浪仔-未完成'
df.loc[3, '状态'] = '浪仔-完成'

df.to_excel('C:\\Users\Administrator\Desktop\充值对比1015.xlsx', index=False)
