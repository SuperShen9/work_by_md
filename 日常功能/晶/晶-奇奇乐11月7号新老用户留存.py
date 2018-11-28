# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from build.Func import or_path, gb

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings
from Func import append_excel
warnings.filterwarnings('ignore')

df = pd.read_excel(or_path('晶\\1107'))

zhuce = pd.read_excel(or_path('晶\\注册'))

zhuce['flag'] = 'new'
zhuce = zhuce[['用户ID', 'flag']]
zhuce.rename(columns={'用户ID': 'player_id'}, inplace=True)

df = pd.merge(left=df, right=zhuce, on='player_id', how='left')

df['flag'].fillna('old', inplace=True)

df=df[['player_id','flag']]

print(df.groupby(['flag']).size())

# exit()

# print(df.groupby('flag').size())

# print(df.sample(5))

df2=append_excel('C:\\Users\Administrator\Desktop\晶\登入')

df2['time']=df2['login_time'].apply(lambda x:x[:10])

df2=pd.merge(left=df2,right=df,on='player_id',how='left')

df2=pd.DataFrame(df2.groupby(['time','flag']).size())

df2.reset_index(inplace=True)

df2=pd.pivot_table(df2,values=0,index='time',columns='flag')

df2.to_excel(or_path('11月7日新老用户留存'))
