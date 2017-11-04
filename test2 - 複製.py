import requests
import bs4
import re
import jieba



res = requests.get('https://www.ptt.cc/bbs/creditcard/M.1507886564.A.15E.html')
soup=bs4.BeautifulSoup(res.text, "html.parser")

aa = soup.select('div[id="main-container"]')
print(aa[0].string)


aa = soup.select('div[id="main-content"]')
print(len(aa))
print(aa[0])
print(aa[0].string)
