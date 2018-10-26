# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import gb, ri_y, nian, yue, df_cut, ri_y2

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

def run2():
    try:
        # 读取数据
        df = pd.read_excel('C:\\Users\Administrator\Desktop\每日数据分析\充值2天.xls'.format(ri_y))
        df3 = pd.read_excel('C:\\Users\Administrator\Desktop\每日数据分析\\注册.xls'.format(ri_y2))
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()

    # 提取日期
    df['day'] = df['pay_time'].apply(lambda x: x.split(' ')[0].split('/')[-1])

    # df和df2重新赋值
    df2 = df[df['day'] == ri_y]
    df = df[df['day'] == ri_y2]

    # 整理前2天当日的注册数据
    df3['Flag'] = 'new'
    df3.rename(columns={'用户ID': 'player_id'}, inplace=True)
    df3 = df3[['player_id', 'Flag']]

    df = pd.merge(left=df, right=df3, on='player_id', how='left')
    df['Flag'].fillna('old', inplace=True)

    df2 = pd.merge(left=df2, right=df3, on='player_id', how='left')
    df2['Flag'].fillna('old', inplace=True)

    # df.to_excel('C:\\Users\Administrator\Desktop\\NEW_T.xlsx', index=False)

    i = 0
    df_form = pd.DataFrame()

    def df_f(df):
        # df_form.loc[i, '平台'] = '奇奇乐'
        df_form.loc[i, '日期'] = '{}/{}/{}'.format(nian, yue, ri_y2)

        # 人数计算
        df_form.loc[i, '新用户量'] = len(df[df['Flag'] == 'new']['player_id'].unique())
        df_form.loc[i, '总用户量'] = len(df['player_id'].unique())
        df_form.loc[i, '新用户占比'] = '%.2f%%' % (df_form.loc[i, '新用户量'] / df_form.loc[i, '总用户量'] * 100)

        # 金额消费计算
        df_form.loc[i, '新用户消费金额'] = df[df['Flag'] == 'new']['amount'].sum()
        df_form.loc[i, '总消费'] = df['amount'].sum()
        df_form.loc[i, '新用户消费占比'] = '%.2f%%' % (df_form.loc[i, '新用户消费金额'] / df_form.loc[i, '总消费'] * 100)

        # 次日再消费人数
        df_form.loc[i, '次日再消费用户量'] = len(df2[df2['Flag'] == 'new']['player_id'].unique())
        df_form.loc[i, '次日再消费人数比'] = '%.2f%%' % (df_form.loc[i, '次日再消费用户量'] / df_form.loc[i, '新用户量'] * 100)

        # # 次日再消费金额计算
        df_form.loc[i, '次日再消费金额'] = df2[df2['Flag'] == 'new']['amount'].sum()
        df_form.loc[i, '次日再消费金额比'] = '%.2f%%' % (df_form.loc[i, '次日再消费金额'] / df_form.loc[i, '新用户消费金额'] * 100)

        return df_form


    df_form = df_f(df)


    # 删除多余2列
    del df_form['总用户量']
    del df_form['总消费']

    print('\n第二个表运行完毕……')
    return df_form




