# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
import datetime

import warnings

warnings.filterwarnings('ignore')

import urllib.error
from urllib.request import urlopen
from datetime import timedelta
import socket


def get_gold_data():
    # 抓取数据
    try:
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

        df.rename(columns={'Outlay': '金币消耗', 'Income': '金币产出', 'redgem': '红宝石', 'num': '活跃用户数', 'time': '时间'},
                  inplace=True)
        df = df[df.columns[1:]]

        return df

    except urllib.error.URLError:
        dingding_error('服务器连接失败.')
    except socket.timeout:
        dingding_error('socket错误，数据继续抓取.')


df = get_gold_data()

print(df)


def dingding(df):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=9d95fddbf93abc91ab9a85a15aa57688a31303c5e293aba686a7ede63710a3fa'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息(参数等于true @所有人)
    xiaoding.send_text(msg='''红包场{}统计：
    金币消耗:{}
    金币产出:{}
    红宝石:{}
    活跃用户数:{}
    回收比:{}\n
环比上一小时：
    金币消耗:{}
    金币产出:{}
    红宝石:{}
    活跃用户数:{}
    回收比:{}
    '''.format(df.loc[1, '时间'],
               int(df.loc[1, '金币消耗']),
               int(df.loc[1, '金币产出']),
               int(df.loc[1, '红宝石']),
               int(df.loc[1, '活跃用户数']),
               df.loc[1, '回收比'],

               df.loc[2, '金币消耗'],
               df.loc[2, '金币产出'],
               df.loc[2, '红宝石'],
               df.loc[2, '活跃用户数'],
               df.loc[2, '回收比']
               ), is_at_all=False)


dingding(df)


def dingding_error(text):
    # WebHook地址
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=9d95fddbf93abc91ab9a85a15aa57688a31303c5e293aba686a7ede63710a3fa'
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # Text消息(参数等于true @所有人)
    xiaoding.send_text(msg='''时间：{}\n抓取反馈：{}
    '''.format(str(datetime.datetime.now())[:19], text)
                       , is_at_all=False)
