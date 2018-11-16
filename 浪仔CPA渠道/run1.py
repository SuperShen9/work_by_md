# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_old_excel

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


def run1():
    df = du_old_excel('充值1114')
    df_map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')
    df_map = df_map[['product_id2', 'Flag2']]
    df_map.rename(columns={'product_id2': 'product_id', 'Flag2': 'Flag'}, inplace=True)

    df['time'] = df['pay_time'].apply(lambda x: x.split(' ')[0])

    # 合并匹配表
    df = pd.merge(left=df, right=df_map, on='product_id', how='left')

    df = df[(df['channel_number'] == 800106) | (df['channel_number'] == 800113)]

    df = pd.DataFrame(df.groupby(['channel_number', 'Flag']).size())

    df.reset_index(inplace=True)

    df = pd.pivot_table(df, values=0, index='Flag', columns='channel_number')

    df.fillna(0, inplace=True)
    df.sort_values(by=df.columns[-1], ascending=0, inplace=True)


    df.reset_index(inplace=True)
    df.rename(columns={800106: '趣头条|800106', 800113: '新闻资讯|800113'}, inplace=True)

    df.to_excel('C:\\Users\Administrator\Desktop\T2.xlsx')


    print('\n第一个表运行完毕……')

    return df


if __name__ == '__main__':
    run1()
