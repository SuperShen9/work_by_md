# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import re

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\\名字加星.xlsx')

df['new'] = df['名字'].apply(lambda x: re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]', x))


def fx(x):
    if len(x) <= 2:
        return x[0] + '*'
    else:
        return x[0] + '*' * (len(x) - 2) + x[-1]


df['加星名称'] = df['new'].apply(lambda x: fx(x))

del df['new']

print('\n数据已处理完毕，请在桌面查收【名字处理结果.xlsx】！')

df.to_excel('C:\\Users\Administrator\Desktop\\名字处理结果.xlsx', index=False)
