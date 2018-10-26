# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np
from Func import gb, ri_y, nian, yue, df_cut, ri_y2
from Func import du_old_excel
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

def run6():
    df=du_old_excel('我要赚钱')

    df['奖励一状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    df['奖励二状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    df['奖励三状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    df['time'] = df['关系建立时间'].apply(lambda x: x.split(' ')[0])

    df1 = df.groupby(['time'])['奖励一状态'].sum()
    df2 = df.groupby(['time'])['奖励二状态'].sum()
    df3 = df.groupby(['time'])['奖励三状态'].sum()

    df4 = df.groupby(['time']).size()

    df = pd.DataFrame([df1, df2, df3, df4]).T

    df.reset_index(inplace=True)
    df['day'] = df['time'].apply(lambda x: int(x.split('/')[-1]))

    df = df[(df['day'] >= int(ri_y2)) & (df['day'] <= int(ri_y))]

    df.rename(columns={'Unnamed 0': '总和'}, inplace=True)

    df['一档完成率'] = (df['奖励一状态'] / df['总和']).apply(lambda x: '%.2f%%' % x)
    df['二档完成率'] = (df['奖励二状态'] / df['总和']).apply(lambda x: '%.2f%%' % x)
    df['三档完成率'] = (df['奖励三状态'] / df['总和']).apply(lambda x: '%.2f%%' % x)

    df = df[['time', '奖励一状态', '奖励二状态', '奖励三状态', '一档完成率', '二档完成率', '三档完成率','总和']]

    df.rename(columns={'奖励一状态': '奖励一完成人数', '奖励二状态': '奖励二完成人数', '奖励三状态': '奖励三完成人数', 'time': '日期'}, inplace=True)

    print('\n第六个表运行完毕……')

    return df


# df.to_excel('C:\\Users\Administrator\Desktop\表格提取源\我要赚钱_OUT.xlsx', index=False)
