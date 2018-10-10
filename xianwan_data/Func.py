# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import datetime

hour = datetime.datetime.now().strftime('%H')

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from datetime import *

time1 = datetime.today()
nian = str(time1.year)
yue = str(time1.month)
ri_y = str(time1.day - 1)
ri = str(time1.day)

if len(yue) < 2:
    yue = '0' + yue
if len(ri_y) < 2:
    ri_y = '0' + ri_y
if len(ri) < 2:
    ri = '0' + ri

def df_sum(df):
    i = 10000
    df.loc[i, '用户id'] = '汇总：'
    df.loc[i, '昵称'] = df.shape[0]
    df.loc[i, '充值金额'] = df['充值金额'].sum()
    df.loc[i, '兑换金额'] = df['兑换金额'].sum()
    df.loc[i, '单用户盈利'] = df['单用户盈利'].sum()
    df.loc[i, '累计红宝石产出'] = df['累计红宝石产出'].sum()
    df = df.reset_index(drop=True)

    return df
