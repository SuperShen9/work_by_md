# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import day
import warnings

warnings.filterwarnings('ignore')

from Func import append_excel

# 读取每日登入用户并合并
df = append_excel('C:\\Users\Administrator\Desktop\奇奇乐付费新用户留存统计\登入数据')

df_cz = append_excel('C:\\Users\Administrator\Desktop\奇奇乐付费新用户留存统计\充值数据')
df_zc = append_excel('C:\\Users\Administrator\Desktop\奇奇乐付费新用户留存统计\注册数据')

# 【充值表】生成：去重列
df_cz['time'] = df_cz['pay_time'].apply(lambda x: str(x)[:10])
df_cz['on'] = df_cz['time'] + '|' + df_cz['player_id'].apply(lambda x: str(x))
# 充值表自我去重
df_cz = df_cz.drop_duplicates(subset=['on'], keep='first')

# 【注册表】生成：去重列
df_zc['time'] = df_zc['注册时间'].apply(lambda x: str(x)[:10])

# 另外计算注册人数
s1 = pd.DataFrame(df_zc.groupby('time').size())
s1.reset_index(inplace=True)
s1.columns = ['登入时间', '注册人数']

df_zc['on'] = df_zc['time'] + '|' + df_zc['用户ID'].apply(lambda x: str(x))
df_zc['flag'] = 'new'
df_zc = df_zc[['on', 'flag']]

# 合并2个表
df_cz = pd.merge(left=df_cz, right=df_zc, on='on', how='left')
df_cz = df_cz[df_cz['flag'] == 'new']
df_cz = df_cz[['on', 'flag']]
df_cz['player_id'] = df_cz['on'].apply(lambda x: int(x.split('|')[1]))

df_cz['flag'] = df_cz['on'].apply(lambda x: x.split('|')[0])

# 【登入表】计算
df['time'] = df['login_time'].apply(lambda x: str(x)[:10])

# 合并【登入表】和【充值用户】
df = pd.merge(left=df, right=df_cz, on='player_id', how='left')

# gb数据用于透视
df = pd.DataFrame(df.groupby(['time', 'flag']).size())
df.reset_index(inplace=True)

# 做透视
df = pd.pivot_table(df, values=0, index='time', columns='flag')

df.reset_index(inplace=True)

list1 = []
for n in range(len(list(df.columns))):
    if n == 0:
        list1.append('登入时间')
    else:
        list1.append(list(df.columns)[n].strip()[5:] + '用户')

df.columns = list1


from C_每日数据code.每次充值用户留存.test import form_out
form = form_out(df)
form = pd.merge(left=s1, right=form, on='登入时间', how='left')

form['付费比']=(form['新注册消费用户数']/form['注册人数']).apply(lambda x: str('%.2f%%' % (x * 100)))

# print(form)
# exit()

# 输出数据
writer = pd.ExcelWriter('C:\\Users\Administrator\Desktop\\奇奇乐{}日付费新用户留存统计.xlsx'.format(day))
form.to_excel(writer, sheet_name='付费用户每日留存', index=False)
df.to_excel(writer, sheet_name='data', index=False)
writer.save()
