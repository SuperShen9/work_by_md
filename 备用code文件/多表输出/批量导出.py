# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

df_all = pd.read_excel('C:\\Users\Administrator\Desktop\TTT1017.xlsx')

# 按照【渠道ID】和【时间】先后排序
df_all = df_all.sort_values(['渠道ID', '日期'])

# 按照每个渠道读取数据
for x, y in df_all.groupby('渠道ID'):
    # 期数向上填充
    y['期数'].fillna(method='ffill', inplace=True)
    # 重置index
    y = y.reset_index(drop=True)
    # 按照渠道名称写入 excel文件
    writer = pd.ExcelWriter('C:\\Users\Administrator\Desktop\每日渠道汇总\\{}.xlsx'.format(y.loc[0, '渠道名']))
    # 按照期数分组
    for x, y2 in y.groupby('期数'):
        # print(y2)

        # 求出日期的前10位
        y2['日期'] = y2['日期'].apply(lambda x: str(x)[:10])

        # sheet名称 按照周期存入
        y2[y2.columns[1:]].to_excel(writer, sheet_name=x[2:6], index=False)
    writer.save()
    # exit()
