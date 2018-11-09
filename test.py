# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import datetime
import time

# ----------------实时监测代码--------------------

while True:
    while True:

        min = datetime.datetime.now().strftime('%M')
        sec = datetime.datetime.now().strftime('%S')
        if int(sec) % 10 <= 3:
            time.sleep(1)
            print('数据已发送，读取数据为{}分{}秒.'.format(min, sec))
            break
        else:
            time.sleep(1)
            break

    time.sleep(10-1)
