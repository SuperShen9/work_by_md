# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# df1 = pd.read_excel('C:\\Users\\Administrator\\Desktop\奖品兑换\奖品兑换701.xlsx')
# df2 = pd.read_excel('C:\\Users\\Administrator\\Desktop\奖品兑换\奖品兑换731.xlsx')
# df3 = pd.read_excel('C:\\Users\\Administrator\\Desktop\奖品兑换\奖品兑换911.xlsx')
#
# df = df1.append(df2, ignore_index=False)
#
# df = df.append(df3, ignore_index=False)
#
# df.to_hdf('C:\\Users\Administrator\Desktop\data.h5', key='data')

df=pd.read_hdf('C:\\Users\Administrator\Desktop\data.h5', key='data')
print(df.head(5))
# df = df.drop_duplicates(keep='last')
print(df.shape[0])
print('-'*100)
df=pd.DataFrame(df.groupby('用户id')['金额'].sum())

df.reset_index(inplace=True)
df.to_excel('C:\\Users\\Administrator\\Desktop\每个用户充值金额.xlsx')
print(df.head())