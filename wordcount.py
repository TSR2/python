import jieba
import math
import pandas as pd
import numpy
from collections import Counter

#jieba.set_dictionary('/dict.txt')   #引用預設詞庫
#stop = open('stop_PTT.txt') #引用停用詞

df    = pd.read_csv("ptt_tag_V1_utf8.txt")
df_SI = df.loc[:103, ['titl', 'push', 'tag', 'stage', 'item', 'text']]
#print(df_SI)

# 將ppt內文全部斷詞，將原始資料計算項目個數，再做成字串

word_list1 =[]
for item1 in df_SI['text']:
    seglist = jieba.cut(item1, cut_all=False)

    word_list2 = []
    for item2 in seglist:
        if len(item2)>1:
            word_list2.append(item2)
    word_list3 = Counter(word_list2)
    word_list4 = pd.DataFrame.from_dict(word_list3,orient='index')
    word_list5 = pd.DataFrame.transpose(word_list4)
    #print(word_list3)
    #print(word_list4)
    #print(word_list5)
    word_list1.append(word_list5)
df_new = pd.concat(word_list1,ignore_index=True)


select = '台新'

df1 = df_new.fillna(0)
select_count = list(df1[df1[select]>0].sum())
allcount = sum(select_count)
idf = list(df1.shape[0]/df_new.count())

idf1 = list(map(lambda x:math.log(x), idf))
values= []
for i in range(4310):
	rr = (select_count[i]/allcount)*idf1[i]
	values.append(rr)

keys = list(df1.columns.values)

df5 = pd.DataFrame({ 'word':keys, 'value' :values})
df_final = df5.sort_values('value',ascending=False)
print(df_final.head)
