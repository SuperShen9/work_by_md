# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

from Func import du_old_excel, du_excel, y7
import datetime

print('\n########请注意Func中的读取修改！###########\n')


def fx(x):
    nian = int(x.split('/')[0])
    yue = int(x.split('/')[1])
    ri = int(x.split('/')[2])

    return datetime.date(nian, yue, ri).isocalendar()[1] % 4


# 充值支付类型周对比
def run1():
    df = du_old_excel('充值')
    df_map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')

    df_map = df_map[['product_id', 'Flag']]

    df['time'] = df['pay_time'].apply(lambda x: x.split(' ')[0])

    df['week'] = df['time'].apply(lambda x: fx(x))

    # 合并匹配表
    df = pd.merge(left=df, right=df_map, on='product_id', how='left')

    df = pd.DataFrame([df.groupby(['Flag']).size(), df.groupby(['Flag'])['amount'].sum()]).T

    df.reset_index(inplace=True)

    df.sort_values(by=df.columns[-2], ascending=0, inplace=True)

    df.fillna(0, inplace=True)

    df.columns = ['类型', '充值次数', '充值金额']
    df['次数占比'] = df['充值次数'] / (df['充值次数'].sum())
    df['金额占比'] = df['充值金额'] / (df['充值金额'].sum())

    print('第一个表运行完毕')

    return df


# 新注册用户当日消费情况
def run2():
    df = du_old_excel('充值')
    df3 = pd.read_excel('C:\\Users\Administrator\Desktop\浪仔周报\注册.xlsx')

    # 提取充值数据的日期
    df['day'] = df['pay_time'].apply(lambda x: x.split(' ')[0].split('/')[2])
    df['on'] = df['player_id'].apply(lambda x: str(x)) + '|' + df['day']

    # # 整理前2天当日的注册数据
    df3['Flag'] = 'new'
    df3.rename(columns={'用户ID': 'player_id'}, inplace=True)
    df3['day'] = df3['注册时间'].apply(lambda x: x.split(' ')[0].split('/')[2])
    df3['on'] = df3['player_id'].apply(lambda x: str(x)) + '|' + df3['day']
    df3 = df3[['on', 'Flag']]

    df = pd.merge(left=df, right=df3, on='on', how='left')
    df['Flag'].fillna('old', inplace=True)

    i = 0
    df_form = pd.DataFrame()

    def df_f(df):
        # 人数计算
        df_form.loc[i, '新用户量'] = len(df[df['Flag'] == 'new']['player_id'].unique())
        df_form.loc[i, '总用户量'] = len(df['player_id'].unique())
        df_form.loc[i, '新用户占比'] = '%.2f%%' % (df_form.loc[i, '新用户量'] / df_form.loc[i, '总用户量'] * 100)

        # 金额消费计算
        df_form.loc[i, '新用户消费金额'] = df[df['Flag'] == 'new']['amount'].sum()
        df_form.loc[i, '总消费'] = df['amount'].sum()
        df_form.loc[i, '新用户消费占比'] = '%.2f%%' % (df_form.loc[i, '新用户消费金额'] / df_form.loc[i, '总消费'] * 100)

        return df_form

    df_form = df_f(df)

    # 删除多余2列
    del df_form['总用户量']
    del df_form['总消费']

    print('第二个表运行完毕.')

    return df_form


