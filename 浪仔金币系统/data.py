# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取数据
df = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔系统_金币_充值\\17号充值.xlsx')
df_hb = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔系统_金币_充值\\红包17号盈利.xlsx')

# 转化时间格式
df['pay_time'] = pd.to_datetime(df['pay_time'])

# 按照时间排序
df_hb = df_hb.sort_values('时间')

# 重置索引
df_hb.reset_index(drop=True, inplace=True)

# 求出每个时段的 收入 & 支出
df_hb['时间1'] = df_hb['时间'].shift(1)
df_hb['支出'] = df_hb['系统支出'] - df_hb['系统支出'].shift(1)
df_hb['收入'] = df_hb['系统收入'] - df_hb['系统收入'].shift(1)

# 求出差值
df_hb['差'] = df_hb['收入'] - df_hb['支出']

# 删除第一行
df_hb = df_hb.drop([0])

# 取出有效列/重置索引/重命名
df_hb = df_hb[['时间1', '时间', '收入', '支出', '差']]
df_hb.reset_index(inplace=True)
df_hb.rename(columns={'时间': '时间2', 'index': '档位'}, inplace=True)

# print(df_hb.head())

# 判定时间档位
for y in range(df.shape[0]):
    y_t = df.loc[y, 'pay_time']

    for x in range(df_hb.shape[0]):
        if (y_t > df_hb.loc[x, '时间1']) and (y_t < df_hb.loc[x, '时间2']):
            df.loc[y, '档位'] = df_hb.loc[x, '档位']

# 最前和最后多出两个区间 - 删除
df = df[df['档位'].notnull()]

# 按档位求出充值人数
df_id = pd.DataFrame(df.groupby(['档位', 'player_id']).size())
df_id.reset_index(inplace=True)

# 合并三个序列 / 转置 / 重命名 / 重置索引
df_new = pd.DataFrame([df.groupby('档位').size(), df_id.groupby('档位').size(), df.groupby('档位')['amount'].sum()])
df_new = df_new.T
df_new.rename(columns={'Unnamed 1': '充值人数', 'Unnamed 0': '充值次数', 'amount': '充值金额'}, inplace=True)
df_new.reset_index(inplace=True)

# 合并【平台系统金币档位】- 【充值表】
df_hb = pd.merge(left=df_hb, right=df_new, on='档位', how='left')

# 导出数据
df_hb.to_excel('C:\\Users\Administrator\Desktop\浪仔系统_金币_充值1017.xlsx', index=False)
