# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np
import datetime

today = datetime.date.today()
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.read_excel('C:\\Users\Administrator\Desktop\\text.xlsx')


print(df)
# df_c.to_excel('C:\\Users\Administrator\Desktop\\text2.xlsx')
exit()
