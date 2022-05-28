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
    vectorizer=CountVectorizer()#����Ὣ�ı��еĴ���ת��Ϊ��Ƶ���󣬾���Ԫ��a[i][j] ��ʾj����i���ı��µĴ�Ƶ
    transformer=TfidfTransformer()#�����ͳ��ÿ�������tf-idfȨֵ
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#��һ��fit_transform�Ǽ���tf-idf���ڶ���fit_transform�ǽ��ı�תΪ��Ƶ����
    weight=tfidf.toarray()#��tf-idf�����ȡ������Ԫ��a[i][j]��ʾj����i���ı��е�tf-idfȨ��
    return weight

print(process(100))
