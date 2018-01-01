
from collections import Counter
import jieba
import csv
import toolz
import numpy
from scipy.stats.stats import pearsonr
import re
import pandas
import datetime
import matplotlib.pyplot as plt
import matplotlib

test_ind = numpy.random.choice(range(200),30)


r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！？，﹚﹞！╱」－（）…＊“》”∼，．：「→；《？｜︶︸︺︼︾▲﹀﹂﹄﹏､～+、。【】〔〕]' 


# =============================================================================
# r = '''[:!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
# ﹔﹕﹖﹗﹚﹞！），．：；？｜︶︸︺︼︾﹀﹂﹄﹏､～￠
# 々‖•·ˇˉ′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
# ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…]+'''
# =============================================================================
with open('C:/Users/TSR/Desktop/project data/ptt_tag_V1.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    score = []
    content = []
    i = 0
    for row in spamreader:
        i = i + 1
        if i >= 202 :
            break
        elif i >= 2:
            score.append(int(row[2]))
            string = re.sub(r,'',row[3]) 
            content.append(string)

with open('C:/Users/TSR/Desktop/python/stopword.txt',encoding = 'utf8') as stopfile:
    spamreader = stopfile.read()


stop1 = spamreader.split('\n')
stop1.append('\n')
stop1.append('\r\n')
stop1.append(' ')

# =============================================================================
# 
# r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n！？，]+' 
# test = content[1]
# 
# string = re.sub(r,'',test) 
# print('%r' % string)
# print('%r' % test)
# =============================================================================

# =============================================================================
# score1 = score
# content1 = content
# score = []
# content = []
# score_test = []
# content_test = []
# 
# for i in range(len(score1)):
#     if i not in test_ind:
#         score.append(score1[i])
#         content.append(content1[i])
#     else:
#         score_test.append(score1[i])
#         content_test.append(content1[i])
# 
# =============================================================================

x = {}
for a, b in zip(score, content):
    if a not in x:
        x[a] = ""
    x[a] = x[a] + b

#jieba.load_userdict('Data_pre2_userdict.txt')
#jieba.load_userdict('C:/Users/TSR/Desktop/python/17Q4 ptt/Data_pre2_userdict.txt')
cut1 = pandas.read_csv("Data_pre2_userdict.txt")

for i in cut1.AA:
    jieba.add_word(i)


#jieba.del_word("中國信託")

def content_to_dict(x):
    list1 = list(jieba.cut(x))
    list_nostop = filter(lambda x: x not in stop1, list1)
    return dict(Counter(list_nostop))

train_dict = toolz.valmap(content_to_dict, x)
train_dict.keys()
train_dict[-3]

# =============================================================================
# for i in range(9):
#     print(train_dict[i].get("樂天", 0))
#     print(train_dict[-i].get("樂天", 0))
# 
# =============================================================================


def get_str_score(x):
    count = []
    weight = []
    score = []
    for key in train_dict.keys():
        if x in train_dict[key] :
            # 取得字詞出現次數
            count.append(train_dict[key][x])
            #留下對應權重
            weight.append(int(key))
        else :
            count.append(0)
            weight.append(0)
    for j in range(len(weight)):
        score.append(count[j]*weight[j])
    if sum(count) == 0:
        return 0
    else:
        return sum(score)/sum(count)

def get_content_score(x):
    str_cut = list(jieba.cut(x))
    total_count = list(map(get_str_score,str_cut))
    return sum(total_count)/len(total_count)


# =============================================================================
# predict = []
# for i in content_test:
#     predict.append(get_content_score(i))
# 
# print(pearsonr(predict, score_test))
# =============================================================================


# =============================================================================
# 
# predict = []
# for i in range(170,200):
#     predict.append(get_content_score(content[i]))
# 
# print(pearsonr(predict, score[170:200]))
# 
# 
# =============================================================================

df_org = pandas.read_csv("C:/Users/TSR/Desktop/python/17Q4 ptt/Data1_ptt.csv")

df = df_org[~df_org.date.isnull() & ~df_org.text.isnull()]
df.index = range(df.shape[0])
sum(df.date.isnull())
# =============================================================================
# get_content_score(df.text[100])
# =============================================================================


def txn_date(x):
    if x.find('月') > 1:
        date = x.strip()
        mm = date[0:date.find('月')]
        dd = date[date.find('月') + 1:date.find('日')]
        date_final = datetime.datetime(2017, int(mm), int(dd))
    else:
        date = x.strip()
        mm = date[0:date.find('/')]
        dd = date[date.find('/') + 1:]
        date_final = datetime.datetime(2017, int(mm), int(dd))
    return date_final


len(df.date)

df['date_new'] = pandas.Series(map(txn_date, df.date))
df[['date', 'date_new']]
df['predict_tag'] = pandas.Series(map(get_content_score, df.text))

tt = df.push
tt[tt == "XX"] = "-100"
tt[tt == "X1"] = "-10"
tt[tt == "X2"] = "-20"
tt[tt == "X3"] = "-30"
tt[tt == "X4"] = "-40"
tt[tt == "X5"] = "-50"
tt[tt == "爆"] = "100"

df['final_push'] = tt.astype(int)
df.final_push
df.to_csv("C:/Users/TSR/Desktop/python/17Q4 ptt/Data2_ptt_sentment.csv")



df = pandas.read_csv("C:/Users/TSR/Desktop/python/17Q4 ptt/Data2_ptt_sentment.csv")

tt = df.date_new.tolist()

df.date_new = pandas.Series(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'),tt))

def test1(x):
    y = x.upper()
    pp = re.sub('LINE PAY','LINEPAY',y)
    pp = re.sub('MONEY BACK','MONEYBACK',pp)
    return(pp)

aa = pandas.Series(map(test1,df.text))
df.text = aa
aa = pandas.Series(map(test1,df.titl))
df.titl = aa


df.text[df.text.str.contains('LINE')]


#聲量線圖
#情感分數
score_df = pandas.DataFrame()
#推文數量
talk_df = pandas.DataFrame()
#發文數量
post_df = pandas.DataFrame()
#討論人數
reply_df = pandas.DataFrame()

for j in ['花旗','台新','國泰','富邦','玉山','中信']:
    mean_score = []
    date1 = []
    talk = []
    reply = []
    post_count = []
    for i in range(202):
        str_con = df.titl.str.contains(j)
        if j == "國泰" :
            str_con = df.titl.str.contains(j) & ~df.titl.str.contains("國泰航空")
    
        end = datetime.datetime(2017, 6, 1)  + datetime.timedelta(i)
        start_date = df.date_new >= end - datetime.timedelta(9)
        end_date = df.date_new <= end
        
        test1 = df[str_con & start_date & end_date]
        
        post_count.append(test1.shape[0])
        mean_score.append(test1.predict_tag.mean(0))
        talk.append(test1.final_push.sum(0))
        reply.append(test1.reply.sum(0))
        date1.append(end)
        
    post_df[j] = post_count
    score_df[j] = mean_score
    talk_df[j] = talk
    reply_df[j] = reply
    
post_df.index = date1    
score_df.index  =date1
talk_df.index = date1
reply_df.index = date1


post_df.plot()
score_df.plot()
talk_df.plot()
reply_df.plot()

post_df.to_csv("Data3_post.csv")
score_df.to_csv("Data3_sentment.csv")
talk_df.to_csv("Data3_talk.csv")
reply_df.to_csv("Data3_reply.csv")



###


score_date_df = pandas.DataFrame()
#推文數量
talk_date_df = pandas.DataFrame()
#發文數量
post_date_df = pandas.DataFrame()
#討論人數
reply_date_df = pandas.DataFrame()


for j in ['花旗','台新','國泰','富邦','玉山','中信']:
    mean_score = []
    date1 = []
    talk = []
    reply = []
    post_count = []
    for i in range(212):
        str_con = df.titl.str.contains(j)
        if j == "國泰" :
            str_con = df.titl.str.contains(j) & ~df.titl.str.contains("國泰航空")
    
        targetdate = datetime.datetime(2017, 6, 1)  + datetime.timedelta(i)
        date_ind = df.date_new == targetdate
        
        test1 = df[str_con & date_ind]
        
        post_count.append(test1.shape[0])
        mean_score.append(test1.predict_tag.mean(0))
        talk.append(test1.final_push.sum(0))
        reply.append(test1.reply.sum(0))
        date1.append(targetdate)
        
    post_date_df[j] = post_count
    score_date_df[j] = mean_score
    talk_date_df[j] = talk
    reply_date_df[j] = reply

post_date_df.index = date1    
score_date_df.index  =date1
talk_date_df.index = date1
reply_date_df.index = date1

post_date_df.to_csv("Data3_post_date.csv")
score_date_df.to_csv("Data3_sentment_date.csv")
talk_date_df.to_csv("Data3_talk_date.csv")
reply_date_df.to_csv("Data3_reply_date.csv")


#拆類別


score_date_df = pandas.DataFrame()
#推文數量
talk_date_df = pandas.DataFrame()
#發文數量
post_date_df = pandas.DataFrame()
#討論人數
reply_date_df = pandas.DataFrame()


split_list = []

split_list.append(['核卡','額度','調額','財力'])
split_list.append(['登錄','登記','活動','回饋','優惠','促刷','點數'])
split_list.append(['盜刷','客服','安全','服務','方便'])

split_index_list=[]

for j in split_list:
    mean_score = []
    date1 = []
    talk = []
    reply = []
    post_count = []
    FF = pandas.Series([ False for i in range(df.shape[0])])
    for i in j:
        titl_index = df.titl.str.contains(i) | df.text.str.contains(i)
        FF = FF | titl_index 
    
    split_index_list.append(FF)

df.shape
sum(split_index_list[0]|split_index_list[1]|split_index_list[2])

df[split_index_list[0]]['A'] = 1

nogroup = df[~(split_index_list[0]|split_index_list[1]|split_index_list[2])]
nogroup.to_csv("Data4_nogroup.csv")

df['A'] = 0
df['B'] = 0
df['C'] = 0
df.A[split_index_list[0]] = 1
df.B[split_index_list[1]] = 1
df.C[split_index_list[2]] = 1


df.to_csv("Data4_ABC.csv")

print(sum(split_index_list[0]))
print(sum(split_index_list[1]))
print(sum(split_index_list[2]))


sum(split_index_list[1])
sum(split_index_list[2])



df.columns

#聲量線圖
#情感分數
dd = []
for k in [12,13,14]:
    score_df = pandas.DataFrame()
    for j in ['花旗','台新','國泰','富邦','玉山','中信']:
        mean_score = []
        date1 = []
        talk = []
        reply = []
        post_count = []
        for i in range(202):
            df1 = df[df.iloc[:,k]==1]
            str_con = df1.titl.str.contains(j)
            
            if j == "國泰" :
                str_con = df1.titl.str.contains(j) & ~df1.titl.str.contains("國泰航空")
        
            end = datetime.datetime(2017, 6, 1)  + datetime.timedelta(i)
            start_date = df1.date_new >= end - datetime.timedelta(9)
            end_date = df1.date_new <= end
            
            test1 = df1[str_con & start_date & end_date]
            if test1.shape[0] == 0:
                mean_score.append(df1[str_con].predict_tag.mean(0))
            else:
                mean_score.append(test1.predict_tag.mean(0))
            date1.append(end)
            
        score_df[j] = mean_score
    score_df.index = date1     
    dd.append(score_df)

type1 = ['A','B','C']

for i in range(3):
    dd[i].to_csv("sentment by type" + type1[i] + ".csv")






#類別count

type_index = {}
type_index['A'] = df.A == 1
type_index['B'] = df.B == 1
type_index['C'] = df.C == 1
type_index['AB'] = (df.A == 1) & (df.B == 1)
type_index['AC'] = (df.A == 1) & (df.C == 1)
type_index['BC'] = (df.B == 1) & (df.C == 1)
type_index['ABC'] = (df.A == 1) & (df.B == 1) & (df.C == 1)


rowname = ['A','B','C','AB','AC','BC','ABC']
colname = ['花旗','台新','國泰','富邦','玉山','中信']


df_reply = pandas.DataFrame()
df_post = pandas.DataFrame()
for i in rowname:
    reply_rowlist = {}
    post_rowlist = {}
    for j in colname:
        str_con = df.titl.str.contains(j)
        df1 = df[type_index[i] & str_con]
        
        reply_rowlist[j] = sum(df1.reply)
        post_rowlist[j] = df1.shape[0]
    df_reply = df_reply.append(pandas.DataFrame.from_dict([reply_rowlist]))
    df_post = df_post.append(pandas.DataFrame.from_dict([post_rowlist]))

df_reply.index = rowname
df_post.index = rowname

df_post.to_csv('post count by type.csv')
df_reply.to_csv('reply count by type.csv')





#卡別
def print_select(x):
    titl_index = df.titl.str.contains(x)
    text_index = df.text.str.contains(x)
    print(df[titl_index | text_index]['titl'])


def print_select(x):
    titl_index = df.titl.str.contains(x)
    print(df[titl_index]['titl'])
print_select('大中華')

print(df[4024:4025]['titl'])


ee = {}
def get_count(x):
    titl_index = df.titl.str.contains(x)
    text_index = df.text.str.contains(x)
    return(sum(titl_index | text_index))

cardtype = {}
cardtype['國泰KOKO'] = ['KOKO']
cardtype['兆豐E秒刷'] = ['E秒']
cardtype['台新GOGO'] = ['GOGO','RICHART','黑狗','紫狗']
cardtype['匯豐現金'] = ['匯豐現金']
cardtype['元大鑽金'] = ['鑽金']
cardtype['富邦數位生活'] = ['數位生活']
cardtype['中信line PAY'] = ["中信LP","中信 LP","中信 LINEPAY","中信LINEPAY","中國信託LINEPAY","中國信託 LINEPAY"]
cardtype['樂天'] = ['樂天']
cardtype['花旗現金回饋'] = ['花旗現金回饋']
cardtype['花旗響樂'] = ['饗樂','響樂']
cardtype['國泰COSTCO'] = ['COSTCO','好市多']
cardtype['中信ANA'] = ['ANA']
cardtype['花旗寰旅'] = ['寰旅']
cardtype['國泰亞洲萬里通'] = ['國泰亞萬','國泰亞洲萬里通']
cardtype['中信大中華'] = ['大中華']
cardtype['國泰長榮'] = ['國泰長榮','國泰世華長榮']
cardtype['美國運通'] = ['美國運通']
cardtype['台新國泰'] = ['台新國泰']
cardtype['美國運通'] = ['美國運通']

def get_count(x):
    Series1 = pandas.Series([ False for i in range(df.shape[0])])
    for i in x:
        titl_index = df.titl.str.contains(i)
        text_index = df.text.str.contains(i)
        Series1 = Series1 | titl_index | text_index
    return(sum(Series1))

def get_count3(x):
    Series1 = pandas.Series([ False for i in range(df.shape[0])])
    for i in x:
        titl_index = df.titl.str.contains(i)
        Series1 = Series1 | titl_index
    return(sum(Series1))

cardtype_count = {}
for i in cardtype:
    count1 = get_count(cardtype[i])
    cardtype_count[i] = count1

cardtype_count2 = {}
for i in cardtype:
    count1 = get_count3(cardtype[i])
    cardtype_count2[i] = count1
cardtype_count 
cardtype_count2
fout = "card type count(title).csv"
fo = open(fout, "w")

for k, v in cardtype_count2.items():
    fo.write(str(k) + ','+ str(v) + '\n')

fo.close()


def get_count2(x):
    titl_index = df.titl.str.contains(x)
    text_index = df.text.str.contains(x)
    ee[x] = sum(titl_index | text_index)

cash = ["KOKO","玉山ICASH","E秒","GOGO","元大鑽金","中信LP","中信 LINEPAY","中信LINEPAY",'樂天','花旗現金']
reward = ['饗樂','COSTCO','好市多','威秀','華航','大中華','數位生活']
mile = ['ANA','寰旅','MONEYBACK','渣打現金回饋','亞萬','國泰亞洲萬里通','國泰長榮','飛行','匯豐華航','華航匯豐','國泰亞洲萬里通','台新國泰','美國運通']
aa = list(map(get_count2, cash))

aa = list(map(get_count2, reward))

aa = list(map(get_count2, mile))

ee


for i in ee:
    print(i)


############雜項

def print_full(x,y):
    pandas.set_option('display.max_rows', y)
    print(x)
    pandas.reset_option('display.max_rows')

print_full(score_df['國泰'])
print_full(score_df['花旗'])
check = df[df.titl.str.contains('凱基')][['titl','predict_tag','date_new','push','reply']]
print_full(check.sort_values(by=['date_new']))

sum(df.titl == '富邦')

str_con = df.titl.str.contains('花旗')
tt1 = df[str_con][['titl','predict_tag','date_new','push']]

print_full(tt1.sort_values(by=['date_new']))












def save_plot(x,title,filename):
    x.plot(title = title,fontsize=20)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 12.5)
    fig.savefig(filename + '.png', dpi=300)

def save_pie(x,title,filename):
    x.sum(0).plot.pie(title = title, figsize=(8, 8) ,fontsize=30)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 12.5)
    fig.savefig(filename + '.png', dpi=300)

