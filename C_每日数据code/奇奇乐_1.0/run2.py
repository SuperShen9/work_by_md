# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_old_excel
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import yesterday, bef_yesterday


def run2():

    df = du_old_excel('充值2天')
    df3 = du_old_excel('注册')

    # 提取充值数据的日期
    df['day'] = df['pay_time'].apply(lambda x: x.split(' ')[0].split('/')[2])

    # #监测第一步
    # df.to_excel('C:\\Users\Administrator\Desktop\\数据监测—step1.xlsx', index=False)
    # print(df.head())
    # exit()

    # df和df2重新赋值
    df2 = df[df['day'] == str(int(str(yesterday)[-2:]))]

    # 注册人数df
    df = df[df['day'] == str(int(str(bef_yesterday)[-2:]))]

    # 监测第二步
    # print(str(yesterday)[-2:])
    # print(df.head())
    # exit()

    # 整理前2天当日的注册数据
    df3['Flag'] = 'new'
    df3.rename(columns={'用户ID': 'player_id'}, inplace=True)
    df3 = df3[['player_id', 'Flag']]

    df = pd.merge(left=df, right=df3, on='player_id', how='left')
    df['Flag'].fillna('old', inplace=True)

    df2 = pd.merge(left=df2, right=df3, on='player_id', how='left')
    df2['Flag'].fillna('old', inplace=True)

    # df.to_excel('C:\\Users\Administrator\Desktop\\NEW_T.xlsx', index=False)
    # exit()

    i = 0
    df_form = pd.DataFrame()

    def df_f(df):
        # df_form.loc[i, '平台'] = '奇奇乐'
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
    print(df)
