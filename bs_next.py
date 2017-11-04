import requests
import bs4
import re
import pandas

list1 = []
title1 = []
push1 = []
author1 = []
date1 = []

for j in range(2000,2050):
    res = requests.get('https://www.ptt.cc/bbs/creditcard/index' + str(j) + '.html')
    soup=bs4.BeautifulSoup(res.text, "html.parser")



    title = soup.select('div[class="title"] > a')
    push = soup.select('.nrec')
    author = soup.select('.author')
    date = soup.select('.date')


    for i in range(len(title)):
        
        if push[i].string == None:
            push[i].string = '0'
            
        list1.append([title[i].string, push[i].string, author[i].string, date[i].string]) 
        title1.append(title[i].string)
        push1.append(push[i].string)
        author1.append(author[i].string)
        date1.append(date[i].string)

data = DataFrame(list1)
