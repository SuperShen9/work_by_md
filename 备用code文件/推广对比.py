# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import gb
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings
from build.Func import or_path
warnings.filterwarnings('ignore')

# df=pd.read_excel(or_path('新推广系统'))
#
# df.set_index('gen_time',inplace=True)
# del df['invite_id']
# del df['player_id']
# # print(df.head())
# # exit()
#
# df.loc['求和']=df.apply(lambda x:sum(x))
#
# df['盈亏'] = df['recharge'] - df['get_redgem'] / 10 - df['redgem'] / 10 - df['gold'] / 20000
#
# print(df)
# exit()
#
# df.to_excel(or_path('new'))

df=pd.read_hdf('C:\\Users\Administrator\Desktop.h5',key='data')

print(df.sample(10))

df=gb(df,'用户ID','差值')

df.to_excel('C:\\Users\Administrator\Desktop\old.xlsx')
exit()
print(df)