# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import datetime

hour = datetime.datetime.now().strftime('%H')

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from datetime import *

time1 = datetime.today()
nian = str(time1.year)
yue = str(time1.month)
ri_y = str(time1.day - 2)
ri = str(time1.day)

if len(yue) < 2:
    yue = '0' + yue
if len(ri_y) < 2:
    ri_y = '0' + ri_y
if len(ri) < 2:
    ri = '0' + ri


# 切割函数
def df_cut(df, gb_col, sum_col, title):
    df_m = gb(df, gb_col, sum_col)
    bins = [5, 100, 200, 500, 1000, 2000, 100000]
    df_c = pd.cut(df_m[sum_col], bins, right=False)
    df_c = pd.DataFrame(df_c)
    df_c = df_c.groupby(sum_col).size()
    df_c = pd.DataFrame(df_c)
    df_c.reset_index(inplace=True)
    df_c.rename(columns={0: title}, inplace=True)
    df_c.set_index('amount',inplace=True)
    return df_c


# 优化groupby之后的输出结果
def gb(df, gb_col, sum_col):
    df_m = df.groupby(gb_col)[sum_col].sum()
    df_m = pd.DataFrame(df_m)
    df_m.reset_index(inplace=True)
    df_m.sort_values(sum_col, ascending=0, inplace=True)
    df_m.reset_index(drop=True, inplace=True)
    return df_m


# 求和功能
def df_sum(df):
    i = 10000
    df.loc[i, '用户id'] = '汇总：'
    df.loc[i, '昵称'] = '{}人'.format(df.shape[0] - 1)
    df.loc[i, '充值金额'] = df['充值金额'].sum()
    df.loc[i, '兑换金额'] = df['兑换金额'].sum()
    df.loc[i, '单用户盈利'] = df['单用户盈利'].sum()
    df.loc[i, '累计红宝石产出'] = df['累计红宝石产出'].sum()
    df = df.reset_index(drop=True)

    return df


'-----------------------------切割时间功能------------------------------------------'


# 截取时间
def df_t(df_in, col):
    df_in[col] = pd.to_datetime(df_in[col])
    df_in = df_in[df_in[col] >= pd.to_datetime('2018-10-08 17:40:00')]
    return df_in


# 每份文件切割时间
def time_cut(day):
    df_in = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\\{}充值.xlsx'.format(day))
    df_in = df_t(df_in, 'pay_time')
    df_in.to_excel('C:\\Users\Administrator\Desktop\\被截取日期的数据\\{}充值.xlsx'.format(day), index=False)

    df_dui = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\\{}兑奖.xlsx'.format(day))
    df_dui = df_t(df_dui, '兑换日期')
    df_dui.to_excel('C:\\Users\Administrator\Desktop\\被截取日期的数据\\{}兑奖.xlsx'.format(day), index=False)

    df_reg = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\\{}注册.xlsx'.format(day))
    df_reg = df_t(df_reg, '注册时间')
    df_reg.to_excel('C:\\Users\Administrator\Desktop\\被截取日期的数据\\{}注册.xlsx'.format(day), index=False)

    df_jew = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\\{}红宝石.xlsx'.format(day))
    df_jew = df_t(df_jew, 'gen_time')
    df_jew.to_excel('C:\\Users\Administrator\Desktop\\被截取日期的数据\\{}红宝石.xlsx'.format(day), index=False)

# time_cut('1008')
