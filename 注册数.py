# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np
from Func import day
import warnings

warnings.filterwarnings('ignore')

from Func import append_excel

# 读取每日登入用户并合并

df_zc = append_excel('C:\\Users\Administrator\Desktop\奇奇乐付费新用户留存统计\注册数据')
# 【注册表】生成：去重列
df_zc['time'] = df_zc['注册时间'].apply(lambda x: str(x)[:10])


print(df_zc.groupby('time').size())