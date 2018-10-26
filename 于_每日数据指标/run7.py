# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_excel

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


def run7():
    df = du_excel('税收')

    df['日期'] = df['日期'].apply(lambda x: str(x)[:10])

    df = pd.pivot_table(df, values='税收', index='日期', columns='场')
    df['总和'] = df.apply(lambda x: x.sum(), axis=1)
    df.reset_index(inplace=True)

    df.rename(columns={'猜猜乐场':'猜猜乐'},inplace=True)

    df = df[['日期', '红包场', '鱼雷场', '猜猜乐','总和']]

    return df.tail(2)


def run8():
    df = du_excel('回收比')
    df['time'] = df['时间'].apply(lambda x: str(x)[:10])

    df = df.groupby('time').sum()

    df['回收比'] = ((df['金币产出'] + df['红宝石产出'] * 2000) / df['金币消耗']).apply(lambda x: '%.2f%%' % (x * 100))

    df.reset_index(inplace=True)

    df.rename(columns={'time': '日期'}, inplace=True)

    print('\n第七个表运行完毕……')

    return df.tail(2)

# print(df)

# df.to_excel('C:\\Users\Administrator\Desktop\表格提取源\税收_OUT.xlsx',index=False)