# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\\Administrator\\Desktop\充值15.xls')

df['hour'] = df['pay_time'].apply(lambda x: x.split(' ')[1].split(':')[0])

df = pd.DataFrame([df.groupby('hour')['player_id'].unique(), df.groupby('hour')['amount'].sum()]).T

df.reset_index(inplace=True)

df['hour'] = df['hour'].apply(lambda x: int(x))
df.sort_values('hour', ascending=1, inplace=True)

df['ren'] = df['player_id'].apply(lambda x: len(x))

df = df[['hour', 'ren', 'amount']]

df.reset_index(drop=True, inplace=True)

df.to_excel('C:\\Users\\Administrator\\Desktop\实时充值统计.xlsx', index=False)
