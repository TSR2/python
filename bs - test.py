import requests
import bs4
import re
import pandas
from functools import reduce  
import snownlp
import jieba


list1 = []
for j in range(2000,2001):
    res = requests.get('https://www.ptt.cc/bbs/creditcard/index' + str(j) + '.html')
    soup=bs4.BeautifulSoup(res.text, "html.parser")




    title = soup.select('div[class="title"] > a')
    link = soup.select('div[class="title"] > a')
    push = soup.select('.nrec')
    author = soup.select('.author')
    date = soup.select('.date')

    for i in range(len(title)):
        main = requests.get('https://www.ptt.cc' + link[i]['href'])
        main_soup=bs4.BeautifulSoup(main.text, "html.parser")
        #內文
        main_text = main_soup.select('div[id="main-content"]')
        #text = ""
        #for p in main_text[0].contents:
        #    if type(p) == bs4.element.NavigableString:
        #        text = text + "\n" + p.string
        content = filter(lambda x: type(x) != bs4.element.Tag, main_text[0].contents)
        content1 = reduce(lambda x,y: x+y,map(lambda x: x.string,content))
        #print(content1)
        #print(snownlp.SnowNLP(content1).sentiments)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(list(jieba.cut(content1)))
        #推文
        push_tag = main_soup.select('div[class="push"]')
        #print(list(map(lambda x:len(x.contents), push_tag)))
        print(push_tag)

        def get_push(x):
            if x.contents[2].string != None :  
                return x.contents[2].string[2::]
            else :
                return " "

        #print(list(map(lambda x:len(x.contents), aa)))
        push_type = list(map(lambda x:x.contents[0].string, push_tag))
        #print(push_type)
        auth = list(map(lambda x:x.contents[1].string, push_tag))
        #print(auth)
        content = list(map(get_push, push_tag))
        #print(content)
        sss = list(map(lambda x:x.contents[3].string, push_tag))
        #print(sss)


        x = {}
        for a, b in zip(auth, content):
            if a not in x:
                x[a] = ""
            x[a] = x[a] + b

        #print(x.keys())
        #print(x.values())

        def map_se(x):
            point = (snownlp.SnowNLP(x).sentiments -0.5)*2
            return [x,point]
        se = list(map(map_se, x.values()))
        print(list(se))

        if push[i].string == None:
            push[i].string = '0'
        if title[i].string != None:
            list1.append([title[i].string, title[i]['href'], push[i].string, author[i].string, date[i].string,content1, list(se)]) 


for i in range(5):
    print(list1[i])