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


def form_out(df):
    form = pd.DataFrame(df['登入时间'])

    print('\ndf累加天数：{}天\n'.format(df.shape[0]))

    # 定义留存函数
    def liucun(df, day):
        i = 0
        if day == 0:
            for col in df.columns[1:]:
                form.loc[i, '新注册消费用户数'] = df[col][i + day]
                i += 1
        else:
            for col in df.columns[1:-day]:
                form.loc[i, '{}日留存'.format(day + 1)] = df[col][i + day]
                i += 1

    # 留存列表
    list1 = [0, 1, 2, 6, 13, 29]

    # 循环执行留存函数
    for i in list1:
        if i < df.shape[0]:
            liucun(df, i)

    form.rename(columns={'2日留存': '次日留存'}, inplace=True)
    form.fillna(0, inplace=True)

    for col in form.columns[2:]:
        form[col + '累计'] = ((form[col].cumsum() / form['新注册消费用户数'].cumsum()) * form[col] / form[col]).apply(
            lambda x: str('%.0f%%' % (x * 100)))

    def more(col):
        form[col] = (form[col] / form['新注册消费用户数']).apply(lambda x: str('%.0f%%' % (x * 100))) + '(' + form[
            col].apply(lambda x: str(int(x))) + ')'

    more('次日留存')
    more('3日留存')
    more('7日留存')
    # more('14日留存')
    # more('30日留存')

    form.replace('nan%', np.NAN, inplace=True)
    form.fillna(method='ffill', inplace=True)
    form.replace('0%(0)', np.NAN, inplace=True)

    return form


# df = pd.read_excel('C:\\Users\Administrator\Desktop\\text.xlsx')
# if __name__ == '__main__':
#     print(form_out(df))
