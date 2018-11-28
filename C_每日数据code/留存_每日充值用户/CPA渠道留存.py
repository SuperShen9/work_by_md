# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
from build.database import lc_url, date
from build.Func import or_path

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')
import datetime

today = datetime.date.today()

df_all = pd.DataFrame()
for x in range(14, 0, -1):
    day = today - datetime.timedelta(days=x)
    df = date(lc_url(day))
    df['time'] = day
    df_all = df_all.append(df)
    print('{}号抓取完毕！'.format(day))

df_all.reset_index(inplace=True)
df_all = df_all[['time', 'counts', 'day1', 'day3', 'day7', 'day14', 'day30']]

# 测试专用
# df_all.to_excel(or_path('TTT'))
# df_all = pd.read_excel(or_path('TTT'))


def more(form, col):
    form[col] = form[col].apply(lambda x: str(int(x))) + '(' + (form[col] / form['counts']).apply(
        lambda x: str('%.0f%%' % (x * 100))) + ')'

for col in df_all.columns[2:]:
    more(df_all, col)

df_all.to_excel(or_path('趣头条每次用户留存'))
