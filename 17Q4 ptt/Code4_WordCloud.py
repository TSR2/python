import os
from os import path
import matplotlib.pyplot as plt
import jieba
from scipy.misc import imread
font=os.path.join(os.path.dirname('/Users/allencheng/Desktop/cwTeXHei-zhonly.ttf'), "cwTeXHei-zhonly.ttf")
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd

ret = open("E:\Python Crawling\web-crawler-tutorial-master\ch2\ptt_tag_V1.csv", "r").read()
seglist = jieba.cut(ret, cut_all=False)
test = " ".join(seglist)
worldcloud1 = WordCloud(font_path = font).generate(test)
plt.imshow(wordcloud1)
plt.axis("off")
plt.show()