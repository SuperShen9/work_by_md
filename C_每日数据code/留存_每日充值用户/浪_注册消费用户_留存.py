# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import day
import warnings
from build.database import date, yesterday, Register, Login, or_path, lz_3lc

warnings.filterwarnings('ignore')
from Func import append_excel

import datetime

today = datetime.date.today()

path = 'C:\\Users\Administrator\Desktop\浪仔_注册消费\\'

# # 日常数据累计
def fx(day):
    df, df1, df2 = lz_3lc(day)
    date(df).to_excel(path + '充值数据\\{}.xlsx'.format(day), index=False)
    Register(date(df1)).to_excel(path + '注册数据\\{}.xlsx'.format(day), index=False)
    Login(date(df2)).to_excel(path + '登入数据\\{}.xlsx'.format(day), index=False)

fx(yesterday)

# # 提取一段时间的三种数据
# for x in range(29):
#     day = today - datetime.timedelta(days=x + 1)
#     fx(day)
#     print('{}号数据抓取完毕'.format(day))
# exit()

# 读取每日登入用户并合并
df = append_excel(path + '登入数据')
df_cz = append_excel(path + '充值数据')
df_zc = append_excel(path + '注册数据')

# df.to_hdf('C:\\Users\Administrator\Desktop\df.h5',key='df')
# df_cz.to_hdf('C:\\Users\Administrator\Desktop\df_cz.h5',key='df_cz')
# df_zc.to_hdf('C:\\Users\Administrator\Desktop\df_zc.h5',key='df_cz')
# exit()

# df = pd.read_hdf('C:\\Users\Administrator\Desktop\df.h5', key='df')
# df_cz = pd.read_hdf('C:\\Users\Administrator\Desktop\df_cz.h5', key='df_cz')
# df_zc = pd.read_hdf('C:\\Users\Administrator\Desktop\df_zc.h5', key='df_cz')

def liucun(df, df_cz, df_zc, choose='new'):
    # 【充值表】生成：去重列
    df_cz['time'] = df_cz['pay_time'].apply(lambda x: pd.to_datetime(str(x).split(' ')[0]))
    df_cz['on'] = df_cz['time'].apply(lambda x: str(x)) + '|' + df_cz['player_id'].apply(lambda x: str(x))

    # 充值表自我去重
    df_cz = df_cz.drop_duplicates(subset=['on'], keep='first')

    # 【注册表】生成：去重列
    df_zc['time'] = df_zc['注册时间'].apply(lambda x: str(x)[:10])

    # 另外计算注册人数
    s1 = pd.DataFrame(df_zc.groupby('time').size())
    s1.reset_index(inplace=True)
    s1.columns = ['登入时间', '注册人数']
    s1['登入时间'] = s1['登入时间'].apply(lambda x: pd.to_datetime(x))
    s1.sort_values('登入时间', inplace=True)

    df_zc['on'] = df_zc['time'].apply(lambda x: str(pd.to_datetime(x.split(' ')[0]))) + '|' + df_zc['用户ID'].apply(
        lambda x: str(x))
    df_zc['flag'] = 'new'
    df_zc = df_zc[['on', 'flag']]

    # 合并2个表
    df_cz = pd.merge(left=df_cz, right=df_zc, on='on', how='left')

    if choose == 'new':
        df_cz = df_cz[df_cz['flag'] == 'new']
        file_name = '新'
    else:
        df_cz = df_cz[df_cz['flag'].isnull()]
        file_name = '未'

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

    df['time'] = df['time'].apply(lambda x: pd.to_datetime(x))
    df['flag'] = df['flag'].apply(lambda x: pd.to_datetime(x))

    # 做透视
    df = pd.pivot_table(df, values=0, index='time', columns='flag')
    df.reset_index(inplace=True)

    # 重命名列名
    list1 = []
    for n in range(len(list(df.columns))):
        if n == 0:
            list1.append('登入时间')
        else:
            list1.append(str(list(df.columns)[n])[5:10] + '号用户')

    df.columns = list1

    # 导入test中的函数
    from test import form_out

    form = form_out(df)
    # 添加充值人数
    form = pd.merge(left=s1, right=form, on='登入时间', how='left')

    form['付费率'] = (form['新注册消费用户数'] / form['注册人数']).apply(lambda x: str('%.2f%%' % (x * 100)))

    form = form[['登入时间', '注册人数', '新注册消费用户数', '付费率', '次日留存', '3日留存', '7日留存', '14日留存', '30日留存',
                 '次日留存累计', '3日留存累计', '7日留存累计', '14日留存累计', '30日留存累计']]

    return form, df, file_name


form, df, file_name = liucun(df, df_cz, df_zc, 'new')

# print(form)
# exit()

# 输出数据
writer = pd.ExcelWriter('C:\\Users\Administrator\Desktop\\浪仔截止{}日付费{}用户留存统计.xlsx'.format(yesterday, file_name))
form.to_excel(writer, sheet_name='付费用户每日留存', index=False)
df.to_excel(writer, sheet_name='data', index=False)
writer.save()
