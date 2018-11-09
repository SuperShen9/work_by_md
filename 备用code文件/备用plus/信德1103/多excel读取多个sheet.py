# -*- coding: utf-8 -*-
# author：Super.Shen
import xlrd
import pandas as pd
import numpy as np
from datetime import *
import os

time1 = datetime.today()
nian = str(time1.year)

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

file_path = 'C:\\Users\Administrator\Desktop\\new'
os.chdir(file_path)

count = 0
df3 = pd.DataFrame()
for x, y, z in os.walk(file_path):
    for file in z:
        count += 1
        wb = xlrd.open_workbook(file)
        sheets = wb.sheet_names()

        df_all = pd.DataFrame()
        for i in range(1, len(sheets)):
            df = pd.read_excel(file, sheet_name=i, skiprows=1, index=False, encoding='utf8')
            df.rename(columns={'兑换还费金额': '兑换话费金额', '渠道/ID': '渠道ID'}, inplace=True)
            df = df[df['渠道ID'].notnull()]
            df['渠道ID'] = df['渠道ID'].apply(lambda x: str(x).split('/')[-1])

            df['日期'] = sheets[i]
            df_all = df_all.append(df)

        # 删除空白行
        df_all = df_all[df_all['渠道ID'].notnull()]
        df_all = df_all[df_all['当日DAU'].notnull()]

        # df_all = df_all.sort_values(by='日期', ascending=0)

        # 读取匹配列表
        # map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')
        # df_map = map[['渠道ID', '渠道名']]

        # df_map['渠道ID'] =df_map['渠道ID'].apply(lambda x:str(x))
        #
        # df_all = pd.merge(left=df_all, right=df_map, on='渠道ID', how='left')

        df_all = df_all[['日期', '渠道ID', '当日DAU', '注册用户数', '登录用户数', '充值金额', '充值人数',
                         'Arpu值', '兑换红包金额', '兑换话费金额', '付费用户占比', '推广费',
                         '次日留存', '3日留存', '7日留存', '14日留存', '30日留存']]

        # 空白值填充0，为了计算有结果
        df_all.fillna(value=0, inplace=True)

        # 计算各个指标
        df_all['获客成本'] = df_all['推广费'] / df_all['注册用户数']
        df_all['回收'] = (df_all['充值金额'] - df_all['兑换红包金额'] - df_all['兑换话费金额']) / df_all['推广费']
        df_all['利润率'] = (df_all['充值金额'] - df_all['兑换红包金额'] - df_all['兑换话费金额'] - df_all['推广费']) / df_all['充值金额']
        df_all['净营'] = (df_all['充值金额'] - df_all['兑换红包金额'] - df_all['兑换话费金额'] - df_all['推广费'])

        # 挑选有用的列
        df_all = df_all[['日期', '渠道ID', '当日DAU', '注册用户数', '登录用户数', '充值金额', '充值人数',
                         'Arpu值', '兑换红包金额', '兑换话费金额', '付费用户占比', '推广费', '获客成本', '回收', '利润率', '净营',
                         '次日留存', '3日留存', '7日留存', '14日留存', '30日留存']]

        # 替换分母为0的计算值
        df_all.replace(np.inf, 0, inplace=True)
        df_all.replace(-np.inf, 0, inplace=True)

        # 日期列str转化为时间戳
        df_all['日期'] = pd.to_datetime(
            pd.Series(df_all['日期'].apply(lambda x: nian + '/' + x.split('-')[0] + '/' + x.split('-')[1])))

        # 按照日期排序
        df_all.sort_values(by='日期', inplace=True)



        df_all.to_excel('C:\\Users\Administrator\Desktop\\{}.xlsx'.format(file), index=False)
