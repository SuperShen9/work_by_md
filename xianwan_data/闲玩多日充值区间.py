# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import gb, df_cut

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\新用户数据分析\充值29.xls')

df['date'] = df['pay_time'].apply(lambda x: pd.to_datetime(x.split(' ')[0]))

df_a = pd.DataFrame()
for x, y in df.groupby('date'):
    y.reset_index(drop=True, inplace=True)
    df1 = gb(y, 'player_id', 'amount')
    df1 = df_cut(df1, 'player_id', 'amount', str(x))
    df_a = df_a.append(df1.T)

print(df_a)
# exit()

df_a.to_excel('C:\\Users\Administrator\Desktop\TTT.xlsx')
