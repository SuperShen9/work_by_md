# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from dingtalkchatbot.chatbot import DingtalkChatbot
import datetime

import warnings

warnings.filterwarnings('ignore')

import json, urllib.error
from urllib.request import urlopen
from datetime import timedelta
import socket

# 抓取网址
url = 'http://47.106.82.91:7000/aspx/interface/ManageData.ashx?action=Huishou&stime=2018-10-25%2013:30:00'
# 读取网址数据，并用json解析
content = urlopen(url=url, timeout=15).read()
content = content.decode('utf-8')
df = pd.read_json(content)

df = df[['id', 'times', 'types', 'Outlay', 'Income', 'num', 'redgem']]

df.sort_values('id', inplace=True)

df['time'] = df['times'].apply(lambda x: x.split('T')[1].split(':')[0] + '点')

df = df[['types', 'time', 'Outlay', 'Income', 'redgem', 'num']]

df = df.tail(6)


def cal(col):
    y.loc[2, col] = '%.1f%%' % ((y.loc[1, col] - y.loc[0, col]) / y.loc[0, col] * 100)
    return y.loc[2, col]


for x, y in df.groupby('types'):
    y.reset_index(drop=True, inplace=True)
    y['回收比'] = (y['Income'] + y['redgem'] * 2000) / y['Outlay']

    y.loc[2, 'time'] = '环比'
    y.loc[2, '回收比'] = (y.loc[1, '回收比'] - y.loc[0,'回收比'])
    cal('Outlay')
    cal('Income')
    cal('redgem')
    cal('num')

    y['回收比'] = y['回收比'].apply(lambda x:'%.2f%%' %(x*100))

    print(x)
    print(y)


