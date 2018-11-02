# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

import datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)


day = datetime.datetime.now().strftime('%d')
print(day)
print(int(day))