# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import os
import xlrd
import numpy as np
from datetime import datetime, timedelta

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# 读取每日后台数据
df = pd.read_excel('C:\\Users\Administrator\Desktop\工作簿1.xlsx', skiprows=1)

# 删除无效列
df = df[df['渠道/ID'].notnull()]
del df['新增用户游戏时长']
del df['所有用户游戏时长']
del df['最高在线']

# 提取有效列
df['渠道名'] = df['渠道/ID'].apply(lambda x: x.split('/')[0])
df['渠道ID'] = df['渠道/ID'].apply(lambda x: int(x.split('/')[1]))

# 标记数据日期
df['日期'] = pd.to_datetime('2018/10/15')

# 重新排序df
df1 = df[['日期', '渠道名', '渠道ID', '当日DAU', '注册用户数', '登录用户数', '充值金额', '充值人数',
          'Arpu值', '兑换红包金额', '兑换话费金额', '付费用户占比', '推广费',
          '次日留存', '3日留存', '7日留存', '14日留存', '30日留存']]

# print('\n今日拆分渠道数量：{}\n'.format(df.shape[0]))

df_all = pd.DataFrame()

# 读取目标文件
file_path = 'C:\\Users\Administrator\Desktop\\text'

# 遍历文件路径
for x, y, excels in os.walk(file_path):
    # print(y)

    # 遍历excel文件
    for excel in excels:
        # print(excel)

        # 读取 “各” 开头的excel文件
        if excel.startswith('各'):
            # 补充路径
            file = x + '\\' + excel
            # xrld打开路径
            wb = xlrd.open_workbook(file)
            # 读取sheet名称
            sheets = wb.sheet_names()
            # 遍历sheet
            for i in range(len(sheets)):
                # 读取各个sheet
                df = pd.read_excel(file, sheet_name=i, index=False, encoding='utf8')
                # print(excel,sheets[i],i)
                # 周期 等于 第一个数字
                cycle = df.columns[0]
                # 重新读取各个sheet
                df = pd.read_excel(file, sheet_name=i, skiprows=1, index=False, encoding='utf8')

                # 重命名列 / 筛选空白列
                df.rename(columns={'兑换还费金额': '兑换话费金额'}, inplace=True)
                df['期数'] = cycle
                df = df[df['当日DAU'].notnull()]
                df = df[df['渠道名'].notnull()]
                # 累加df_all
                df_all = df_all.append(df, ignore_index=True)

# 将 数字的 日期改为 datatime
df_all['日期'] = df_all['日期'].apply(lambda x: datetime(1900, 1, 1) + timedelta(days=x - 2))

# 添加每日 下载的渠道 数据
df_all = df_all.append(df1, ignore_index=True)

# 重新排序列
df_all = df_all[['期数', '日期', '渠道名', '渠道ID', '当日DAU', '注册用户数', '登录用户数', '充值金额', '充值人数',
                 'Arpu值', '兑换红包金额', '兑换话费金额', '付费用户占比', '推广费',
                 '次日留存', '3日留存', '7日留存', '14日留存', '30日留存']]

# 导出数据
df_all.to_excel('C:\\Users\Administrator\Desktop\TTT1017.xlsx', index=False)
