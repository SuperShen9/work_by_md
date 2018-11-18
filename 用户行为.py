# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import warnings
from Func import gb

warnings.filterwarnings('ignore')

# df_c = pd.read_excel('C:\\Users\Administrator\Desktop\行为数据分析\充值15.xls')
# df_c = gb(df_c, 'player_id', 'amount')
# df_c.rename(columns={'player_id': '用户ID', 'amount': '充值'}, inplace=True)
#
#
# df = pd.read_excel('C:\\Users\Administrator\Desktop\\用户行为.xlsx')
#
# df = pd.merge(left=df, right=df_c, on='用户ID',how='left')
#
# df.to_excel('C:\\Users\Administrator\Desktop\\用户行为.xlsx', index=False)
#
# # print(df.head())
#
# exit()

df = pd.read_excel('C:\\Users\Administrator\Desktop\行为数据分析\变动日志15.xls')

df['变动时间'] = df['变动时间'].apply(lambda x: pd.to_datetime(x))

df.sort_values('变动时间', inplace=True)

f1 = pd.DataFrame()
count = 0
for x, y in df.groupby('用户ID'):
    y.reset_index(drop=True, inplace=True)

    f1.loc[count, '用户ID'] = y.loc[0, '用户ID']

    try:
        yy = y[(y['变动属性'] == '金币') & (y['游戏种类'] == '红包场')].reset_index(drop=True)
        f1.loc[count, '初始金币'] = yy.loc[0, '初始值']
    except KeyError:
        f1.loc[count, '初始金币'] = 0

    f1.loc[count, '红包场金币变动'] = y[(y['变动属性'] == '金币') & (y['游戏种类'] == '红包场')][' 差值（结束值-初始值）'].sum()
    f1.loc[count, '红包场红宝石变动'] = y[(y['变动属性'] == '红宝石') & (y['游戏种类'] == '红包场')][' 差值（结束值-初始值）'].sum()

    try:
        yy = y[(y['变动属性'] == '金币') & (y['游戏种类'] == '红包场')].reset_index(drop=True)
        f1.loc[count, '结束金币'] = yy.loc[yy.shape[0] - 1, '结束值']
    except KeyError:
        f1.loc[count, '结束金币'] = 0

    f1.loc[count, '兑换红宝石'] = y[(y['变动属性'] == '红宝石') & (y['游戏种类'] == '大厅')][' 差值（结束值-初始值）'].sum()

    count += 1

f1['金币赢取'] = f1['红包场金币变动'] / 20000
f1['宝石赚取'] = f1['红包场红宝石变动'] / 10
f1['求和'] = f1['金币赢取'] + f1['宝石赚取']

f1['盈亏回收比'] = (f1['宝石赚取'] / (f1['金币赢取'].apply(lambda x: -x)) * 100)

f1 = f1[f1['用户ID'] != '100149']

# f1['盈亏回收比'] = (f1['宝石赚取'] / (f1['金币赢取'].apply(lambda x:-x))*100).apply(lambda x: '%.0f%%' % x)

f1.to_excel('C:\\Users\Administrator\Desktop\\用户行为.xlsx', index=False)
