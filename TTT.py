# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')
# df_map = map[['渠道ID', '渠道名']]
#
# print(df_map)

date = ['2017-5-1', '2017-5-2', '2017-5-3'] * 3
rng = pd.to_datetime(date)
df = pd.DataFrame({'date': rng,
                   'key': list('abcdabcda'),
                   'values': np.random.rand(9) * 10})
print(df)
print('-----')
print(pd.pivot_table(df, values='values', index='date', columns='key', aggfunc=np.sum))
