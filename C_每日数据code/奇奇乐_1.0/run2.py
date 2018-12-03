# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_old_excel

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings
from build.database import date, url2, url8

warnings.filterwarnings('ignore')

from Func import yesterday, bef_yesterday


def run2():
    df = date(url2)

    # 2018-11-27更新【前天注册新用户】
    df3 = date(url8)

    # 提取充值数据的日期
    df['day'] = df['pay_time'].apply(lambda x: pd.to_datetime(str(x).split(' ')[0]))

    # df和df2重新赋值
    df2 = df[df['day'] == pd.to_datetime(yesterday)]

    # 注册人数df
    df = df[df['day'] == pd.to_datetime(bef_yesterday)]


    # 整理前2天当日的注册数据
    df3['Flag'] = 'new'
    df3.rename(columns={'用户id': 'player_id'}, inplace=True)

    df3 = df3[['player_id', 'Flag']]

    df = pd.merge(left=df, right=df3, on='player_id', how='left')
    df['Flag'].fillna('old', inplace=True)

    df2 = pd.merge(left=df2, right=df3, on='player_id', how='left')
    df2['Flag'].fillna('old', inplace=True)


    i = 0
    df_form = pd.DataFrame()

    def df_f(df):
        df_form.loc[i, '日期'] = '{}'.format(bef_yesterday)

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


if __name__ == '__main__':
    df = run2()
