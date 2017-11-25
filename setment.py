
from collections import Counter
import jieba
import csv
import toolz

with open('C:/Users/TSR/Desktop/project data\ptt_tag_V1.csv') as csvfile:
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


        
def get_content_score(x):
    str_cut = list(jieba.cut(x))
    total_count = map(lambda x: contents_cut[1][x] ,str_cut)
    return list(total_count)

ss = get_content_score(content[1])
