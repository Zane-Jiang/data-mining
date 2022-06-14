import math
import os
import re
import shutil

import jieba

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# https://blog.csdn.net/qq_29110265/article/details/90769363
from snownlp import SnowNLP

'''
预处理类
'''


class prepross:
    stop_words_path = 'resource/stopwords.txt'
    base_path = 'result/news'

    def __init__(self, base_path):
        self.base_path = base_path

    '''
    重命名文件，使得文件中出现的数字断档被去除,空白文档被去除
    '''
    def rename(self):
        base_path_src = 'result/row_news'
        base_path_dic = 'result/news'
        num = 1
        for file in os.listdir(base_path_src):
            # os.rename(os.path.join(base_path_src, file), os.path.join(base_path_dic, str(num)) + ".txt")
            content = open(os.path.join(base_path_src, file),'r',encoding='utf-8').readline()
            new_content = "".join(content.split(" "))
            if new_content != "":
                shutil.copyfile(os.path.join(base_path_src, file), base_path_dic + '/' + str(num) + ".txt")
                num = num + 1
        print("共计%d条 文件预处理完毕" % num)
        return num


    '''
    数据预处理，从中获得语料库
    '''

    def process(self, max_nums):
        to_spilt_sentence = []
        for i in range(1, max_nums+1):
            sentence = open('%s//%d.txt' % (self.base_path, i), 'r',encoding='utf-8').readline()
            pattern = re.compile('[^\u4e00-\u9fa5^a-z^A-Z^0-9]')
            line = re.sub(pattern, '', sentence)
            new_sentence = ''.join(line.split())
            to_spilt_sentence.append(new_sentence)
        row_words = [jieba.lcut(s) for s in to_spilt_sentence]
        stop_words = set([item.strip() for item in open(self.stop_words_path, 'r', encoding='utf-8').readlines()])
        corpus = []
        for row_doc in row_words:
            doc = ''
            for word in row_doc:
                if word in stop_words:
                    continue
                else:
                    doc = doc + word + " "
            corpus.append(doc)
        return corpus

    def textRank(self,max_nums):
        row_words = []
        to_spilt_sentence = []
        for i in range(1, max_nums+1):
            sentence = open('%s//%d.txt' % (self.base_path, i), 'r', encoding='utf-8').readline()
            pattern = re.compile('[^\u4e00-\u9fa5^a-z^A-Z^0-9]')
            line = re.sub(pattern, '', sentence)
            new_sentence = ''.join(line.split())
            to_spilt_sentence.append(new_sentence)
            snlp = SnowNLP(new_sentence)
            row_words.append(snlp.keywords(limit=int(len(jieba.lcut(new_sentence))/2)))
        stop_words = set([item.strip() for item in open(self.stop_words_path, 'r', encoding='utf-8').readlines()])
        corpus = []
        for row_doc in row_words:
            doc = ''
            for word in row_doc:
                if word in stop_words:
                    continue
                else:
                    doc = doc + word + " "
            corpus.append(doc)
        return corpus


'''
tf-idf 向量构建
'''





class TFIDF:
    base_path = ''
    '''计算tf-idf向量'''

    def countTfIdf(corpus):
        i = 1
        for doc in corpus:
            print('第 %d 文档分词 %s :' % (i, doc))
            i = i + 1
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(corpus))
        weight = tfidf.toarray()
        return weight

    def getX(corpus):
        i = 1
        for doc in corpus:
            print('第 %d 文档分词 %s :' % (i, doc))
            i = i + 1
        vectorizer = CountVectorizer()
        X =vectorizer.fit_transform(my_prepross.process(max_nums))
        return X

    def getX(self, base_path, max_nums):

        self.base_path = base_path
        my_prepross = prepross(base_path)
        corpus = my_prepross.textRank(max_nums)
        i = 1
        for doc in corpus:
            print('第 %d 文档分词 %s :' % (i, doc))
            i = i + 1
        vectorizer = CountVectorizer()
        X =vectorizer.fit_transform(corpus)
        return X


    ''' 根据语料库获取'''

    def tf_idf_with_textRank(self, base_path, max_nums):

        self.base_path = base_path
        my_prepross = prepross(base_path)
        # return TFIDF.countTfIdf(my_prepross.process(max_nums))
        return TFIDF.countTfIdf(my_prepross.textRank(max_nums))

    def tf_idf(self, base_path, max_nums):

        self.base_path = base_path
        my_prepross = prepross(base_path)
        return TFIDF.countTfIdf(my_prepross.process(max_nums))
        # return TFIDF.countTfIdf(my_prepross.textRank(max_nums))
