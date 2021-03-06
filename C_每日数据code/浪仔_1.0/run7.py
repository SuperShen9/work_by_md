# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_excel
from build.database import earn, lz_url, yesterday, y2, y3
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

def run9():
    df = du_excel('渠道')

    df = df.groupby('时间').sum()
    del df['充值人数']
    del df['最高在线']
    del df['付费用户占比']

    df.reset_index(inplace=True)

    df.loc[0,'兑换总金额']=df.loc[0,'兑换红包金额']+df.loc[0,'兑换话费金额']
    del df['兑换话费金额']
    del df['兑换红包金额']

    # print(df)

    print('\n第九个表【渠道】运行完毕……')

    return df


def run7():
    df2 = earn(lz_url, y3)
    df1 = earn(lz_url, y2)
    df = earn(lz_url, yesterday)

    df_c = df2.append(df1, ignore_index=True)
    df = df_c.append(df, ignore_index=True)

    df['税收'] = df['税收'].apply(lambda x: int(x))
    df['日期'] = df['日期'].apply(lambda x: str(x).split('T')[0])
    df['差值'] = df['税收'] - df['税收'].shift(4)

    df = pd.pivot_table(df, values='差值', index='日期', columns='场')

    df['总和'] = df.apply(lambda x: x.sum(), axis=1)
    df.reset_index(inplace=True)

    df.rename(columns={'猜猜乐场': '猜猜乐'}, inplace=True)

    df = df[['日期', '红包场', '鱼雷场', '水果场', '猜猜乐', '总和']]

    print('\n第八个表【税收】运行完毕……')

    return df.tail(2)

if __name__ == '__main__':
    print(run7())