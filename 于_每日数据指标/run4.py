# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np
from Func import du_excel, ri_y2, nian, yue

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

import datetime
today = datetime.date.today()
bef_yesterday = today - datetime.timedelta(days=2)

def run4():

    df = du_excel('红宝石')
    df2 = du_excel('红宝石明细')

    '----------------------计算第一个表----------------------------------------------------------'

    df = pd.pivot_table(df, values='数值', index='时间', columns='原因')
    df.reset_index(inplace=True)

    df = df[
        ['时间', '游戏产出', '新手礼包', '充值礼包', '成就任务', '分享抽奖', '玩家兑换红包', '玩家兑换话费', '玩家兑换金币', '幸运抽奖', '购买物品', '欢乐夺宝']]

    df = df[df['时间'] >= pd.to_datetime('{}'.format(bef_yesterday))]

    df['时间'] = df['时间'].apply(lambda x: str(x)[:10])

    '================================计算第二个表========================================='


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

        df2['一档比'] = (df2['第一档'] / df2['总和']).apply(lambda x: '%.2f%%' % (x*100))
        df2['二档比'] = (df2['第二档'] / df2['总和']).apply(lambda x: '%.2f%%' % (x*100))
        df2['三档比'] = (df2['第三档'] / df2['总和']).apply(lambda x: '%.2f%%' % (x*100))

        df2 = df2[['第一档', '第二档', '第三档', '一档比', '二档比', '三档比', '总和']]
        df2.reset_index(inplace=True)

        return df2


    df_ren = hongbaoshi_minxi(df2, '次数')

    df_money = hongbaoshi_minxi(df2, '总额')

    df2 = df_ren.append(df_money)

    df2 = df2[df2['日期'] >= pd.to_datetime('{}'.format(bef_yesterday))]
    df2['日期'] = df2['日期'].apply(lambda x: str(x)[:10])
    print('\n第四个表运行完毕……')

    return df, df2


if __name__ == '__main__':
    run4()


