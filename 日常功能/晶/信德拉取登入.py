# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')


T_line = 35
def append_excel(file_path):
    df_all = pd.DataFrame()
    count = 0
    diff_file = []
    for x, y, z in os.walk(file_path):
        print('-' * T_line)
        print('文件夹中存在 {} 个文件.\n'.format(len(z)))
        for excel in z:
            file = x + '\\' + excel
            df = pd.read_excel(file)
            df_all = df_all.append(df, ignore_index=True)
            count += 1
            if count == 1:
                df_shape_start = df.shape[1]

            if df.shape[1] != df_shape_start:
                diff_file.append(excel)

    if df_shape_start == df_all.shape[1]:

        print('每个表格的列相同，且为{}列,数据合并完毕。'.format(df_shape_start))
        print('-' * T_line)
    else:
        print('表格{}的列不同，请检查！'.format(diff_file))
        print('-' * T_line)

    return df_all

# 读取每日登入用户并合并
df = append_excel('C:\\Users\Administrator\Desktop\奇10月登入数据')

print('\n当前文件中所有用户数量：{}'.format(df.shape[0]))

from build.Func import or_path

# df.to_excel(or_path('TTT'))

print('\n当前文件中用户唯一数值：{}'.format(df.drop_duplicates('player_id').shape[0]))


