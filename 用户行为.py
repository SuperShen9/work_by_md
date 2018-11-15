# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\\变动日志.xls')

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

f1['盈亏回收比']=(f1['宝石赚取']/(f1['金币赢取'].apply(lambda x:-1))).apply(lambda x:'%.0f%%'%x)

f1.to_excel('C:\\Users\Administrator\Desktop\\用户行为.xlsx', index=False)

# =================备用===============
# 兑换红宝石
# print(y[(y['变动属性'] == '红宝石') & (y['游戏种类'] == '大厅')][' 差值（结束值-初始值）'].sum())

# 红包场红宝石变动
# print(y[(y['变动属性'] == '红宝石') & (y['游戏种类'] == '红包场')][' 差值（结束值-初始值）'].sum())

# 红包场金币变动
# print(y[(y['变动属性'] == '金币') & (y['游戏种类'] == '红包场')][' 差值（结束值-初始值）'].sum())

# 金币初始值，金币结束值
# print(y.loc[0, '初始值'], y.loc[y.shape[0] - 1, '结束值'])
