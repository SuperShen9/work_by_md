# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import datetime
from build.database import url3, date, huishou

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

import os

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from run1 import run1
from run2 import run2
from run3 import run3
from run4 import run4
from run5 import run5
from run6 import run6
from run7 import run7, run8, run9

df1 = run1()
df2 = run2()
df3, df_3, df_3_3 = run3()
df4, df_4 = run4()
df5 = run5()
df6 = run6()
df7 = run7()
# df8 = run8()
df9 = run9()

df_hb = huishou(date(url3), 1)
df_yl = huishou(date(url3), 2)

# 数据导出
writer = pd.ExcelWriter('C:\\Users\Administrator\Desktop\\run_奇奇乐_{}.xlsx'.format(yesterday))

df9.to_excel(writer, sheet_name='渠道', index=False)

df1.to_excel(writer, sheet_name='充值支付类型占比', index=False)
df2.to_excel(writer, sheet_name='新注册其次占比', index=False)

df3.tail(2).to_excel(writer, sheet_name='金币产出', index=False)
df_3.tail(2).to_excel(writer, sheet_name='金币消耗', index=False)
df_3_3.tail(2).to_excel(writer, sheet_name='金币系统赠送', index=False)

df4.tail(2).to_excel(writer, sheet_name='宝石分类', index=False)
df_4.to_excel(writer, sheet_name='宝石明细', index=False)

df5.to_excel(writer, sheet_name='奖品发放')

df7.tail(2).to_excel(writer, sheet_name='税收', index=False)

df6.to_excel(writer, sheet_name='我要赚钱', index=False)

# df8.to_excel(writer, sheet_name='回收比', index=False)

df_hb.to_excel(writer, sheet_name='红包场', index=False)
df_yl.to_excel(writer, sheet_name='鱼雷场', index=False)

writer.save()


file1 = 'C:\\Users\Administrator\Desktop\\{}数据'.format(today)
list1 = [file1, ]
for i in list1:
    if os.path.exists(i):
        print('\n{}已创建文件！'.format(today))
    else:
        os.mkdir(i)
