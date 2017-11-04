import requests
import bs4
import re
txt = ""
for i in range(5900,5936):
    #print('https://www.ptt.cc/bbs/movie/index' + str(i) + '.html')
    res = requests.get('https://www.ptt.cc/bbs/movie/index' + str(i) + '.html')
    res.raise_for_status()
    txt = txt + res.text

b = re.findall('<a href="/bbs/movie/M.*</a>',txt)
len(b)
for i in range(100):
	print(b[i])
