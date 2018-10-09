# -*- coding: utf-8 -*-
# author：Super.Shen

import pandas as pd

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)
import warnings

warnings.filterwarnings('ignore')

# print(type(y.groupby('player_id')['具体变动'].apply(lambda x: list(x.T))))
# print(type(pd.DataFrame(y.groupby('player_id')['具体变动'].apply(lambda x: list(x.T)))))
# print(pd.DataFrame(y.groupby('player_id')['具体变动'].apply(lambda x: list(x.T))).reset_index())
# exit()