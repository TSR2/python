
# 抓資料要跑很久! 要留30分鐘

import requests
import pandas as pd
import bs4
import time


name_col = ['titl', 'link', 'push', 'auth', 'date', 'text','reply']
tt1_col = []  # 做一個空的list
list1 = []
#1925
for num in range(1925, 2586):
    print(num)
    res = requests.get('https://www.ptt.cc/bbs/creditcard/index' + str(num) + '.html')
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    time.sleep(10)
    aa = soup.select('div[class="nrec"] > span')
    titl = soup.select('div[class="title"] > a')
    link = soup.select('div[class="title"] > a')
    push = soup.select('.nrec')
    auth = soup.select('.author')
    date = soup.select('.date')

    list2 = []
    for i in range(len(titl)):
        #print(link[i])
        main = requests.get('https://www.ptt.cc' + link[i]['href'])
        main_soup = bs4.BeautifulSoup(main.text, "html.parser")
        main_text = main_soup.select('div[id="main-content"]')
        text = ""
        
        if main_text != []:
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
            #push_type = list(map(lambda x:x.contents[0].string, push_tag))
            auth_push = list(map(lambda x:x.contents[1].string, push_tag))
            #content = list(map(get_push, push_tag))
            #sss = list(map(lambda x:x.contents[3].string, push_tag))
            uni_auth = []
            for x in auth_push:
                if x not in uni_auth:
                    uni_auth.append(x)
    # =============================================================================
    #         x = {}
    #         for a, b in zip(auth_push, content):
    #             if a not in x:
    #                 x[a] = ""
    #             x[a] = x[a] + b
    # =============================================================================
            
            
            #list2.append(text)
            #print(list2[1])
            if  push[i].string == None:
                push[i].string = '0'
            if  titl[i].string != None:
                list1.append([titl[i].string, link[i]['href'], push[i].string, auth[i].string, date[i].string, text, len(uni_auth)])

df_data_PTT = pd.DataFrame(list1, columns=name_col)
df_data_PTT.to_csv("C:/Users/TSR/Desktop/python/17Q4 ptt/Data1_ptt.csv")
