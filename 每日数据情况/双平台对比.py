# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import gb, ri_y, nian, yue, df_cut

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

try:
    # 读取数据
    df = pd.read_excel('C:\\Users\Administrator\Desktop\每日充值金额\\浪{}.xlsx'.format(ri_y))
    df2 = pd.read_excel('C:\\Users\Administrator\Desktop\每日充值金额\\奇{}.xlsx'.format(ri_y))
except FileNotFoundError:
    print('\n缺少运行数据，请先下载……')
    exit()

i = 0
df_form = pd.DataFrame()


def df_f(df):
    df_form.loc[i, '日期'] = '{}/{}/{}'.format(nian, yue, ri_y)
    if i == 0:
        df_form.loc[i, '平台'] = '浪仔'
    else:
        df_form.loc[i, '平台'] = '奇奇乐'

    df_form.loc[i, '充值总金额'] = df['amount'].sum()
    df_form.loc[i, '充值次数'] = df.shape[0]
    df_form.loc[i, '充值人数'] = len(df['player_id'].unique())

    df_m = gb(df, 'player_id', 'amount')
    df_m = df_m[df_m['amount'] >= 500]

    df_form.loc[i, '充值大户量'] = df_m.shape[0]

    df_form.loc[i, '大户充值排序'] = str(list(df_m['amount']))

    return df_form


df_form = df_f(df)
i = 1
df_form = df_f(df2)

'------------------切割比例 再形成表--------------------'
df_c = df_cut(df, 'player_id', 'amount')
df_c2 = df_cut(df2, 'player_id', 'amount')

df_c = pd.DataFrame([df_c, df_c2]).T
df_c.reset_index(inplace=True)
df_c.columns = ['充值区间', '浪仔', '奇奇乐']

df_form = pd.concat([df_form, df_c], axis=1)

print('\n{}月{}号双平台【区间充值】分布情况'.format(yue, ri_y))

df_form.to_excel('C:\\Users\Administrator\Desktop\双平台{}充值情况.xlsx'.format(ri_y), index=False)
