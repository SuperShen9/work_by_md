# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from build.database import out_bdzr
from build.Func import gb
from build.Func import or_path

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')
import datetime

# 从后台下载14开始的变动日志
# today = datetime.date.today()
# df_all = pd.DataFrame()
# for x in range(14, 0, -1):
#     day = today - datetime.timedelta(days=x)
#     df = out_bdzr(day)
#     df_all = df_all.append(df)
#     print('{}号抓取完毕！'.format(day))
#
# df_all.

# # 筛选出属于CPA的变动日志
# df = pd.read_hdf('C:\\Users\Administrator\Desktop\\bdrz.h5', key='data')
# df_reg = pd.read_excel(or_path('新闻资讯注册'))
# df_reg['flag'] = 'new'
# df_reg = df_reg[['用户ID', 'flag']]
# df = pd.merge(left=df, right=df_reg, on='用户ID', how='left')
# df = df[df['flag'].notnull()]
# df.to_hdf('C:\\Users\Administrator\Desktop\\test.h5', key='data')
# print(df.shape[0])
# exit()

df_pay = pd.read_excel(or_path('新闻资讯充值'))
df_pay = gb(df_pay, 'player_id', 'amount')

df = pd.read_hdf('C:\\Users\Administrator\Desktop\\test.h5', key='data')

df = pd.DataFrame(df.groupby(['游戏种类', '用户ID']).size())

df.reset_index(inplace=True)

df2 = pd.pivot_table(df, values=0, index='用户ID', columns='游戏种类')

df2 = df2[['大厅', '红包场', '鱼雷场', '水果狂欢', '鱼乐场']]
df2.reset_index(inplace=True)
df2.rename(columns={'用户ID': 'player_id'}, inplace=True)

df2 = pd.merge(left=df2, right=df_pay, on='player_id', how='left')

df2.fillna(0, inplace=True)

df2.sort_values(by='amount', ascending=0, inplace=True)

# df2.to_excel(or_path('kankan'))

df_f = pd.DataFrame(df.groupby('游戏种类').size()).T

df_f['总注册人数'] = 1295
df_f = df_f[['总注册人数', '大厅','红包场', '鱼雷场', '水果狂欢', '鱼乐场']]

# 数据导出
writer = pd.ExcelWriter(or_path('CPA渠道分析'))

df_f.to_excel(writer, sheet_name='用户场次占比', index=False)
df2.to_excel(writer, sheet_name='充值场次占比', index=False)
df_pay.to_excel(writer,sheet_name='充值排行',index=False)
writer.save()