
from collections import Counter
import jieba
import csv
import toolz
from scipy.stats.stats import pearsonr
import re
import pandas
import datetime

df    = pandas.read_csv("C:/Users/TSR/Desktop/python/ptt_tag_V1_date_utf.csv")
df.ix[1:5,:]

ss = []
df.shape
get_content_score(df.text[100])
df.date[1:100]
ss = list(map(get_content_score, df.text[1900:1990]))

df['setment'] = ss

df.ix[1:5,:]

ass = df.date[1:100]

ass

ass.str.contains('月')

ass[2].find('月')  

ass[2].index('月')
aa = datetime.date(2001,9,19)

aa1 = datetime.date(2001,9,20)
aa + 3
aa1 - aa  == 1

f1 = df.ix[0,:]
def 