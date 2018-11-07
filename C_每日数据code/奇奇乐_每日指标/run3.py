# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import bef_yesterday, du_old_excel,du_excel

def run3():

    df = du_excel('金币分类')
    df_map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')

    # 修改不规则的列
    for x in range(df.shape[0]):
        if '鱼雷' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '玩家兑换鱼雷'

        elif '红宝石' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '玩家兑换红宝石'


    def change_col(x):
        if '鱼雷' in x:
            return int(x.split('(')[0])
        elif '红宝石' in x:
            return int(x.split('(')[0])
        else:
            return int(x)

    df['数值'] = df['数值'].apply(lambda x: change_col(str(x)))

    '-----------------系统赠送金币分类-----------------'

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
