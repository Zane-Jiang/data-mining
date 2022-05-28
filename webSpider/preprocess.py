import  re
import jieba

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

#https://blog.csdn.net/qq_29110265/article/details/90769363

stop_words_path = 'source/stopwords.txt'
def clear_character(sentence):
    pattern = re.compile('[^\u4e00-\u9fa5^a-z^A-Z^0-9]')
    line = re.sub(pattern, '', sentence)
    new_sentence = ''.join(line.split())
    return new_sentence

def process(max_nums):
    to_spilt_sentence = []
    for i in range(1,max_nums):
        to_spilt_sentence.append(clear_character(sentence=open('result/news/%d.txt'%i,'r',encoding='utf-8').readline()))
    row_words = [jieba.lcut(s) for s in to_spilt_sentence]
    print(row_words[::])
    print()
    stop_words = set([item.strip() for item in open(stop_words_path, 'r',encoding='utf-8').readlines()])
    words = []
    for row_word in row_words:
        for word in row_word:
            if word in stop_words:
                continue
            else:
                words.append(word)
    return words

def countIdf(corpus):
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    return weight

print(process(100))
