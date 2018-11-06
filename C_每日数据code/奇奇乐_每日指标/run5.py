# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_old_excel

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


def run5():
    df = du_old_excel('奖品发放')

    df['奖励'] = df['金额'].apply(lambda x: str(x) + '元') + df['类型']

    df['日期'] = df['兑换日期'].apply(lambda x: x[:10])

    df = pd.DataFrame(df.groupby(['日期', '奖励']).size())
    df.reset_index(inplace=True)

    df = pd.pivot_table(df, values=0, index='日期', columns='奖励')

    list1 = ['2元红包', '5元红包', '8元红包', '10元红包', '20元红包', '50元红包', '10元话费', '20元话费', '50元话费', '100元话费']

    try:
        df = df[list1]
    except KeyError:
        # 判定红包类型是否存在于list1
        error = [l for l in list1 if l not in list(df.columns)]
        # 把不存在的部分保存进df
        for x in error:
            df[x] = 0
        df = df[list1]


    df.fillna(0, inplace=True)


    df['总和'] = df.apply(lambda x: x.sum(), axis=1)

    print('\n第五个表运行完毕……')

    return df


if __name__ == '__main__':
    run5()
