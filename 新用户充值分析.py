# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import time

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\新用户数据分析\充值29.xls')
df_new = pd.read_excel('C:\\Users\Administrator\Desktop\新用户数据分析\注册.xls')

df_new['用户ID'] = df_new['用户ID'].apply(lambda x: str(x)) + df_new['注册时间'].apply(lambda x: x[:10])
df['player_id'] = df['player_id'].apply(lambda x: str(x)) + df['pay_time'].apply(lambda x: x[:10])

df_new['flag'] = 'new'
df_new.rename(columns={'用户ID': 'player_id'}, inplace=True)
df_new = df_new[['player_id', 'flag']]

df = pd.merge(left=df, right=df_new, on='player_id', how='left')

df.to_excel('C:\\Users\Administrator\Desktop\TTT.xlsx', index=False)
exit()

df['flag'].fillna('old', inplace=True)
df['time'] = df['pay_time'].apply(lambda x: x[:10])

df_ren = df.drop_duplicates(subset=['player_id'], keep='first')

df_ren = pd.DataFrame(df_ren.groupby(['time', 'flag']).size())

df_ren.reset_index(inplace=True)
df_ren = pd.pivot_table(df_ren, values=0, index='time', columns='flag')
df_ren.reset_index(inplace=True)
df_ren['all'] = df_ren['new'] + df_ren['old']
df_ren['new_per'] = df_ren['new'] / df_ren['all']

# print(df_ren)
# exit()

df_ren.to_excel('C:\\Users\Administrator\Desktop\TTT.xlsx', index=False)

# if __name__=='__main__':
#     run()
