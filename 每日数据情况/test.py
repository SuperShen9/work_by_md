# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import gb, ri_y, nian, yue

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

try:
    # 读取数据
    df = pd.read_excel('C:\\Users\Administrator\Desktop\每日充值金额\\浪仔{}号充值.xlsx'.format(ri_y))
    df2 = pd.read_excel('C:\\Users\Administrator\Desktop\每日充值金额\\奇奇乐{}号充值.xlsx'.format(ri_y))
except FileNotFoundError:
    print('\n缺少运行数据，请先下载……')
    exit()






print(df_c)
