# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import os
from Func import nian, yue, ri, ri_y, df_sum, df_t

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 切换到数据目录
filepath = 'C:\\Users\Administrator\Desktop\\xianwan4'
os.chdir(filepath)

# 读取文件并合并
for x, y, excels in os.walk(filepath):
    len_fk = len(excels)
    for name in ['充值', '兑奖', '宝石', '注册']:
        df = pd.DataFrame()
        for excel in excels:
            if excel.split('.')[0][-2:] == name:
                print('读取文件名称：{}'.format(excel))
                df1 = pd.read_excel(excel)
                df = df.append(df1, ignore_index=True)
        print('-'*50)
        df.to_excel('C:\\Users\Administrator\Desktop\\xianwan_合并\\{}{}{}.xlsx'.format(yue,ri_y,name),index=False)

def data():
    # 读取数据
    df_in = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan_合并\\{}{}充值.xlsx'.format(yue, ri_y))
    # df_in = df_t(df_in, 'pay_time')

    df_dui = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan_合并\\{}{}兑奖.xlsx'.format(yue, ri_y))
    # df_dui = df_t(df_dui, '兑换日期')

    df_reg = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan_合并\\{}{}注册.xlsx'.format(yue, ri_y))
    # df_reg = df_t(df_reg, '注册时间')

    # 计算每个用户充值金额
    print('充值金额：{}'.format(df_in['amount'].sum()))
    df1 = pd.DataFrame(df_in.groupby(['player_id', 'nickname'])['amount'].sum())
    df1.sort_values(by='amount', ascending=0, inplace=True)
    df1.reset_index(inplace=True)
    df1.rename(columns={'player_id': '用户id', 'amount': '充值金额', 'nickname': '昵称'}, inplace=True)

    # 计算每个用户兑换金额
    print('兑换奖励：{}'.format(df_dui['金额'].sum()))
    df2 = pd.DataFrame(df_dui.groupby(['用户id', '昵称'])['金额'].sum())
    df2.sort_values(by='金额', ascending=0, inplace=True)
    df2.reset_index(inplace=True)
    df2.rename(columns={'金额': '兑换金额'}, inplace=True)

    # 合并充值-兑换数据
    df12 = pd.merge(left=df1, right=df2, on='用户id', how='outer')
    df12.loc[df12['昵称_x'].isnull(), '昵称_x'] = df12['昵称_y']
    del df12['昵称_y']
    df12.rename(columns={'昵称_x': '昵称'}, inplace=True)
    df12.fillna(0, inplace=True)
    df12['单用户盈利'] = df12['充值金额'] - df12['兑换金额']
    df12.sort_values(by='单用户盈利', ascending=0, inplace=True)

    # 标记注册数据
    print('注册：{}'.format(df_reg.shape[0]))
    df_reg['新老用户'] = '新'
    df_reg = df_reg[['用户ID', '新老用户']]
    df_reg.rename(columns={'用户ID': '用户id'}, inplace=True)

    # 总表标记用老用户
    df123 = pd.merge(left=df12, right=df_reg, on='用户id', how='left')
    df123['新老用户'].fillna(value='老', inplace=True)

    return df123


# df123.to_excel('C:\\Users\Administrator\Desktop\T.xlsx',index=False)

'------------------------------读取宝石数据---------------------------------'

# 读取 【宝石-数字】 匹配数据
df_map = pd.read_excel('C:\\Users\Administrator\Desktop\\map.xlsx')
df_map = df_map[['reason', 'Flag_jew']]
df_map.dropna(inplace=True)

# 计算123dataframe
df123 = data()

# 读取宝石数据
df_jew = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan_合并\\{}{}宝石.xlsx'.format(yue, ri_y))
# df_jew = df_t(df_jew, 'gen_time')

# 标记reason属性
df_jew = pd.merge(left=df_jew, right=df_map, on='reason', how='left')

# 计算宝石累计
df = pd.DataFrame(df_jew.groupby(['player_id', 'Flag_jew'])['add_value'].sum())
df.reset_index(inplace=True)

# 新增变动列
df['具体变动'] = df['Flag_jew'] + ':' + df['add_value'].apply(lambda x: str(x))

# 计算道具变动情况
df_add = pd.DataFrame()
for x, y in df.groupby('player_id'):
    df_add = df_add.append(pd.DataFrame(y.groupby('player_id')['具体变动'].apply(lambda x: list(x.T))).reset_index(),
                           ignore_index=True)

df_add.rename(columns={'player_id': '用户id'}, inplace=True)

# 清理红宝石数据
df4 = pd.DataFrame(df_jew.groupby(['player_id'])['add_value'].sum())
df4.sort_values(by='add_value', ascending=0, inplace=True)
df4.reset_index(inplace=True)
df4.rename(columns={'player_id': '用户id', 'add_value': '累计红宝石产出'}, inplace=True)

# 合并红宝石产出
df1234 = pd.merge(left=df123, right=df4, on='用户id', how='left')

# 合并总体数据
df = pd.merge(left=df1234, right=df_add, on='用户id', how='left')

'-------------------------美化输出格式------------------------------------------'

# 筛选【盈利】部分，为了【总和】从新排序，为了横向合并重置索引，增加隔开列
df_a = df_sum(df[df['单用户盈利'] > 0])
df_a.sort_values(by='单用户盈利', ascending=0, inplace=True)
df_a.reset_index(drop=True, inplace=True)
df_a[' '] = ' '

# 筛选【持平】部分，为了【总和】从新排序，为了横向合并重置索引，增加隔开列
df_b = df_sum(df[df['单用户盈利'] == 0])
df_a.sort_values(by='单用户盈利', ascending=0, inplace=True)
df_b.reset_index(drop=True, inplace=True)


# 筛选【亏损】部分，为了【总和】从新排序，为了横向合并重置索引，增加隔开列
df_c = df_sum(df[df['单用户盈利'] < 0])
df_c.sort_values(by='单用户盈利', inplace=True)
df_c.reset_index(drop=True, inplace=True)
df_c[' '] = ' '

# 三个表横向合并
df3 = pd.concat([df_a, df_c], axis=1)
df3 = pd.concat([df3, df_b], axis=1)


# 输出数据
df3.to_excel('C:\\Users\Administrator\Desktop\\闲玩安卓{}天统计.xlsx'.format(int(ri)-8), index=False)