# 周度金币产生消耗占比
def run3():
    df = du_excel('金币分类')
    df_map = pd.read_excel('C:\\Users\Administrator\Desktop\map.xlsx')

    # 修改不规则的列====================================
    for x in range(df.shape[0]):
        if '鱼雷' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '兑换鱼雷'

        elif '红包券' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '兑换红包券'
        elif '迎新红包' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '兑换迎新红包'

    def change_col(x):
        if '鱼雷' in x:
            return int(x.split('(')[0])
        elif '红包券' in x:
            return int(x.split('(')[0])
        elif '迎新红包' in x:
            return int(x.split('(')[0])
        else:
            return int(x)

    df['数值'] = df['数值'].apply(lambda x: change_col(str(x)))

    # ====================================================

    df3 = df[df.columns[:3]]
    df3.dropna(axis=0, how='any', inplace=True)

    # 选取7天之前的时间
    df3 = df3[df3['时间'].apply(lambda x: pd.to_datetime(x)) >= pd.to_datetime(y7)]
    print('\n如果是月报，需要修改！ func中的y7值改为30\n')

    df3 = pd.pivot_table(df3, values='数值', index='时间', columns='原因')


    df3 = df3[['每日登录抽奖', 'VIP奖励', '新手礼包', '成就任务']]

    df3.reset_index(inplace=True)

    df3 = pd.DataFrame(df3.sum()).T

    '-----------------金币消耗汇总表--------------'

    # 金币消耗-透视
    df2 = df[df.columns[-3:]]
    df2.dropna(axis=0, how='any', inplace=True)

    # 选取7天之前的时间
    df2 = df2[df2['时间2'].apply(lambda x: pd.to_datetime(x)) >= pd.to_datetime(y7)]

    df2 = pd.pivot_table(df2, values='数值2', index='时间2', columns='原因2')
    del df2['单局结算']
    df2.reset_index(drop=True, inplace=True)

    df2 = pd.DataFrame(df2.sum()).T

    '----------------------------金币产出汇总表--------------------------'
    # 金币产出-透视
    df = df[df.columns[:3]]



    # 选取7天之前的时间
    df = df[df['时间'].apply(lambda x: pd.to_datetime(x)) >= pd.to_datetime(y7)]

    df_map = df_map[['原因', 'jinbi']]
    df_map.dropna(inplace=True)



    # 合并匹配表
    df = pd.merge(left=df, right=df_map, on='原因', how='left')


    df = df.groupby(['时间', 'jinbi'])['数值'].sum()

    df = pd.DataFrame(df)
    df.reset_index(inplace=True)

    df = pd.pivot_table(df, values='数值', index='时间', columns='jinbi')

    df.reset_index(inplace=True)

    df = df[['时间', '用户充值', '系统赠送', '兑换红包券', '兑换鱼雷', '兑换迎新红包', '领取邮件']]

    df.reset_index(drop=True, inplace=True)

    df = pd.DataFrame(df.sum()).T

    print('第三个表运行完毕.')

    return df, df2, df3


# 月度红包券计算
def run4():
    df = du_excel('红宝石')
    df2 = du_excel('红宝石明细')

    # 修改不规则的列=====================================
    for x in range(df.shape[0]):
        if '红包' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '玩家兑换红包'

        elif '话费' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '玩家兑换话费'

        elif '金币' in str(df.loc[x, '数值']):
            df.loc[x, '原因'] = '玩家兑换金币'

    def change_col(x):
        if '红包' in x:
            return int(x.split('(')[0])
        elif '话费' in x:
            return int(x.split('(')[0])
        elif '金币' in x:
            return int(x.split('(')[0])
        else:
            return int(x)

    df['数值'] = df['数值'].apply(lambda x: change_col(str(x)))

    # 选取7天之前的时间
    df = df[df['时间'].apply(lambda x: pd.to_datetime(x)) >= pd.to_datetime(y7)]
    df2 = df2[df2['日期'].apply(lambda x: pd.to_datetime(x)) >= pd.to_datetime(y7)]

    # ==========================================================

    '----------------------计算第一个表----------------------------------------------------------'

    df = pd.pivot_table(df, values='数值', index='时间', columns='原因')
    df.reset_index(inplace=True)


    # df = df[
    #     ['时间', '游戏产出', '新手礼包', '充值礼包', '玩家兑换红包', '玩家兑换金币', '幸运抽奖', '购买物品', '欢乐夺宝','活动抽奖']]

    df = df[
        ['时间', '游戏产出', '新手礼包', '充值礼包', '玩家兑换红包', '玩家兑换金币', '幸运抽奖', '购买物品', '欢乐夺宝', '分享抽奖']]

    df = pd.DataFrame(df.sum()).T

    '================================计算第二个表========================================='

    def fx(x):
        if x < 10:
            return '第一档'
        elif (x >= 10) and (x < 80):
            return '第二档'
        else:
            return '第三档'


    df2['档位'] = df2['游戏产出红宝石（红包场）'].apply(lambda x: fx(x))

    df2 = df2.groupby('档位').sum()
    df2 = df2[['次数', '总额']].T

    def hongbaoshi_minxi(df2):
        df2['总和'] = df2.apply(lambda x: x.sum(), axis=1)

        df2['一档比'] = (df2['第一档'] / df2['总和']).apply(lambda x: '%.2f%%' % (x * 100))
        df2['二档比'] = (df2['第二档'] / df2['总和']).apply(lambda x: '%.2f%%' % (x * 100))
        df2['三档比'] = (df2['第三档'] / df2['总和']).apply(lambda x: '%.2f%%' % (x * 100))

        df2 = df2[['第一档', '第二档', '第三档', '一档比', '二档比', '三档比', '总和']]
        df2.reset_index(inplace=True)

        return df2

    df2 = hongbaoshi_minxi(df2)

    del df2['一档比']
    del df2['二档比']
    del df2['三档比']

    print('第四个表运行完毕.')

    return df, df2

