# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

try:
    # 读取数据
    df = pd.read_excel('C:\\Users\Administrator\Desktop\每日数据分析\红宝石.xlsx')
    df2 = pd.read_excel('C:\\Users\Administrator\Desktop\每日数据分析\红宝石明细.xlsx')
except FileNotFoundError:
    print('\n缺少运行数据，请先下载……')
    exit()


# df = pd.pivot_table(df, values='数值', index='时间', columns='原因')
#
# df=df[['游戏产出','新手礼包','充值礼包','成就任务','分享抽奖','玩家兑换礼物','幸运抽奖','购买物品','欢乐夺宝']]
#
# df.to_excel('C:\\Users\Administrator\Desktop\表格提取源\红宝石分类.xlsx')


def fx(x):
    if x < 10:
        return '第一档'
    elif (x >= 10) and (x < 80):
        return '第二档'
    else:
        return '第三档'


df2['档位'] = df2['游戏产出红宝石（红包场）'].apply(lambda x: fx(x))


def hongbaoshi_minxi(df2, value):
    df2 = pd.pivot_table(df2, values=value, index='日期', columns='档位', aggfunc=np.sum)
    df2['总和'] = df2.apply(lambda x: x.sum(), axis=1)

    df2['一档比'] = (df2['第一档'] / df2['总和']).apply(lambda x: '%.2f%%' % x)
    df2['二档比'] = (df2['第二档'] / df2['总和']).apply(lambda x: '%.2f%%' % x)
    df2['三档比'] = (df2['第三档'] / df2['总和']).apply(lambda x: '%.2f%%' % x)

    df2 = df2[['第一档', '第二档', '第三档', '一档比', '二档比', '三档比', '总和']]

    return df2


df_ren = hongbaoshi_minxi(df2, '次数')

df_money = hongbaoshi_minxi(df2, '总额')

df2 = df_ren.append(df_money)

df2.to_excel('C:\\Users\Administrator\Desktop\表格提取源\红宝石明细.xlsx')

# print(df2)
