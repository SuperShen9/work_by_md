# -*- coding: utf-8 -*-
# author：Super.Shen
import xlrd
import pandas as pd
from build.Func import or_path
from datetime import *
import os

time1 = datetime.today()
nian = str(time1.year)

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

def old_app(pingtai='qi'):
    if pingtai=='qi':
        file_path = 'C:\\Users\Administrator\Desktop\图表数据\奇奇乐'
        writer = pd.ExcelWriter(or_path('奇奇乐周报-报表'))
        list1 = ['新注册其次占比', '金币产出', '宝石分类', '宝石明细', '税收', '我要赚钱', '回收比']
    else:
        file_path = 'C:\\Users\Administrator\Desktop\图表数据\浪仔'
        writer = pd.ExcelWriter(or_path('浪仔周报-报表'))
        list1 = ['新注册其次占比', '金币产出', '宝石分类', '宝石明细', '税收', '我要赚钱']

    os.chdir(file_path)

    # 总的
    # list1 = ['渠道', '充值支付类型占比', '新注册其次占比', '金币产出', '金币消耗', '金币系统赠送', '宝石分类', '宝石明细', '奖品发放', '税收', '我要赚钱', '回收比']

    for name in list1:
        df_all = pd.DataFrame()
        for x, y, z in os.walk(file_path):
            for file in z:
                df = pd.read_excel(file, sheet_name=name, index=False, encoding='utf8')
                if name == '宝石明细':
                    df = df.drop([2, 3])
                elif name == '新注册其次占比':
                    df = df[['日期', '新用户量', '次日再消费用户量']]
                elif name == '金币产出':
                    df['其他'] = df['领取邮件'] + df['系统赠送']

                    if pingtai == 'qi':
                        df = df[['时间', '用户充值', '兑换红宝石', '兑换鱼雷', '其他']]
                    else:
                        df = df[['时间', '用户充值', '兑换红包券', '兑换鱼雷', '其他']]

                elif name == '宝石分类':
                    try:
                        df['其他'] = df['充值礼包'] + df['分享抽奖'] + df['成就任务'] + df['新手礼包']
                        df['其他2'] = df['幸运抽奖'] + df['欢乐夺宝'] + df['购买物品']
                        df = df[['时间', '游戏产出', '其他', '玩家兑换红包', '玩家兑换话费', '玩家兑换金币', '其他2']]

                    except KeyError:
                        if pingtai == 'qi':
                            df['其他'] = df['充值礼包'] + df['成就任务'] + df['新手礼包']
                            df['其他2'] = df['幸运抽奖'] + df['欢乐夺宝'] + df['购买物品']
                            df = df[['时间', '游戏产出', '其他', '玩家兑换红包', '玩家兑换话费', '玩家兑换金币', '其他2']]
                        else:
                            df['其他'] = df['充值礼包'] + df['分享抽奖'] + df['新手礼包']
                            df['其他2'] = df['幸运抽奖'] + df['欢乐夺宝'] + df['购买物品']
                            df = df[['时间', '游戏产出', '其他', '玩家兑换红包', '玩家兑换金币', '其他2']]

                elif name == '宝石明细':
                    del df['总和']
                elif name == '税收':
                    if pingtai == 'qi':
                        df['鱼雷场'] = df['鱼雷初级场'] + df['鱼雷中级场'] + df['鱼雷高级场']
                        df = df[['日期', '红包场', '鱼雷场', '猜猜乐']]
                    else:
                        pass

                df_all = df_all.append(df)

        df_all.sort_values(df_all.columns[0], inplace=True)
        df_all.drop_duplicates(keep='last', inplace=True)
        df_all.to_excel(writer, sheet_name=name, index=False)

    writer.save()

old_app()