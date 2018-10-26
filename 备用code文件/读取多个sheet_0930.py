# -*- coding: utf-8 -*-
# author：Super.Shen
import xlrd
import pandas as pd
import os
from datetime import *

time1 = datetime.today()
nian = str(time1.year)

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# file_path = 'D:\MD_DATA\\0930数据\统计数据读取'
file_path ='D:\MD_DATA\\0930数据\统计数据读取\备用'
os.chdir(file_path)

df_all = pd.DataFrame()
for x, y, z in os.walk(file_path):
    for file in z:
        wb = xlrd.open_workbook(file)
        sheets = wb.sheet_names()
        for i in range(len(sheets)):
            df = pd.read_excel(file, sheet_name=i, skiprows=1, index=False, encoding='utf8')
            df.rename(columns={'兑换还费金额': '兑换话费金额', '渠道名称': '渠道名'}, inplace=True)
            df_all = df_all.append(df)

        df_all = df_all[['日期', '渠道名', '渠道ID', '当日DAU', '注册用户数', '登录用户数', '充值金额', '充值人数',
                         'Arpu值', '兑换红包金额', '兑换话费金额', '付费用户占比', '推广费',
                         '次日留存', '3日留存', '7日留存', '14日留存', '30日留存']]

        df_all = df_all[df_all['当日DAU'].notnull()]
        df_all.fillna(method='bfill', inplace=True)

df_all.to_excel('C:\\Users\Administrator\Desktop\T0930-2.xlsx', index=False)