save_plot(post_df, "post", "post")
save_plot(score_df, "socre", "socre")
save_plot(talk_df, "talk", "talk")
save_plot(reply_df, "reply", "reply")

save_pie(post_df, "post", "post_pie")
save_pie(score_df, "socre", "socre_pie")
save_pie(talk_df, "talk", "talk_pie")
save_pie(reply_df, "reply", "reply_pie")


tt=post_df.sum(0)

tt.plot.pie(subplots=True, figsize=(8, 8),fontsize=20)

post_df.plot(fontsize=20)
score_df.plot()
talk_df.plot()
reply_df.plot()

tt.plot.pie(subplots=True, figsize=(8, 8),fontsize=20)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 12.5)
fig.savefig('test2png.png', dpi=300)


# =============================================================================
#
#
#
# df.titl[df.titl.str.contains('花旗')]
# df.date_new <= datetime.datetime(2017, 10, 1)
# test[test.str.contains('月')]
# tt = datetime.datetime(2009, 11, 8)
# tt1 = datetime.datetime(2009, 11, 15)
# p = tt1 -tt
# p.days
# df.date_new[1] <= datetime.datetime(2009, 11, 15)
# datetime.datetime(2009, 11, 15) + datetime.timedelta(30)
#
# ss = list(map(get_content_score, df.text[1900:1990]))
#
# df['setment'] = ss
#
# df.ix[1:5,:]
#
# ass = df.date[1:100]
#
# ass
#
# ass.str.contains('月')
#
# ass[98].find('日')
#
# ass[2].index('月')
# aa = datetime.date(2001,9,19)
#
# aa1 = datetime.date(2001,9,20)
# aa + 3
# aa1 - aa  == 1
#
# f1 = df.ix[0,:]
# def
# =============================================================================
