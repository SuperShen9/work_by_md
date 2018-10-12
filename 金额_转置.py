# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔金币产出明细(2).xlsx')



df = pd.pivot_table(df, values='数值', index='时间', columns='原因')

df = df[['未知', '每日登录抽奖', '玩家兑换礼物', '单局结算+', '充值', '充值礼包', '新手礼包', '成就任务', 'VIP奖励',
         '特惠充值', '快速充值', '领取邮件', '普通月卡', '豪华月卡', '单局结算-', '幸运抽奖']]



df['平台金币总产出'] = df[df.columns[:14]].apply(lambda x: x.sum(), axis=1)
df['平台金币总消耗'] = df[df.columns[14:16]].apply(lambda x: x.sum(), axis=1)
df['金币总盈余'] = df['平台金币总产出']+df['平台金币总消耗']
df = df.reset_index()
df.fillna(0, inplace=True)

df.to_excel('C:\\Users\Administrator\Desktop\浪仔金币产出明细(转置).xlsx',index=False)


