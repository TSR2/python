import requests
import bs4
import re


res = requests.get('https://www.ptt.cc/bbs/creditcard/M.1507886564.A.15E.html')
soup=bs4.BeautifulSoup(res.text, "html.parser")

aa = soup.select('div[class="push"]')
au1 = aa[0].select('span[class="f3 hl push-userid"]')
print(au1)
soup._select_debug = True
au2 = soup.select('div[class="push"] > "f3 hl push-userid"')
print(au2)
# def trans_to_list(list1):
# 	return list(map(lambda x:x[0].string, list1))

# print(trans_to_list(aa))

list_response = []
for i in aa :
	au = i.select('span[class="f3 hl push-userid"]')
	push_type1 = i.select('span[class="hl push-tag"]')
	push_type2 = i.select('span[class="f1 hl push-tag"]')
	main = i.select('span[class="f3 push-content"]')




	#print(i.select('span[class="f3 hl push-userid"]')[0].string)
	# x = {}
	# for a, b in zip(listA, listB):
	# 	if a not in x:
	# 	x[a] = 0
	# 	x[a] += b