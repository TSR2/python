import requests
import bs4
import re
import jieba
import snownlp


res = requests.get('https://www.ptt.cc/bbs/creditcard/M.1507886564.A.15E.html')
soup=bs4.BeautifulSoup(res.text, "html.parser")

aa = soup.select('div[class="push"]')
name1 = ""
text = ""
p = 1
for i in aa :

    au = i.select('span[class="f3 hl push-userid"]')
    main = i.select('span[class="f3 push-content"]')
    #print(au[0].string)
    #print(main[0].string)

    
    if  au[0].string != name1:
        if p == 1:
            name1 = au[0].string
            text = text + main[0].string[2::]
        else:
            
            s1 = snownlp.SnowNLP(text)
            print(name1)
            print(text,s1.sentiments)
            name1 = au[0].string
            text = main[0].string[2::]
        
        
    else:
        #print(text)
        text = text + main[0].string[2::]
    p = p+1
