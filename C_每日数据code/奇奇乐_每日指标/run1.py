# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_old_excel
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


def run1():
    try:
        # 读取数据
        df = du_old_excel('充值2天')
        df_map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')
    except FileNotFoundError:
        print('\n缺少运行数据，请先下载……')
        exit()

    df_map = df_map[['product_id', 'Flag']]

    df['time'] = df['pay_time'].apply(lambda x: x.split(' ')[0])

    # 合并匹配表
    df = pd.merge(left=df, right=df_map, on='product_id', how='left')

    df_out = pd.DataFrame()
    for x, y in df.groupby(['time']):
        y = pd.DataFrame(y.groupby('Flag').size())
        y.columns = [x]
        df_out = pd.concat([df_out, y], axis=1)

    df_out.fillna(0, inplace=True)
    df_out.sort_values(by=df_out.columns[-1], ascending=0, inplace=True)


    # df_out[df_out.columns[0][-2:] + '号比例'] = df_out[df_out.columns[0]].apply(
    #     lambda x: '%.2f%%' % (x / df_out[df_out.columns[0]].sum() * 100))
    # df_out[df_out.columns[1][-2:] + '号比例'] = df_out[df_out.columns[1]].apply(
    #     lambda x: '%.2f%%' % (x / df_out[df_out.columns[1]].sum() * 100))

    df_out.reset_index(inplace=True)
    df_out.rename(columns={'index': '类型', 'Flag': '类型'}, inplace=True)

    print('\n第一个表运行完毕……')

    return df_out


if __name__ == '__main__':
    run1()
