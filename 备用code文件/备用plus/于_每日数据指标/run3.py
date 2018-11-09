# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import bef_yesterday

def run3():
    try:
        # 读取数据
        df = pd.read_excel('C:\\Users\Administrator\Desktop\每日数据分析\金币分类.xlsx')
        df_map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()

    df3 = df[df.columns[:3]]
    df3.dropna(axis=0, how='any', inplace=True)
    df3 = pd.pivot_table(df3, values='数值', index='时间', columns='原因')
    df3 = df3[['每日登录抽奖', 'VIP奖励', '新手礼包', '成就任务', '分享抽奖']]
    df3.reset_index(inplace=True)
    df3 = df3[df3['时间'] >= pd.to_datetime('{}'.format(bef_yesterday))]

    df3['时间'] = df3['时间'].apply(lambda x: str(x)[:10])

    '-----------------金币消耗汇总表--------------'

    # 金币消耗-透视
    df2 = df[df.columns[-3:]]
    df2.dropna(axis=0, how='any', inplace=True)
    df2 = pd.pivot_table(df2, values='数值2', index='时间2', columns='原因2')
    del df2['单局结算']
    df2.reset_index(inplace=True)
    df2['时间2'] = df2['时间2'].apply(lambda x: str(x)[:10])

    '----------------------------金币产出汇总表--------------------------'
    # 金币产出-透视
    df = df[df.columns[:3]]
    df_map = df_map[['原因', 'jinbi']]
    df_map.dropna(inplace=True)

    # 合并匹配表
    df = pd.merge(left=df, right=df_map, on='原因', how='left')

    df = df.groupby(['时间', 'jinbi'])['数值'].sum()

    df = pd.DataFrame(df)
    df.reset_index(inplace=True)

    df = pd.pivot_table(df, values='数值', index='时间', columns='jinbi')

    df.reset_index(inplace=True)

    df = df[['时间', '用户充值', '系统赠送', '兑换红宝石','兑换鱼雷', '领取邮件']]
    df['时间'] = df['时间'].apply(lambda x: str(x)[:10])

    print('\n第三个表运行完毕……')

    return df, df2, df3


if __name__ == '__main__':
    run3()
