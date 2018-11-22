# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_old_excel

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


def run6():
    df = du_old_excel('我要赚钱')

    df['gen_time'] = df['gen_time'].apply(lambda x: x.split(' ')[0])

    del df['invite_id']
    del df['player_id']
    df.set_index('gen_time', inplace=True)

    df_s=pd.DataFrame(df.groupby('gen_time').size())

    df = df.groupby('gen_time').sum()

    df['盈亏'] = df['recharge'] - df['get_redgem'] / 10 - df['redgem'] / 10 - df['gold'] / 20000

    df.reset_index(inplace=True)

    df=pd.merge(left=df_s,right=df,on='gen_time',how='left')

    df.rename(columns={'get_redgem': '获得红宝石', 'recharge': '充值金额', 'redgem': '奖励红宝石', 'gold': '奖励金币', 0: '被推广用户人数'},
              inplace=True)

    print('\n第六个表运行完毕……')

    return df


if __name__ == '__main__':
    run6()
