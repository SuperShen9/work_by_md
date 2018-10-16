# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import os
import xlrd
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\工作簿1.xlsx', skiprows=1)

df = df[df['渠道/ID'].notnull()]
del df['新增用户游戏时长']
del df['所有用户游戏时长']
del df['最高在线']

# print('\n今日拆分渠道数量：{}\n'.format(df.shape[0]))


file_path = 'C:\\Users\Administrator\Desktop\\text'
for x, y, excels in os.walk(file_path):
    # print(y)
    for excel in excels:
        # print(excel)
        if excel.startswith('各'):
            wb = xlrd.open_workbook(x+'\\'+excel)
            for sheet_name in wb.sheet_names():
                sh = wb.sheet_by_name(sheet_name)

                print(sh.cell(1, 2).value)
            exit()

