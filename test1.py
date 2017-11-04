import requests
import bs4

res = requests.get('https://www.ptt.cc/bbs/Gossiping/index.html')
res.raise_for_status()
print(res.text[:300])
