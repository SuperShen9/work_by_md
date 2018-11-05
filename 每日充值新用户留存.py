# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import append_excel

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

# 【登入表】计算
df['time'] = df['login_time'].apply(lambda x: str(x)[:10])
print(df.head())


print(df_cz.head())
# print(df_zc.head())
