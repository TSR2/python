library(tm)
library(tmcn)
library(rJava)
library(plyr)
library(stringr)
library(ggplot2)
library(wordcloud)
library(Rwordseg)
library(XML)
library(RCurl)
library(jiebaR)
library(dplyr)
library(magrittr)

wk = worker()

data_org <- read.csv("C:/Users/TSR/Desktop/project data/ptt_tag_V1.csv",
                 header = T, stringsAsFactors = FALSE, encoding = "big5")
len = 200

data_org$tag[1:len] %>% table
data_1 = data_org[1:len,]
data_1 = data_1[data_1$tag != 0,]
len1 = dim(data_1)[1]
set.seed(7)
lead = sample(1:len1,len1)
data = data_1
index_data = data[lead[1:floor(len1*0.9)],]
index_data_test = data[lead[(floor(len1*0.9)+1):len1],]

combine_text = index_data %>% group_by(tag) %>% summarise(text1=paste(text, collapse=""))
print(combine_text[6,2],width = 200)


split_list= apply(combine_text, 1, function(x) list(x[1] %>% as.numeric,wk[x[2]]))
split_list %>% sapply(function(x) c(x[1],length(x[[2]])))

keys = worker("keywords",topn=5)
split_list %>% sapply( function(x) vector_keywords(x[[2]],keys))



#情感分析 字典
pos = read.table("C:/Users/TSR/Desktop/project data/pos.txt",stringsAsFactors = FALSE)
pos = pos[,1]
pos[1:100]

neg = read.table("C:/Users/TSR/Desktop/project data/neg.txt",stringsAsFactors = FALSE)
neg = neg[,1]
neg[1:100]

c(1,3,4) %in% c(3,4)

map_sentment = function(x){
  pos_point = x[[2]] %in% pos %>% sum
  neg_point = x[[2]] %in% neg %>% sum
  c(x[1] %>% as.numeric(),pos_point,neg_point)
}

test1 = split_list %>% sapply(map_sentment)
test1
test1 %<>% as.data.frame()

rbind(test1,test1[2,]/test1[3,])


#情感分析 自創
test = index_data_test
index_data_test[1,]
index_data_test$tag
map_sentment_alan = function(y){
  score = split_list %>% sapply(function(x) x[[2]] %in% y %>% sum %>% prod(x[[1]]))  %>% sum
  count = split_list %>% sapply(function(x) x[[2]] %in% y %>% sum )  %>% sum
  if (count == 0) count = 1
  #print(paste("count:",count))
  #print(paste("score:",score))
  #print(paste("score/count",score/count)) 
  score/count
}
ss = c()
test_size = dim(test)[1]
for (i in 1:test_size) {
  test_file = wk[test[i,4]]
  tt1 = test_file %>% sapply(map_sentment_alan) %>% mean
  ss = c(ss,tt1)
}
index_data_test$tag
t = data.frame(index_data_test$tag[1:test_size],ss)

cor.test(index_data_test$tag[1:test_size],ss,method="pearson")

split_list[[2]][[2]] %in% wk[test[1,4]][1]

