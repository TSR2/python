
from collections import Counter
import jieba
import csv
import toolz
import string

with open('C:/Users/TSR/Desktop/project data/ptt_tag_V1.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    score = []
    content = []
    i = 0
    for row in spamreader:
        i = i + 1
        if i >= 201 :
            break
        elif i >= 2:
            score.append(row[2])
            content.append(row[3])


with open('C:/Users/TSR/Desktop/python/stopword.txt',encoding = 'utf8') as stopfile:
    spamreader = stopfile.read()

 
stop1 = spamreader.split('\n')



x = {}
for a, b in zip(score, content):
    if a not in x:
        x[a] = ""
    x[a] = x[a] + b

def content_to_dict(x):
    return dict(Counter(list(jieba.cut(x))))


aaa = toolz.valmap(lambda x:dict(Counter(list(jieba.cut(x)))), x)
#contents_cut = map(lambda x: Counter(list(jieba.cut(x))), x.values())
#contents_cut = list(contents_cut)


def get_str_score(x):
    count = []
    weight = []
    score = []
    for key in aaa.keys():
        if x in aaa[key] :
            count.append(aaa[key][x])
            weight.append(int(key))
        else :
            count.append(0)
            weight.append(0)
    for j in range(len(weight)):
        score.append(count[j]*weight[j])
    
    return sum(score)/sum(count)

def get_content_score(x):
    str_cut = list(jieba.cut(x))
    total_count = list(map(get_str_score,str_cut))
    return sum(total_count)/len(total_count)

score_final = []
for i in range(10):
    score_final.append([get_content_score(content[i]),score[i]])

print(score_final)
