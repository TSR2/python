
from collections import Counter
import jieba
import csv
import toolz
import numpy
from scipy.stats.stats import pearsonr
import re
import pandas
import datetime
import matplotlib.pyplot as plt
import matplotlib

test_ind = numpy.random.choice(range(200),30)


r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！？，﹚﹞！╱」－（）…＊“》”∼，．：「→；《？｜︶︸︺︼︾▲﹀﹂﹄﹏､～+、。【】〔〕]' 


# =============================================================================
# r = '''[:!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
# ﹔﹕﹖﹗﹚﹞！），．：；？｜︶︸︺︼︾﹀﹂﹄﹏､～￠
# 々‖•·ˇˉ′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
# ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…]+'''
# =============================================================================
with open('C:/Users/TSR/Desktop/project data/ptt_tag_V1.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    score = []
    content = []
    i = 0
    for row in spamreader:
        i = i + 1
        if i >= 202 :
            break
        elif i >= 2:
            score.append(int(row[2]))
            string = re.sub(r,'',row[3]) 
            content.append(string)

with open('C:/Users/TSR/Desktop/python/stopword.txt',encoding = 'utf8') as stopfile:
    spamreader = stopfile.read()


stop1 = spamreader.split('\n')
stop1.append('\n')
stop1.append('\r\n')
stop1.append(' ')

# =============================================================================
# 
# r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n！？，]+' 
# test = content[1]
# 
# string = re.sub(r,'',test) 
# print('%r' % string)
# print('%r' % test)
# =============================================================================

# =============================================================================
# score1 = score
# content1 = content
# score = []
# content = []
# score_test = []
# content_test = []
# 
# for i in range(len(score1)):
#     if i not in test_ind:
#         score.append(score1[i])
#         content.append(content1[i])
#     else:
#         score_test.append(score1[i])
#         content_test.append(content1[i])
# 
# =============================================================================

x = {}
for a, b in zip(score, content):
    if a not in x:
        x[a] = ""
    x[a] = x[a] + b

jieba.load_userdict('C:/Users/TSR/Desktop/python/stopword.txt')


def content_to_dict(x):
    list1 = list(jieba.cut(x))
    list_nostop = filter(lambda x: x not in stop1, list1)
    return dict(Counter(list_nostop))

train_dict = toolz.valmap(content_to_dict, x)
train_dict.keys()
train_dict[-3]

# =============================================================================
# for i in range(9):
#     print(train_dict[i].get("樂天", 0))
#     print(train_dict[-i].get("樂天", 0))
# 
# =============================================================================


def get_str_score(x):
    count = []
    weight = []
    score = []
    for key in train_dict.keys():
        if x in train_dict[key] :
            # 取得字詞出現次數
            count.append(train_dict[key][x])
            #留下對應權重
            weight.append(int(key))
        else :
            count.append(0)
            weight.append(0)
    for j in range(len(weight)):
        score.append(count[j]*weight[j])
    if sum(count) == 0:
        return 0
    else:
        return sum(score)/sum(count)

def get_content_score(x):
    str_cut = list(jieba.cut(x))
    total_count = list(map(get_str_score,str_cut))
    return sum(total_count)/len(total_count)


# =============================================================================
# predict = []
# for i in content_test:
#     predict.append(get_content_score(i))
# 
# print(pearsonr(predict, score_test))
# =============================================================================


# =============================================================================
# 
# predict = []
# for i in range(170,200):
#     predict.append(get_content_score(content[i]))
# 
# print(pearsonr(predict, score[170:200]))
# 
# 
# =============================================================================

df_org = pandas.read_csv("C:/Users/TSR/Desktop/python/ptt_tag_V1_date_utf.csv")

df = df_org[~df_org.date.isnull()]
df.index = range(df.shape[0])
sum(df.date.isnull())
# =============================================================================
# get_content_score(df.text[100])
# =============================================================================
test = df.date[1:100]


def txn_date(x):
    if x.find('月') > 1:
        date = x.strip()
        mm = date[0:date.find('月')]
        dd = date[date.find('月') + 1:date.find('日')]
        date_final = datetime.datetime(2017, int(mm), int(dd))
    else:
        date = x.strip()
        mm = date[0:date.find('/')]
        dd = date[date.find('/') + 1:]
        date_final = datetime.datetime(2017, int(mm), int(dd))
    return date_final


len(df.date)

df['date_new'] = pandas.Series(map(txn_date, df.date))
df[['date', 'date_new']]
df.columns
df['predict_tag'] = pandas.Series(map(get_content_score, df.text))

df[['tag', 'predict_tag']]

score_df = pandas.DataFrame()

for j in ['花旗', '玉山', '台新', '國泰', '中信']:
    mean_score = []
    date1 = []
    for i in range(90):
        str_con = df.titl.str.contains(j)
        end = datetime.datetime(2017, 8, 1) + datetime.timedelta(i)
        start_date = df.date_new >= end - datetime.timedelta(9)
        end_date = df.date_new <= end

        test1 = df[str_con & start_date & end_date]

        mean_score.append(test1.predict_tag.mean(0))
        date1.append(end)
    score_df[j] = mean_score

score_df.index = date1

print(score_df.columns)
score_df.columns[0]

score_df.plot()

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 12.5)
fig.savefig('test2png.png', dpi=300)





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
