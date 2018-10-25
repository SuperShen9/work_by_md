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

df = df[df['types'] == 1]


def cal(col):
    df.loc[2, col] = '%.1f%%' % ((df.loc[1, col] - df.loc[0, col]) / df.loc[0, col] * 100)
    return df.loc[2, col]


df.reset_index(drop=True, inplace=True)
df['回收比'] = (df['Income'] + df['redgem'] * 2000) / df['Outlay']

df.loc[2, 'time'] = '环比'
df.loc[2, '回收比'] = (df.loc[1, '回收比'] - df.loc[0, '回收比'])
cal('Outlay')
cal('Income')
cal('redgem')
cal('num')

df['回收比'] = df['回收比'].apply(lambda x: '%.2f%%' % (x * 100))

df.rename(columns={'Outlay': '金币消耗', 'Income': '金币产出', 'redgem': '红宝石', 'num': '活跃用户数', 'time': '时间'}, inplace=True)

df = df[df.columns[1:]]

print(df)
