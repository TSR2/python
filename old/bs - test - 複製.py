import requests
import bs4
import re
from functools import reduce  


list1 = []
for j in range(2000,2020):
    res = requests.get('https://www.ptt.cc/bbs/creditcard/index' + str(j) + '.html')
    soup=bs4.BeautifulSoup(res.text, "html.parser")

        
    aa = soup.select('div[class="title"] > a')
    print(len(aa))
    for i in range(len(aa)):
        print(aa[i].string)
        print(aa[i]['href'])

    aa = soup.select('.nrec')
    print(len(aa))
    #for i in range(len(aa)):
        #print(aa[i].string)
        

    aa = soup.select('div[class="nrec"] > span')
    print(len(aa))
    for i in range(len(aa)):
        print(aa[i].string)



    aa = soup.select('div[class="nrec"] > span')
    print(len(aa))
    for i in range(len(aa)):
        print(aa[i].string)


    title = soup.select('div[class="title"] > a')
    link = soup.select('div[class="title"] > a')
    push = soup.select('.nrec')
    author = soup.select('.author')
    date = soup.select('.date')
    
    for i in range(len(title)):
        main = requests.get('https://www.ptt.cc' + link[i]['href'])
        main_soup=bs4.BeautifulSoup(main.text, "html.parser")
        main_text = main_soup.select('div[id="main-content"]')
        content = filter(lambda x: type(x) == bs4.element.NavigableString, main_text[0].contents)
        content1 = "\n".join(map(lambda x: x.string,content))
        #content1 = reduce(lambda x,y: x+y,map(lambda x: x.string,content))
        print(content1)
        
        if push[i].string == None:
            push[i].string = '0'
        if  title[i].string != None:
            list1.append([title[i].string, title[i]['href'], push[i].string, author[i].string, date[i].string]) 
