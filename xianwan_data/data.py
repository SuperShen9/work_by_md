# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

def data():
    # 读取数据
    df_in = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\充值1008.xlsx')
    df_dui = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\兑奖1008.xlsx')
    df_reg = pd.read_excel('C:\\Users\Administrator\Desktop\\xianwan4\注册1008.xlsx')

    # 计算每个用户充值金额
    df1 = pd.DataFrame(df_in.groupby(['player_id', 'nickname'])['amount'].sum())
    df1.sort_values(by='amount', ascending=0, inplace=True)
    df1.reset_index(inplace=True)
    df1.rename(columns={'player_id': '用户id', 'amount': '充值金额', 'nickname': '昵称'}, inplace=True)

    # 计算每个用户兑换金额
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
    df_reg['新老用户'] = '新'
    df_reg = df_reg[['用户ID', '新老用户']]
    df_reg.rename(columns={'用户ID': '用户id'}, inplace=True)


    # 总表标记用老用户
    df123 = pd.merge(left=df12, right=df_reg, on='用户id', how='left')
    df123['新老用户'].fillna(value='老', inplace=True)

    return df123

# df123.to_excel('C:\\Users\Administrator\Desktop\T.xlsx',index=False)

