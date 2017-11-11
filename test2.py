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
list_response = []
for i in aa :

    au = i.select('span[class="f3 hl push-userid"]')
    push_type1 = i.select('span[class="hl push-tag"]')
    push_type2 = i.select('span[class="f1 hl push-tag"]')
    main = i.select('span[class="f3 push-content"]')
    #print(au[0].string)
    #print(main[0].string)

    if  au[0].string != name1:
        if p == 1:
            name1 = au[0].string
            text = text + main[0].string[2::]
        else:
            


            if len(push_type1) > 0 : 
                print(push_type1[0].string)
            else:
                print(push_type2[0].string)
            s1 = snownlp.SnowNLP(text)
            print(name1)
            print(text,s1.sentiments)
            list_response.append(text)
            name1 = au[0].string
            text = main[0].string[2::]
            
        
    else:
        #print(text)
        text = text + main[0].string[2::]
    p = p+1
