# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

import urllib.request
import json


# --------------------------------
# 获取企业微信token
# --------------------------------

def get_token(url, corpid, corpsecret):
    token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
    token = json.loads(urllib.request.urlopen(token_url).read().decode())['access_token']
    return token


# --------------------------------
# 构建告警信息json
# --------------------------------
def messages(msg):
    values = {
        "touser": '@all',
        "msgtype": 'text',
        "agentid": 1000002,  # 偷懒没有使用变量了，注意修改为对应应用的agentid
        "text": {'content': msg},
        "safe": 0
    }
    msges = (bytes(json.dumps(values), 'utf-8'))
    return msges


# --------------------------------
# 发送告警信息
# --------------------------------
def send_message(url, token, data):
    send_url = '%s/cgi-bin/message/send?access_token=%s' % (url, token)
    respone = urllib.request.urlopen(urllib.request.Request(url=send_url, data=data)).read()
    x = json.loads(respone.decode())['errcode']
    # print(x)
    if x == 0:
        print('Succesfully')
    else:
        print('Failed')


##############函数结束########################

corpid = 'wx***********************'
corpsecret = 'Iwy******************************'
url = 'https://qyapi.weixin.qq.com'
msg = 'test,Python调用企业微信测试'

# 函数调用
test_token = get_token(url, corpid, corpsecret)
msg_data = messages(msg)
send_message(url, test_token, msg_data)
