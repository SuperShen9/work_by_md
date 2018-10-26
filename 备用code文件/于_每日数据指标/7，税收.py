# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from Func import du_excel

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = du_excel('税收')

df['日期'] = df['日期'].apply(lambda x: str(x)[:10])

df = pd.pivot_table(df, values='税收', index='日期', columns='场')
df['总和'] = df.apply(lambda x: x.sum(), axis=1)
df.reset_index(inplace=True)

df.rename(columns={'猜猜乐场':'猜猜乐'},inplace=True)

df = df[['日期', '红包场', '鱼雷场', '猜猜乐','总和']]

print(df)

df.to_excel('C:\\Users\Administrator\Desktop\表格提取源\税收_OUT.xlsx',index=False)