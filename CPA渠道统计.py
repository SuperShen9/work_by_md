# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import or_path, gb

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df_pay = pd.read_excel(or_path + '充值.xls')

df_reg = pd.read_excel(or_path + '注册.xls')

# 【充值表】生成：去重列
df_pay['time'] = df_pay['pay_time'].apply(lambda x: str(x)[:10])
df_pay['on'] = df_pay['time'] + '|' + df_pay['player_id'].apply(lambda x: str(x))

# 【注册表】生成：去重列
df_reg['time'] = df_reg['注册时间'].apply(lambda x: str(x)[:10])
df_reg['on'] = df_reg['time'] + '|' + df_reg['用户ID'].apply(lambda x: str(x))
df_reg['flag'] = 'new'
df_reg = df_reg[['on', 'flag']]

df_pay = pd.merge(left=df_pay, right=df_reg, on='on', how='left')

df_pay = df_pay[(df_pay['flag'].notnull()) & (df_pay['channel'] == 800106)]

df_out = gb(df_pay, 'time', 'amount').set_index('time')

df_out['count'] = df_pay.groupby(['time']).size()
df_out.reset_index(inplace=True)
df_out['time'] = df_out['time'].apply(lambda x: pd.to_datetime(x))
df_out.sort_values('time', inplace=True)
df_out = df_out[['time', 'count', 'amount']]

df_out.to_excel(or_path + 'CPA渠道输出.xlsx')
print(df_out)


