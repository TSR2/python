 # -*- coding: utf-8 -*-
from collections import Counter
import jieba
import csv
import toolz
from scipy.stats.stats import pearsonr
import re
import pandas
import datetime
import matplotlib.pyplot as plt
import matplotlib


df_org    = pandas.read_csv("C:/Users/TSR/Desktop/python/ptt_tag_V1_date_utf.csv")

df = df_org[~df_org.date.isnull()]
df.index = range(df.shape[0])
sum(df.date.isnull())
# =============================================================================
# get_content_score(df.text[100])
# =============================================================================
test=df.date[1:100]


def txn_date(x):
    if x.find('月') > 1:
        date = x.strip()
        mm = date[0:date.find('月')]
        dd = date[date.find('月')+1:date.find('日')]
        date_final = datetime.datetime(2017, int(mm), int(dd))
    else:
        date = x.strip()
        mm = date[0:date.find('/')]
        dd = date[date.find('/')+1:]
        date_final = datetime.datetime(2017, int(mm), int(dd))
    return date_final

len(df.date)


df['date_new'] = pandas.Series(map(txn_date,df.date))
df[['date','date_new']]
df.columns
df['predict_tag'] = pandas.Series(map(get_content_score,df.text))

df[['tag','predict_tag']]

df.push
Counter(df.push)

score_df = pandas.DataFrame()
talk_df = pandas.DataFrame()

for j in ['花旗','玉山','台新','國泰','中信']:
    mean_score = []
    date1 = []
    talk = []
    for i in range(90):
        str_con = df.titl.str.contains(j)
        end = datetime.datetime(2017, 8, 1)  + datetime.timedelta(i)
        start_date = df.date_new >= end - datetime.timedelta(9)
        end_date = df.date_new <= end
        
        test1 = df[str_con & start_date & end_date]
        
        mean_score.append(test1.predict_tag.mean(0))
        talk.append(test1.push.sum(0))
        date1.append(end)
    score_df[j] = mean_score
    talk_df[j] = talk
    
score_df.index  =date1
talk_df.index = date1
print(score_df.columns)
score_df.columns[0]

score_df.plot()
talk_df.plot()

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 12.5)
fig.savefig('test2png.png', dpi=300)


def print_full(x):
    pandas.set_option('display.max_rows', len(x))
    print(x)
    pandas.reset_option('display.max_rows')

print_full(score_df['國泰'])


str_con = df.titl.str.contains('台新')
tt1 = df[str_con][['titl','predict_tag','date_new','push']]

print_full(tt1.sort_values(by=['date_new']))




# =============================================================================
# 
# 
# 
# df.titl[df.titl.str.contains('花旗')]
# df.date_new <= datetime.datetime(2017, 10, 1)
# test[test.str.contains('月')]
# tt = datetime.datetime(2009, 11, 8)
# tt1 = datetime.datetime(2009, 11, 15)
# p = tt1 -tt
# p.days
# df.date_new[1] <= datetime.datetime(2009, 11, 15)
# datetime.datetime(2009, 11, 15) + datetime.timedelta(30)
# 
# ss = list(map(get_content_score, df.text[1900:1990]))
# 
# df['setment'] = ss
# 
# df.ix[1:5,:]
# 
# ass = df.date[1:100]
# 
# ass
# 
# ass.str.contains('月')
# 
# ass[98].find('日')  
# 
# ass[2].index('月')
# aa = datetime.date(2001,9,19)
# 
# aa1 = datetime.date(2001,9,20)
# aa + 3
# aa1 - aa  == 1
# 
# f1 = df.ix[0,:]
# def 
# =============================================================================
