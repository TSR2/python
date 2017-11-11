import requests
import bs4
import re
import snownlp

res = requests.get('https://www.ptt.cc/bbs/creditcard/M.1507886564.A.15E.html')
soup=bs4.BeautifulSoup(res.text, "html.parser")

aa = soup.select('div[class="push"]')
# aa = soup.select('span[class="f3 hl push-userid"]')

# au1 = aa[0].select('span[class="f3 hl push-userid"]')
# print(len(aa[0].contents))
# print(au1)
# print(au1[0].string)

#print(list(map(lambda x:len(x.contents), aa)))
push_type = list(map(lambda x:x.contents[0].string, aa))
#print(push_type)
auth = list(map(lambda x:x.contents[1].string, aa))
#print(auth)
content = list(map(lambda x:x.contents[2].string[2::], aa))
#print(content)
sss = list(map(lambda x:x.contents[3].string, aa))
#print(sss)


x = {}
for a, b in zip(auth, content):
	if a not in x:
		x[a] = ""
	x[a] = x[a] + b

print(x.keys())
print(x.values())

def map_se(x):
	point = (snownlp.SnowNLP(x).sentiments -0.5)*2
	return [x,point]
se = list(map(map_se, x.values()))
print(list(se))


# print(trans_to_list(aa))

# list_response = []
# for i in aa :
# 	au = i.select('span[class="f3 hl push-userid"]')
# 	push_type1 = i.select('span[class="hl push-tag"]')
# 	push_type2 = i.select('span[class="f1 hl push-tag"]')
# 	main = i.select('span[class="f3 push-content"]')




	#print(i.select('span[class="f3 hl push-userid"]')[0].string)


