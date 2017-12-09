
from collections import Counter
import jieba
import csv
import toolz
import string
from scipy.stats.stats import pearsonr
import re

r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n！？，﹚﹞！），．：；？｜︶︸︺︼︾﹀﹂﹄﹏､～]+' 


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
# =============================================================================
# 
# r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n！？，]+' 
# test = content[1]
# 
# string = re.sub(r,'',test) 
# print('%r' % string)
# print('%r' % test)
# =============================================================================
x = {}
for a, b in zip(score[1:190], content[1:190]):
    if a not in x:
        x[a] = ""
    x[a] = x[a] + b

def content_to_dict(x):
    list1 = list(jieba.cut(x))
    list_nostop = filter(lambda x: x not in stop1, list1)
    return dict(Counter(list_nostop))

train_dict = toolz.valmap(content_to_dict, x)

train_dict.keys()
train_dict[9]
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

predict = []
for i in range(190,200):
    predict.append(get_content_score(content[i]))

print(pearsonr(predict, score[190:200]))

