import math
import os
import re
import jieba
import numpy as np
from sklearn.externals import joblib

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


# https://blog.csdn.net/qq_29110265/article/details/90769363


#重命名文件，使得文件中出现的数字断档被去除
def rename():
    base_path_src = 'result/row_news'
    base_path_dic = 'result/news'
    num = 1
    for file in os.listdir(base_path_src):
        os.rename(os.path.join(base_path_src,file),os.path.join(base_path_dic,str(num))+".txt")
        num = num + 1
    print("共计%d条"%num)



class TFIDF:
    stop_words_path = 'resource/stopwords.txt'
    base_path = ''
    def clear_character(sentence):
        pattern = re.compile('[^\u4e00-\u9fa5^a-z^A-Z^0-9]')
        line = re.sub(pattern, '', sentence)
        new_sentence = ''.join(line.split())
        return new_sentence


    def process(max_nums):
        to_spilt_sentence = []
        for i in range(1, max_nums):
            to_spilt_sentence.append(
               TFIDF.clear_character(sentence=open('%s//%d.txt' % (TFIDF.base_path,i), 'r', encoding='utf-8').readline()))
        row_words = [jieba.lcut(s) for s in to_spilt_sentence]
        stop_words = set([item.strip() for item in open(TFIDF.stop_words_path, 'r', encoding='utf-8').readlines()])
        corpus = []
        for row_doc in row_words:
            doc = ''
            for word in row_doc:
                if word in stop_words:
                    continue
                else:
                    doc = doc + word +" "
            corpus.append(doc)
        return corpus


    def countTfIdf(corpus):
        # print("aaa%s"%corpus)
        i = 1
        for doc in corpus:
            print('第 %d 文档分词 %s :'%( i,doc))
            i = i + 1
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(corpus))
        weight = tfidf.toarray()
        # print(weight[:1])
        # joblib.dump(tfidf_vectorizer, 'tfidf_fit_result.pkl')
        return weight
    def tf_idf(base_path,max_nums):
            TFIDF.base_path = base_path
            return TFIDF.countTfIdf(TFIDF.process(max_nums))




