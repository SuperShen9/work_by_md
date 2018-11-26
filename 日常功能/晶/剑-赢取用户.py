# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import append_excel
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings
from build.Func import or_path
warnings.filterwarnings('ignore')

# df=append_excel('C:\\Users\Administrator\Desktop\jian')
#
# df.to_hdf('C:\\Users\Administrator\Desktop\jian\T.h5',key='data')
# exit()

df=pd.read_hdf('C:\\Users\Administrator\Desktop\jian\T.h5',key='data')


df = pd.DataFrame(df.groupby(['用户ID', '游戏种类','变动属性'])['差值'].sum())
df.reset_index(inplace=True)

# df=df[df['变动属性'].apply(lambda x:len(str(x))<2)]

df=df[df['变动属性']!=2]
df=df[df['变动属性']!=4]

def zl(x):
    if x==0:
        return '大厅'
    elif x==1:
        return '鱼雷场'
    elif x==20:
        return '红包场'
    elif x==21:
        return '鱼乐场'
    elif x==22:
        return '猜猜乐'

def sx(x):
    if x==1:
        return '金币'
    elif x==3:
        return '红包券'
    elif x==10001:
        return '鱼雷'



df['游戏种类']=df['游戏种类'].apply(lambda x:zl(x))
df['变动属性']=df['变动属性'].apply(lambda x:sx(x))


out=pd.DataFrame()
for x,y in df.groupby('用户ID'):

    y = pd.pivot_table(y, values='差值', index='游戏种类', columns='变动属性')
    y.fillna(0,inplace=True)



    y['求和']=y['红包券']*2000+y['金币']+y['鱼雷']*10000
    y['ID']=x
    y.reset_index(inplace=True)
    y= pd.pivot_table(y, values='求和', index='ID', columns='游戏种类')

    out=out.append(y)

del out['大厅']
out.fillna(0,inplace=True)
out['求和']=out.apply(lambda x:x.sum(),axis=1)
out2=out/20000


out.to_excel(or_path('四个用户变动详情'))
out2.to_excel(or_path('四个用户变动详情2'))


