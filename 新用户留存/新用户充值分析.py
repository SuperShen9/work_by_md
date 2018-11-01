# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import time

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取充值数据 / 注册数据
df = pd.read_excel('C:\\Users\Administrator\Desktop\奇奇乐_新用户_留存\充值数据\\20181031.xls')
df_new = pd.read_excel('C:\\Users\Administrator\Desktop\奇奇乐_新用户_留存\注册数据\\20181031.xls')
df_dr = pd.read_excel('C:\\Users\Administrator\Desktop\登入总数据.xlsx')

# 两个表建立用来merge的列（因为充值数据为多日，所以需要添加日期用于分辨出当初注册当初充值，排除当日注册以后充值）
df_new['用户ID'] = df_new['用户ID'].apply(lambda x: str(x)) + '|' + df_new['注册时间'].apply(lambda x: x[:10])
df['player_id'] = df['player_id'].apply(lambda x: str(x)) + '|' + df['pay_time'].apply(lambda x: x[:10])

# 注册数据标记flag 为 new，重命名列名用于on，取出merge的2列
df_new['flag'] = 'new'
df_new.rename(columns={'用户ID': 'player_id'}, inplace=True)
df_new = df_new[['player_id', 'flag']]

# 合并【充值数据】和【注册数据】
df = pd.merge(left=df, right=df_new, on='player_id', how='left')

# 创建建立留存的表
df_liu = df[df['flag'] == 'new'][['player_id', 'flag']]

# 被merge的数据需要去重
df_liu = df_liu.drop_duplicates(subset=['player_id'], keep='first')

df_liu['注册时间'] = df_liu['player_id'].apply(lambda x: x.split('|')[1])
df_liu['player_id'] = df_liu['player_id'].apply(lambda x: int(x.split('|')[0]))

# 合并【注册数据】和【登入数据】
df_dr = pd.merge(left=df_dr, right=df_liu, on='player_id', how='left')

# 筛选出符合要求的数据
df_dr = df_dr[df_dr['注册时间'].notnull()]
df_dr = df_dr[df_dr['登入时间'] != df_dr['注册时间']]


df_dr = pd.DataFrame(df_dr.groupby(['注册时间', '登入时间']).size())
df_dr.reset_index(inplace=True)
df_dr = pd.pivot_table(df_dr, values=0, index='注册时间', columns='登入时间').T

print(df_dr)
exit()
# df_dr.to_excel('C:\\Users\Administrator\Desktop\TTT.xlsx', index=False)


df['flag'].fillna('old', inplace=True)
df['time'] = df['pay_time'].apply(lambda x: x[:10])

df_ren = df.drop_duplicates(subset=['player_id'], keep='first')

df_ren = pd.DataFrame(df_ren.groupby(['time', 'flag']).size())

df_ren.reset_index(inplace=True)
df_ren = pd.pivot_table(df_ren, values=0, index='time', columns='flag')
df_ren.reset_index(inplace=True)
df_ren['all'] = df_ren['new'] + df_ren['old']
df_ren['new_per'] = df_ren['new'] / df_ren['all']

df_ren['time'] = df_ren['time'].apply(lambda x: pd.to_datetime(x))
df_ren.sort_values('time', ascending=1, inplace=True)

print(df_ren)
exit()

df_ren.to_excel('C:\\Users\Administrator\Desktop\TTT.xlsx', index=False)

# if __name__=='__main__':
#     run()
