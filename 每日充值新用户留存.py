# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import append_excel

# 读取每日登入用户并合并
df = append_excel('C:\\Users\Administrator\Desktop\数据合并')

df_cz = pd.read_excel('C:\\Users\Administrator\Desktop\充值.xls')
df_zc = pd.read_excel('C:\\Users\Administrator\Desktop\注册.xls')

# 【充值表】生成：去重列
df_cz['time'] = df_cz['pay_time'].apply(lambda x: str(x)[:10])
df_cz['on'] = df_cz['time'] + '|' + df_cz['player_id'].apply(lambda x: str(x))
# 充值表自我去重
df_cz = df_cz.drop_duplicates(subset=['on'], keep='first')

# 【注册表】生成：去重列
df_zc['time'] = df_zc['注册时间'].apply(lambda x: str(x)[:10])
df_zc['on'] = df_zc['time'] + '|' + df_zc['用户ID'].apply(lambda x: str(x))
df_zc['flag'] = 'new'
df_zc = df_zc[['on', 'flag']]

# 合并2个表
df_cz = pd.merge(left=df_cz, right=df_zc, on='on', how='left')
df_cz = df_cz[df_cz['flag'] == 'new']
df_cz = df_cz[['on', 'flag']]
df_cz['player_id'] = df_cz['on'].apply(lambda x: int(x.split('|')[1]))

df_cz['flag'] = df_cz['on'].apply(lambda x: x.split('|')[0])

# 【登入表】计算
df['time'] = df['login_time'].apply(lambda x: str(x)[:10])

# 合并【登入表】和【充值用户】
df = pd.merge(left=df, right=df_cz, on='player_id', how='left')

# gb数据用于透视
df = pd.DataFrame(df.groupby(['time','flag']).size())
df.reset_index(inplace=True)

# 做透视
df = pd.pivot_table(df, values=0, index='time', columns='flag')
df.reset_index(inplace=True)
df.rename(columns={''})


df.to_excel('C:\\Users\Administrator\Desktop\\text.xlsx')
