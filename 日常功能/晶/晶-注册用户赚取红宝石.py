# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from dingtalkchatbot.chatbot import DingtalkChatbot
import warnings

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import os
from Func import or_path

warnings.filterwarnings('ignore')

import urllib.error
from urllib.request import urlopen
import socket
import time
import datetime


# 定义红包场-抓取-函数
def get_data(today):
    # 抓取数据
    try:
        # # 抓取网址
        # url = 'http://47.106.82.91:7000/aspx/interface/ManageData.ashx?action=ChangeLog&stime={}&etime={}&game=20'.format(
        #     today, today)
        # # 读取网址数据，并用json解析
        # content = urlopen(url=url, timeout=15).read()
        # content = content.decode('utf-8')
        # df = pd.read_json(content)
        #
        # # 数据分析
        # df['变动时间'] = df['变动时间'].apply(lambda x: pd.to_datetime(x))
        #
        # df.sort_values('变动时间', inplace=True)
        #
        # df.to_excel(or_path('奇奇乐今天变动日志数据'))

        df = pd.read_excel(or_path('奇奇乐今天变动日志数据'))

        # print(df.head())
        # exit()

        df['变动']=df['变动属性']+':'+df['初始值'].apply(lambda x:str(x))+'-'+df['差值'].apply(lambda x:str(-x))+';'

        df = df.groupby('用户ID')['变动'].sum()
        df.to_excel(or_path('TTT'))



        exit()

        # 去重df
        df_m = df[df['变动属性'] == '金币']
        df_m.drop_duplicates(subset='用户ID', keep='first',inplace=True)

        df_m = df_m[['用户ID', '初始值']]

        df = pd.DataFrame(df.groupby(['用户ID', '变动属性'])['差值'].sum())
        df.reset_index(inplace=True)

        df = pd.pivot_table(df, values='差值', index='用户ID', columns='变动属性')
        df.reset_index(inplace=True)

        df = df[['用户ID', '金币', '红宝石']]
        df.fillna(0, inplace=True)

        df['金币赢取'] = df['金币'] / 17000
        df['宝石赚取'] = df['红宝石'] / 10
        df['求和'] = df['金币赢取'] + df['宝石赚取']

        df.sort_values('求和', inplace=True, ascending=0)

        df.reset_index(drop=True, inplace=True)

        df=pd.merge(left=df,right=df_m,on='用户ID',how='left')

        # print(df.head())
        # exit()

        df.to_excel(or_path('奇奇乐盈利数据'))

        exit()

        return df

    except urllib.error.URLError:
        pass
    except socket.timeout:
        pass


today = datetime.date.today()
get_data(today)

# # ----------------用户回测代码--------------------
# today = datetime.date.today()
# yesterday = today - datetime.timedelta(days=1)
# hour = datetime.datetime.now().strftime('%H')
# min = datetime.datetime.now().strftime('%M')
#
# rmb = 50
#
# df = pd.read_excel('C:\\Users\Administrator\Desktop\\用户行为2.xlsx')
# df['输出'] = df['用户ID'].apply(lambda x: '> 用户ID：' + str(x) + '  -  ') + df['求和'].apply(
#             lambda x: '净赢：' + str(int(x)) + '\n\n')
#
# df2 = df[df['求和'] > rmb]
# df3 = df.tail(5)
#
#
# if df2.empty:
#     dingding_error('没有RMB赚取超过{}元的人.'.format(rmb))
# else:
#     dingding(df2)
#
#
# if df3.shape[0] < 5:
#     dingding_error('用户变动数据少于5人，稍后再次抓取.')
# else:
#     dingding2(df3)
#
# exit()
