# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# # 读取2次导出的数据
# df = pd.read_excel('D:\MD_DATA\\1012数据\\27号之前.xlsx')
# df1 = pd.read_excel('D:\MD_DATA\\1012数据\\27号之后.xlsx')
#
# # 合二为一
# df = df.append(df1, ignore_index=True)
#
# # 取出有用的列
# df_reg = df[['用户ID', '注册时间', '登录时间']]
#
# # 充命名列用于合并
# df_reg.rename(columns={'用户ID': 'player_id'}, inplace=True)
#
# # 读取充值数据
# df = pd.read_excel('D:\MD_DATA\\1012数据\\浪仔充值数据.xlsx')
#
# # 合并注册时间和登入时间
# df = pd.merge(left=df, right=df_reg, on='player_id', how='left')

# df.to_excel('D:\MD_DATA\\1012数据\\data.xlsx', index=False)

'--------------------------------第二步：分布时间----------------------------'

# 读取数据
df = pd.read_excel('D:\MD_DATA\\1012数据\data.xlsx')

# 修改时间类型
df['注册时间'] = pd.to_datetime(df['注册时间'])
df['登录时间'] = pd.to_datetime(df['登录时间'])

# 添加时间差
df['时间差'] = df['登录时间'] - df['注册时间']

# 转置充值曲线
df_add = pd.DataFrame()
for x, y in df.groupby('player_id'):
    df_add = df_add.append(pd.DataFrame(y.groupby('player_id')['amount'].apply(lambda x: list(x.T))).reset_index(),
                           ignore_index=True)

# 再次合并df
df = pd.merge(left=df, right=df_add, on='player_id', how='left')

# 计算充值天数/金额
df['充值天数'] = df['amount_y'].apply(lambda x: len(x))
df['充值总金额'] = df['amount_y'].apply(lambda y: sum([int(x) for x in y]))

# 重命名列
df.rename(columns={'日期': '充值日期', 'player_id': '用户ID', 'nickname': '昵称', 'channel_number': '渠道', 'amount_x': '当日充值',
                   'amount_y': '充值曲线'}, inplace=True)

# 导出数据
df.to_excel('C:\\Users\Administrator\Desktop\浪仔充值用户数据_1012.xlsx', index=False)
