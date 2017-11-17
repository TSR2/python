import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from datetime import datetime
import matplotlib.dates as mdates

plt.style.use('ggplot')

df = pd.read_csv("C:/Users/TSR/Desktop/project data/NYC_restaurant.csv")

df = df.loc[:, ['DBA','CUISINE DESCRIPTION','BORO',
                'SCORE','GRADE','INSPECTION DATE',
                'VIOLATION CODE','VIOLATION DESCRIPTION']]
print(df)
df = df[df['DBA'                  ].notnull()]
df = df[df['CUISINE DESCRIPTION'  ].notnull()]
df = df[df['BORO'                 ].notnull()]
df = df[df['SCORE'                ].notnull()]
df = df[df['INSPECTION DATE'      ].notnull()]
df = df[df['VIOLATION CODE'       ].notnull()]
df = df[df['VIOLATION DESCRIPTION'].notnull()]


#Nodupkey到餐廳level

df       = df.sort_values(['DBA','BORO','INSPECTION DATE'],ascending = [1,1,0])
df_rest  = df.drop_duplicates(['DBA','BORO'], keep='last')


#1. PIVOT比較餐廳型態/地區/分數

restIncl = ['American','Italian','Chinese','Japanese','Mexican','Latin','Spanish']

df_rest_10 = df_rest[df_rest['CUISINE DESCRIPTION'].isin(restIncl)]
'''
boro_type = df_rest_10.pivot_table(values ='SCORE',
                                   index  ='CUISINE DESCRIPTION',
                                   columns='BORO',
                                   aggfunc='mean')
print(boro_type)

freq = df.pivot_table(values='SCORE',
                      index=['VIOLATION CODE','VIOLATION DESCRIPTION'],
                      columns='BORO',
                      aggfunc='count')
'''

#print(freq)

#2. 統計分析

des = df_rest['SCORE'].describe()
kur = df_rest['SCORE'].kurt()
skw = df_rest['SCORE'].skew()

#print(des)
#print(kur)
#print(skw)

'''
#3. 視覺化

boro_type.plot(kind='bar')
plt.show()

freq.plot(kind='bar')
plt.show()
'''

x = df['INSPECTION DATE']
y = df['SCORE']

x = [datetime.strptime(d, '%m/%d/%Y').date() for d in x]  # 把 string-> date的格式，讓程式讀懂日期 (先encode成一個變數，如同EXCEL寫日期，把格式改成數字)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))  # 抓這張圖的橫軸然後格式化成客製化日期

plt.scatter(x, y,s =1)  #畫散佈圖，s是每個marker的size
plt.show()

# plt.plot(x,y)
# plt.show()

'''
freq = df.pivot_table(values='SCORE',
                      index=['VIOLATION CODE','VIOLATION DESCRIPTION'],
                      columns='BORO',
                      aggfunc='count')
print(freq)
freq.to_csv("E:\Python Materials\Violation.csv")
'''

## 決策樹

tree = DecisionTreeClassifier(criterion='gini',max_depth=5)
aa = tree.fit(df[['SCORE']], df[['BORO']])
print(aa.predict_proba(19))