# 奖品发放
def run5():
    df = du_old_excel('奖品发放')

    df['奖励'] = df['金额'].apply(lambda x: str(x) + '元') + df['类型']

    df = pd.DataFrame(df.groupby(['奖励']).size()).T
    df.reset_index(inplace=True)

    list1 = ['1元红包', '2元红包', '5元红包', '10元红包', '20元红包', '30元红包']

    try:
        df = df[list1]
    except KeyError:
        # 判定红包类型是否存在于list1
        error = [l for l in list1 if l not in list(df.columns)]
        # 把不存在的部分保存进df
        for x in error:
            df[x] = 0
        df = df[list1]

    df.fillna(0, inplace=True)

    df['总和'] = df.apply(lambda x: x.sum(), axis=1)

    print('第五个表运行完毕.')
    return df


# 月度推广计算
def run6():
    df = du_old_excel('我要赚钱')

    df['奖励一状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    df['奖励二状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)
    df['奖励三状态'].replace({'已完成': 1, '未完成': 0}, inplace=True)

    del df['被推广玩家']
    del df['推广玩家']
    df.set_index('关系建立时间', inplace=True)

    df = pd.DataFrame(df.sum()).T

    print('\n第六个表运行完毕……')

    return df


def run7():
    df = du_excel('税收')

    # 选取7天之前的时间
    df = df[df['日期'].apply(lambda x: pd.to_datetime(x)) >= pd.to_datetime(y7)]

    df['差值'] = df['税收'] - df['税收'].shift(24)

    df = df.tail(4)

    df = pd.pivot_table(df, values='差值', index='日期', columns='场')

    df['总和'] = df.apply(lambda x: x.sum(), axis=1)

    df.rename(columns={'猜猜乐场': '猜猜乐'}, inplace=True)

    df = df[['红包场', '鱼雷场', '水果场', '猜猜乐', '总和']]

    print('第七个表【税收】运行完毕……')

    return df


df1 = run1()
df2 = run2()
df3, df_3, df_3_3 = run3()
df4, df_4 = run4()
df5 = run5()
df6 = run6()
df7 = run7()

# # 数据导出
writer = pd.ExcelWriter('C:\\Users\Administrator\Desktop\\浪仔-周报材料.xlsx')

df2.to_excel(writer, sheet_name='新用户消费占比', index=False)
df1.to_excel(writer, sheet_name='充值支付类型', index=False)


df3.to_excel(writer, sheet_name='金币产出', index=False)
df_3.to_excel(writer, sheet_name='金币消耗', index=False)
df_3_3.to_excel(writer, sheet_name='金币系统赠送', index=False)

df6.to_excel(writer, sheet_name='我要赚钱', index=False)

df7.to_excel(writer, sheet_name='税收', index=False)

df4.to_excel(writer, sheet_name='宝石分类', index=False)
df_4.to_excel(writer, sheet_name='宝石明细', index=False)

df5.to_excel(writer, sheet_name='奖品发放', index=False)

writer.save()
