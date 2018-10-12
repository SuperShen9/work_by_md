# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 反向通过分组-看用户充值几次
# df_zu = pd.DataFrame(df.groupby(['分组', 'player_id', 'nickname', 'channel_number']).size())
# df_zu = df_zu.reset_index()
# df_zu.rename(columns={0: '充值次数'}, inplace=True)

# # 分组
# df_f = pd.DataFrame(df.groupby('分组').size())
# df_f.columns=['人数']
# df_f.reset_index(inplace=True)
# print(df_f)

# def cut(df):
#     cdt1 = df['amount'] >= 5
#     cdt2 = df['amount'] < 100
#     df.loc[cdt1 & cdt2, '分组'] = '1|5 - 100'
#
#     cdt1 = df['amount'] >= 100
#     cdt2 = df['amount'] < 200
#     df.loc[cdt1 & cdt2, '分组'] = '2|100 - 200'
#
#     cdt1 = df['amount'] >= 200
#     cdt2 = df['amount'] < 500
#     df.loc[cdt1 & cdt2, '分组'] = '3|200 - 500'
#
#     cdt1 = df['amount'] >= 500
#     cdt2 = df['amount'] < 1000
#     df.loc[cdt1 & cdt2, '分组'] = '4|500 - 1000'
#
#     cdt1 = df['amount'] >= 1000
#     cdt2 = df['amount'] < 2000
#     df.loc[cdt1 & cdt2, '分组'] = '5|1000 - 2000'
#
#     cdt1 = df['amount'] >= 2000
#     df.loc[cdt1, '分组'] = '6|2000 +'
#
#     return df