import jieba
import pandas as pd
from sklearn import tree
from collections import Counter
from pandas.core.frame import DataFrame
import math
import re
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer
df    = pd.read_csv("Data4_ABC.csv")


df_SI = df

with open('Data_pre1_stopword.txt',encoding = 'utf8') as stopfile:
    spamreader = stopfile.read()


stop1 = spamreader.split('\n')
stop1.append('\n')
stop1.append('\r\n')
stop1.append(' ')
r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！？，﹚﹞！╱」－（）…＊“》”∼，．：「→；《？｜︶︸︺︼︾▲﹀﹂﹄﹏､～+、。【】〔〕]' 


bank =  ['花旗','台新','國泰','富邦','玉山','中信','元大']
pp = []
for i in bank:
    bank_index = df_SI.titl.str.contains(i)
    text = df_SI[bank_index]['text']
    print(len(text))
    text_all = ' '.join(text).upper()
    pp.append(text_all)


cut1 = pandas.read_csv("Data_pre2_userdict.txt")

for i in cut1.AA:
    jieba.add_word(i)
aa = []
for i in pp:
    cut1 = jieba.lcut(i)
    list_nostop = filter(lambda x: x not in stop1, cut1)
    list_nostop = ' '.join(list_nostop)
    list_nostop = re.sub('[0-9]','',list_nostop)
    list_nostop = re.sub(r,'',list_nostop)
    list_nostop = re.sub('LINE PAY','LINEPAY',list_nostop)
    aa.append(list_nostop)




vectorizer = CountVectorizer()  
#计算个词语出现的次数  
X = vectorizer.fit_transform(aa)  
#获取词袋中所有文本关键词  
word = vectorizer.get_feature_names()  
print(word)  
#查看词频结果  
print(X.toarray())

#类调用  
transformer = TfidfTransformer()  
#将词频矩阵X统计成TF-IDF值  
tfidf = transformer.fit_transform(X)  
#查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重  
print(tfidf.toarray())


ss = pandas.DataFrame(tfidf.toarray(),columns = word)
ss1 = pd.DataFrame.transpose(ss)
ss1.columns = bank
ss1
ss1.sort_values('國泰',ascending=False)
ss1['index'] = ss1.index

df_Bank=pd.DataFrame()
for i in range(len(bank)):
    ss2 = pd.DataFrame()
    ss2 = ss1[[bank[i],'index']]
    ss2 = ss2.sort_values(bank[i],ascending=False).reset_index(drop=True)
    df_Bank = pd.concat([df_Bank,ss2], axis=1)

print_full(df_Bank,150)
df_Bank.iloc[:100].to_csv("TFIDF_all.csv")
