# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_old_excel
from build.Func import or_path
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import yesterday, bef_yesterday


def run2():
    try:
        # 读取数据
        df = du_old_excel('充值2天')
        df3 = du_old_excel('注册CPA')
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()

    df = df[df['channel'] == 800106]

    def time_c(df, col, sp=' '):
        df[col] = df[col].apply(lambda x: pd.to_datetime(str(x).split(sp)[0]))
        return df

    df = time_c(df, 'pay_time')
    df = df[df['pay_time'] == pd.to_datetime(yesterday)]


    df3 = time_c(df3, '注册时间')
    df3['flag']='new'
    df3.rename(columns={'用户ID':'player_id'},inplace=True)
    df3=df3[['player_id','flag']]

    df=pd.merge(left=df,right=df3,on='player_id',how='left')
    df=df[df['flag'].notnull()]


    print(len(df['player_id'].unique()))
    print(df['amount'].sum())

    df.to_excel(or_path+'saddf.xlsx')

    exit()

    return df

if __name__ == '__main__':
    df = run2()
