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

    df = df[(df['channel'] == 800106) | (df['channel'] == 800113)]

    # 取str时间函数
    def time_c(df, col, sp=' '):
        df[col] = df[col].apply(lambda x: pd.to_datetime(str(x).split(sp)[0]))
        return df

    # 取出充值时间为昨天的数据
    df = time_c(df, 'pay_time')
    df = df[df['pay_time'] == pd.to_datetime(yesterday)]

    # 注册数据清洗用于匹配
    df3 = time_c(df3, '注册时间')
    df3['flag'] = 'new'
    df3.rename(columns={'用户ID': 'player_id'}, inplace=True)
    df3 = df3[['player_id', 'flag']]

    # 匹配到充值数据
    df = pd.merge(left=df, right=df3, on='player_id', how='left')
    df = df[df['flag'].notnull()]

    df = pd.DataFrame([df.groupby('channel')['amount'].sum(), df.groupby('channel')['player_id'].unique()]).T

    df['新用户付费人数'] = df['player_id'].apply(lambda x: len(x))

    df['(付费率)'] = ''

    df = df[['新用户付费人数', '(付费率)', 'amount']]

    df.to_excel(or_path + 'CPA注册新用户付费率.xlsx')

    exit()

    return df


if __name__ == '__main__':
    df = run2()
