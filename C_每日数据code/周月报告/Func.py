# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import datetime
import os

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 格式是时间戳
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
day= datetime.datetime.now().strftime('%d')
hour = datetime.datetime.now().strftime('%H')
min = datetime.datetime.now().strftime('%M')


# 月报修改之处一 [月报的税收有问题，需要修改。]
y7=today - datetime.timedelta(days=14)
# y7=today - datetime.timedelta(days=30)



T_line = 35
def append_excel(file_path):
    df_all = pd.DataFrame()
    count = 0
    diff_file = []
    for x, y, z in os.walk(file_path):
        print('-' * T_line)
        print('文件夹中存在 {} 个文件.\n'.format(len(z)))
        for excel in z:
            file = x + '\\' + excel
            df = pd.read_excel(file)
            df_all = df_all.append(df, ignore_index=True)
            count += 1
            if count == 1:
                df_shape_start = df.shape[1]

            if df.shape[1] != df_shape_start:
                diff_file.append(excel)

    if df_shape_start == df_all.shape[1]:

        print('每个表格的列相同，且为{}列,数据合并完毕。'.format(df_shape_start))
        print('-' * T_line)
    else:
        print('表格{}的列不同，请检查！'.format(diff_file))
        print('-' * T_line)

    return df_all


def du_excel(sheet_name):
    try:
        # 读取数据
        # df = pd.read_excel('C:\\Users\Administrator\Desktop\\周报数据\\周报.xlsx', sheet_name=sheet_name)
        df = pd.read_excel('C:\\Users\Administrator\Desktop\\浪仔周报\\浪仔.xlsx', sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()




def du_old_excel(excel_name):
    try:
        # 读取数据  ==========月报修改之处2===============
        # df = pd.read_excel('C:\\Users\Administrator\Desktop\周报数据\\{}.xls'.format(excel_name))
        df = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔周报\{}.xls'.format(excel_name))
        # df = pd.read_excel('C:\\Users\Administrator\Desktop\月报数据\\{}.xls'.format(excel_name))
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


'-----------------Func内部调试运行----------------------------'

# if __name__ == '__main__':
#     append_excel()
