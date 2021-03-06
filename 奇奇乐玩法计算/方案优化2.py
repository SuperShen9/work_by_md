# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

p1 = 776
p2 = 6984
p3 = 27160

h1 = 2
h2 = 20
h3 = 100

# # 税8个点
c1 = 0.1104
c2 = 1.104
c3 = 3.968

# c1 = 0.1104
# c2 = 0.904
# c3 = 1.768

try:
    # 读取方案数据
    df = pd.read_excel('C:\\Users\Administrator\Desktop\方案放入.xlsx')
except FileNotFoundError:
    print('\n缺少运行数据，请先将【方案放入】放在桌面……')
    exit()


# 划分档位函数
def fx_d(x):
    if x < 20:
        return 1
    else:
        return 2


df['数量'] = df['结算要求'].apply(lambda x: int(x.split(' x ')[1]))

# 划分档位
df['档位'] = df['数量'].apply(lambda x: fx_d(x))


# 领取次数划分函数
def fx(x):
    if x >= 20:
        if (x % 20) == 0:
            return x / 20
        else:
            # 加20才能稳定领取次数加一
            return (x + 20) / 20
    else:
        if (x % 2) == 0:
            return x / 2
        else:
            return (x + 1) / 2


# 划分领取次数
df['领取次数'] = (df['数量'].apply(lambda x: int(fx(x)))).apply(lambda x: int(x))

# 计算炮数
cdt = df['档位'] == 1
df.loc[cdt, '炮数'] = df['领取次数'] * p1

cdt2 = df['档位'] == 2
df.loc[cdt2, '炮数'] = df['领取次数'] * p2

# 计算金币
df['金币'] = df['炮数'] * 100

# 计算收入 / 收入不能累加 - 支出必须累加
df.loc[cdt, '收入'] = round(df['领取次数'] * c1, 2)
df.loc[cdt2, '收入'] = round(df['领取次数'] * c2, 2)

# 支出累加
df['支出'] = df['广告主单价'].cumsum()

# 计算利润
df['利润'] = round(df['收入'] - df['支出'], 2)

# 累加利润
df['累加利润'] = round(df['利润'].cumsum(), 2)

# print(df)
# exit()

del df['数量']

df.to_excel('C:\\Users\Administrator\Desktop\方案优化_运算.xlsx', index=False)

print('\n数据【方案优化_运算.xlsx】已存放在桌面，请查收！')
