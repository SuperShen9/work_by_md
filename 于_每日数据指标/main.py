# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

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
from run7 import run7,run8

df1 = run1()
df2 = run2()
df3, df_3 = run3()
df4, df_4 = run4()
df5 = run5()
df6 = run6()
df7 = run7()
df8 = run8()

# print(df8)
# exit()

# 数据导出
writer = pd.ExcelWriter('C:\\Users\Administrator\Desktop\表格提取源\All_OUT.xlsx')
df1.to_excel(writer, sheet_name='充值支付类型占比', index=False)
df2.to_excel(writer, sheet_name='新注册其次占比', index=False)

df3.tail(2).to_excel(writer, sheet_name='金币产出', index=False)
df_3.tail(2).to_excel(writer, sheet_name='金币消耗', index=False)

df8.to_excel(writer, sheet_name='回收比', index=False)

df4.tail(2).to_excel(writer, sheet_name='宝石分类', index=False)
df_4.to_excel(writer, sheet_name='宝石明细', index=False)

df5.to_excel(writer, sheet_name='奖品发放')

df7.tail(2).to_excel(writer, sheet_name='税收', index=False)

df6.to_excel(writer, sheet_name='我要赚钱', index=False)


writer.save()
