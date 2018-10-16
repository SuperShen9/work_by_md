# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('D:\MD_DATA\\1015数据\奇奇乐推广.xlsx')
df2 = pd.read_excel('D:\MD_DATA\\1015数据\浪仔推广.xlsx')


def fill1(df):
    # 转化时间序列
    df['关系建立时间'] = pd.to_datetime(df['关系建立时间'])
    # 切割时间(浪仔时间短，以浪仔为准)
    df = df[df['关系建立时间'] > pd.to_datetime('2018-09-11 17:41:20')]
    # 排序，重置索引
    df = df.sort_values('关系建立时间')
    df = df.reset_index(drop=True)

    # df['奖励一状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    # df['奖励二状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    # df['奖励三状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    return df


df = fill1(df)
df2 = fill1(df2)

df_s = pd.DataFrame()


def form(df, i):
    if i == 0:
        df_s.loc[i, '平台'] = '奇奇乐'
    else:
        df_s.loc[i, '平台'] = '浪仔'
    df_s.loc[i, '推广人数'] = df.drop_duplicates(subset=['推广玩家'], keep='first').shape[0]
    df_s.loc[i, '被推广人数'] = df.shape[0]
    df_s.loc[i, '奖励一完成人数'] = df['奖励一状态'].sum()
    df_s.loc[i, '奖励一完成比率'] = '%.0f%%' % (df_s.loc[i, '奖励一完成人数'] / df_s.loc[i, '被推广人数'] * 100)
    df_s.loc[i, '奖励二完成人数'] = df['奖励二状态'].sum()
    df_s.loc[i, '奖励二完成比率'] = '%.0f%%' % (df_s.loc[i, '奖励二完成人数'] / df_s.loc[i, '被推广人数'] * 100)
    df_s.loc[i, '奖励三完成人数'] = df['奖励三状态'].sum()
    df_s.loc[i, '奖励三完成比率'] = '%.0f%%' % (df_s.loc[i, '奖励三完成人数'] / df_s.loc[i, '被推广人数'] * 100)

    return df_s


df = form(df, 0)
df = form(df2, 1)

df.to_excel('C:\\Users\Administrator\Desktop\两平台推广情况.xlsx', index=False)
