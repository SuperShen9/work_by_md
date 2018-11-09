# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import gb, ri_y, nian, yue, df_cut, ri_y2

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

try:
    # 读取数据
    df = pd.read_excel('C:\\Users\Administrator\Desktop\奇奇乐新用户充值\\充{}.xlsx'.format(ri_y2))
    df2 = pd.read_excel('C:\\Users\Administrator\Desktop\奇奇乐新用户充值\\充{}.xlsx'.format(ri_y))
    df3 = pd.read_excel('C:\\Users\Administrator\Desktop\奇奇乐新用户充值\\注{}.xlsx'.format(ri_y2))
    df_lei = pd.read_excel('D:\MD_DATA\奇奇乐新用户叠加\\data.xlsx')
except FileNotFoundError:
    print('\n缺少运行数据，请先下载……')
    exit()

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
    df_form.loc[i, '平台'] = '奇奇乐'
    df_form.loc[i, '日期'] = '{}/{}/{}'.format(nian, yue, ri_y2)

    # 人数计算
    df_form.loc[i, '新用户量'] = len(df[df['Flag'] == 'new']['player_id'].unique())
    df_form.loc[i, '总用户量'] = len(df['player_id'].unique())
    df_form.loc[i, '新用户占比'] = '%.2f%%' % (df_form.loc[i, '新用户量'] / df_form.loc[i, '总用户量'] * 100)

    # 金额消费计算
    df_form.loc[i, '新用户消费'] = df[df['Flag'] == 'new']['amount'].sum()
    df_form.loc[i, '总消费'] = df['amount'].sum()
    df_form.loc[i, '新用户消费占比'] = '%.2f%%' % (df_form.loc[i, '新用户消费'] / df_form.loc[i, '总消费'] * 100)

    # 次日再消费人数
    df_form.loc[i, '次日再消费用户量'] = len(df2[df2['Flag'] == 'new']['player_id'].unique())
    df_form.loc[i, '次日再消费人数比'] = '%.2f%%' % (df_form.loc[i, '次日再消费用户量'] / df_form.loc[i, '新用户量'] * 100)

    # # 次日再消费金额计算
    # df_form.loc[i, '次日再消费金额'] = df2[df2['Flag'] == 'new']['amount'].sum()
    # df_form.loc[i, '次日再消费金额比'] = '%.2f%%' % (df_form.loc[i, '次日再消费金额'] / df_form.loc[i, '新用户消费'] * 100)

    return df_form


df_form = df_f(df)

# 删除多余2列
del df_form['总用户量']
del df_form['总消费']

# 调价到累加数据 / 去重
df_form = df_lei.append(df_form, ignore_index=True)
df_form.drop_duplicates(keep='last', inplace=True)

# 导出到桌面
df_form.to_excel('C:\\Users\Administrator\Desktop\\奇奇乐{}号新用户统计情况.xlsx'.format(ri_y2), index=False)
print('\n数据已导出到桌面……！')

# 数据存放累加数据
df_form.to_excel('D:\MD_DATA\奇奇乐新用户叠加\\data.xlsx', index=False)
print('\n数据已累加到 data ……\n')

print('{}月{}号奇奇乐【新注册用户】充值情况'.format(yue, ri_y2))
