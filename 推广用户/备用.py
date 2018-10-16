# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df_c = pd.read_excel('D:\MD_DATA\\1015数据\充值\奇奇乐bef_8.10.xlsx')
df_c1 = pd.read_excel('D:\MD_DATA\\1015数据\充值\奇奇乐8.11_9.11.xlsx')
df_c2 = pd.read_excel('D:\MD_DATA\\1015数据\充值\奇奇乐充值9.12_now.xlsx')

df_c_all = df_c.append(df_c1, ignore_index=True)
df_c_all = df_c_all.append(df_c2, ignore_index=True)

df_c_all.drop_duplicates(inplace=True)


# # 推广玩家ID清洗
# df['推广玩家ID'] = df['推广玩家'].apply(lambda x: x.split('(')[0])
# df['推广玩家昵称'] = df['推广玩家'].apply(lambda x: x.split('(')[1][:-1])
