# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import os

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')


file_dr = 'C:\\Users\Administrator\Desktop\奇奇乐_新用户_留存\用户登入数据'

file_cz = 'C:\\Users\Administrator\Desktop\奇奇乐_新用户_留存\充值数据'

df1 = pd.DataFrame()
for x, y, z in os.walk(file_dr):
    for excel in z:
        file = x + '\\' + excel
        df = pd.read_excel(file)

        # 登入时间的数据类型是str
        df['登入时间'] = '2018/10/' + excel.split('.')[0]

        df1 = df1.append(df, ignore_index=True)

df1.to_excel('C:\\Users\Administrator\Desktop\登入总数据.xlsx', index=False)

exit()
