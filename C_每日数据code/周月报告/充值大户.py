# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import datetime

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings
from Func import du_old_excel, df_cut, y7

warnings.filterwarnings('ignore')


def fx(x):
    nian = int(x.split('/')[0])
    yue = int(x.split('/')[1])
    ri = int(x.split('/')[2])

    return datetime.date(nian, yue, ri).isocalendar()[1] % 4


# 充值支付类型周对比
def run1():
    df = pd.read_excel('C:\\Users\Administrator\Desktop\第一周充值.xls')

    # df=pd.DataFrame(df.groupby('player_id')['amount'].sum())
    # df.sort_values('amount',inplace=True,ascending=0)
    #
    # df.to_excel('C:\\Users\Administrator\Desktop\充值大户.xlsx')

    #
    df = df_cut(df, 'player_id', 'amount')

    df.to_excel('C:\\Users\Administrator\Desktop\第一周充值区间.xlsx')
    exit()


    return df


run1()
