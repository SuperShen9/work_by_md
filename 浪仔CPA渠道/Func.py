# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import datetime
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
bef_yesterday = today - datetime.timedelta(days=2)
hour = datetime.datetime.now().strftime('%H')

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


# 读取xlsx文件的时候用sheet写入
def du_excel(sheet_name):
    try:
        # 读取数据
        df = pd.read_excel('C:\\Users\Administrator\Desktop\\B_浪仔每日数据\\浪仔.xlsx', sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()

def du_old_excel(excel_name):
    try:
        # 读取数据
        df = pd.read_excel('C:\\Users\Administrator\Desktop\\浪仔CPA\\{}.xls'.format(excel_name))
        return df
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()


# 优化groupby之后的输出结果
def gb(df, gb_col, sum_col):
    df_m = df.groupby(gb_col)[sum_col].sum()
    df_m = pd.DataFrame(df_m)
    df_m.reset_index(inplace=True)
    df_m.sort_values(sum_col, ascending=0, inplace=True)
    df_m.reset_index(drop=True, inplace=True)
    return df_m

# 切割函数
def df_cut(df, gb_col, sum_col):

    df_m = gb(df, gb_col, sum_col)
    bins = [5, 100, 200, 500, 1000, 2000, 100000]
    df_c = pd.cut(df_m[sum_col], bins, right=False)
    df_c = pd.DataFrame(df_c)
    df_c = df_c.groupby(sum_col).size()
    return df_c


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
