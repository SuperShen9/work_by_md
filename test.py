# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import datetime
import time

f1 = pd.read_excel('C:\\Users\Administrator\Desktop\\用户行为.xlsx')

# print(f1['金币赢取'])
# print(f1['金币赢取'].apply(lambda x: -x))
# exit()

f1['盈亏回收比'] = (f1['宝石赚取'] / (f1['金币赢取'].apply(lambda x: -x)))

f1.sort_values('盈亏回收比', ascending=0, inplace=True)

f1.replace(-np.inf, np.NAN, inplace=True)

# f1.to_excel('C:\\Users\Administrator\Desktop\\XXXX.xlsx')
# exit()

y = pd.DataFrame(pd.cut(f1['盈亏回收比'], 100))
print(y.groupby('盈亏回收比').size())


