
# 抓資料要跑很久! 要留30分鐘

import requests
import pandas as pd
import bs4

name_col = ['titl', 'link', 'push', 'auth', 'date', 'text','reply']
tt1_col = []  # 做一個空的list
list1 = []

for num in range(2000, 2020):

    res = requests.get('https://www.ptt.cc/bbs/creditcard/index' + str(num) + '.html')
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    aa = soup.select('div[class="nrec"] > span')
    titl = soup.select('div[class="title"] > a')
    link = soup.select('div[class="title"] > a')
    push = soup.select('.nrec')
    auth = soup.select('.author')
    date = soup.select('.date')

    list2 = []
    for i in range(len(titl)):
        main = requests.get('https://www.ptt.cc' + link[i]['href'])
        main_soup = bs4.BeautifulSoup(main.text, "html.parser")
        main_text = main_soup.select('div[id="main-content"]')
        text = ""
        for p in main_text[0].contents:
            if type(p) == bs4.element.NavigableString:
                text = text + "\n" + p.string
        # content = filter(lambda x: type(x) != bs4.element.Tag, main_text[0].contents)
        # content1 = reduce(lambda x,y: x+y,map(lambda x: x.string,content))
        #print(text)
        
        
        push_tag = main_soup.select('div[class="push"]')
        #print(list(map(lambda x:len(x.contents), push_tag)))
        #print(push_tag)

        def get_push(x):
            if x.contents[2].string != None :  
                return x.contents[2].string[2::]
            else :
                return " "

        #print(list(map(lambda x:len(x.contents), aa)))
        push_type = list(map(lambda x:x.contents[0].string, push_tag))
        auth_push = list(map(lambda x:x.contents[1].string, push_tag))
        content = list(map(get_push, push_tag))
        sss = list(map(lambda x:x.contents[3].string, push_tag))

        x = {}
        for a, b in zip(auth_push, content):
            if a not in x:
                x[a] = ""
            x[a] = x[a] + b
        
        
        list2.append(text)
        #print(list2[1])
        if  push[i].string == None:
            push[i].string = '0'
        if  titl[i].string != None:
            list1.append([titl[i].string, link[i]['href'], push[i].string, auth[i].string, date[i].string, text, len(x)])

df_data_PTT = pd.DataFrame(list1, columns=name_col)
df_data_PTT.to_csv("E:\Python Crawling\web-crawler-tutorial-master\ch2\Data1_ptt.csv")
