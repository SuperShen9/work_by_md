# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd
import numpy as np

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

df = pd.DataFrame({'one': np.random.rand(3), 'two': np.random.rand(3)})
list1 = [0, 1]

df['add'] = pd.DataFrame(list1)

print(df)


