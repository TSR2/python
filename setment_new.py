
from collections import Counter
import jieba
import csv
import toolz
import string
from pandas import DataFrame
from pandas import Series


df = pandas.read_csv("C:/Users/TSR/Desktop/python/ptt_tag_V1_utf8.txt")

df1 = df.ix[1:200,:]
df1.columns
u_tag = df1.tag.unique()

group_df = DataFrame()


df_temp = df[df.tag == 9]
text1 = ''.join(df_temp.text)
append_df = DataFrame('tag': i , 'text')

for i in u_tag:
    df_temp = df[df.tag == i]
    text1 = ''.join(df_temp.text)
    append_df = DataFrame('tag': i , 'text')
