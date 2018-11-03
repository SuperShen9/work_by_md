# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import du_old_excel
import datetime


def fx(x):
    nian = int(x.split('/')[0])
    yue = int(x.split('/')[1])
    ri = int(x.split('/')[2])

    return datetime.date(nian, yue, ri).isocalendar()[1] % 4

# 充值支付类型周对比
def run1():
    try:
        # 读取数据
        df = du_old_excel('充值')
        df_map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()

    df_map = df_map[['product_id', 'Flag']]

    df['time'] = df['pay_time'].apply(lambda x: x.split(' ')[0])

    df['week'] = df['time'].apply(lambda x: fx(x))

    # 合并匹配表
    df = pd.merge(left=df, right=df_map, on='product_id', how='left')

    df = pd.DataFrame(df.groupby(['Flag']).size())

    # 周报告
    # df = pd.DataFrame(df.groupby(['week', 'Flag']).size())

    df.reset_index(inplace=True)

    # df = pd.pivot_table(df, values=0, index='Flag', columns='week')

    df.sort_values(by=df.columns[-1], ascending=0, inplace=True)

    df.fillna(0, inplace=True)

    print(df)

    return df


# 奖品发放周对比
def run2():
    try:
        # 读取数据
        df = du_old_excel('奖品发放')
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()

    df['time'] = df['兑换日期'].apply(lambda x: x.split(' ')[0])

    df['week'] = df['time'].apply(lambda x: fx(x))

    print(df)
    exit()

    df = pd.DataFrame(df.groupby(['week', 'Flag']).size())

    df.reset_index(inplace=True)

    df = pd.pivot_table(df, values=0, index='Flag', columns='week')

    df.sort_values(by=df.columns[-1], ascending=0, inplace=True)

    df.fillna(0, inplace=True)

    return df

run1()