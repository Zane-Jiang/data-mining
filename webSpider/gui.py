import os
import re
import shutil

import jieba
import wordcloud
from sklearn.metrics import confusion_matrix
import numpy as np
import itertools
import preproces_pkg
import matplotlib.pyplot as plt
class disp:
    stop_words_path = 'resource/stopwords.txt'
    def get_pridict_lable(self,true_path,predict_path):
        '''
        根据输入地址与输出地址，确定混淆矩阵的输入数组
        :param true_path:
        :param predict_path:
        :return:
        '''
        x_true = []
        for cluster_ in os.listdir(true_path):
            for item in os.listdir(true_path+"\\"+cluster_):
                x_true.append(cluster_)
        y_pridict = []
        for cluster_ in os.listdir(predict_path):
            for item in os.listdir(predict_path + "\\" + cluster_):
                y_pridict.append(cluster_)
        xy = []
        xy.append(x_true)
        xy.append(y_pridict)
        return xy

    def get_confusion_matrix(self,xy):
        x_true = xy[0]
        y_predict = xy[1]
        print(xy)

        return confusion_matrix(x_true,y_predict)


    def process(self,basepath):
        to_spilt_sentence = []
        for file in os.listdir(basepath):
            sentence = open(basepath+'/'+file, 'r',encoding='utf-8').readline()
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


    def disp_word_cloud(self,basepath,dir_name):
        savepath = 'evaluation/wordcloud'
        try:
            shutil.rmtree(savepath+'/'+dir_name)
        except FileNotFoundError:
            print('创建词云图文件ing')
        print('更新词云图文件ing')
        os.mkdir(savepath+'/'+dir_name)
        for file in os.listdir(basepath):
            w = wordcloud.WordCloud(font_path='evaluation/wordcloud/simhei.ttf')
            text = ''.join(self.process(basepath+"/"+file))
            print(text)
            w.generate(text)

            w.to_file(savepath+'/'+dir_name+"/"+file+"_wordcloud.png")


    #引用
    def plot_confusion_matrix(self,target_names,true_path,predict_path,title,save_fig_path,xlable,ylable,cmap=None,normalize=False):
        xy=self.get_pridict_lable(true_path,predict_path)
        confusionMatrix = self.get_confusion_matrix(xy)
        accuracy = np.trace(confusionMatrix) / float(np.sum(confusionMatrix)) #计算准确率
        misclass = 1 - accuracy #计算错误率
        if cmap is None:
            cmap = plt.get_cmap('Blues') #颜色设置成蓝色

        plt.figure(figsize=(7,6)) #设置窗口尺寸
        plt.imshow(confusionMatrix, interpolation='nearest', cmap=cmap) #显示图片
        plt.title(title) #显示标题
        plt.colorbar() #绘制颜色条
        plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
        plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
        if target_names is not None:
            tick_marks = np.arange(len(target_names))
            plt.xticks(tick_marks, target_names, rotation=45) #x坐标标签旋转45度
            plt.yticks(tick_marks, target_names) #y坐标
        if normalize:
            confusionMatrix = confusionMatrix.astype('float32') / confusionMatrix.sum(axis=1)
            confusionMatrix = np.round(confusionMatrix,2) #对数字保留两位小数
        thresh = confusionMatrix.max() / 1.5 if normalize else confusionMatrix.max() / 2
        for i, j in itertools.product(range(confusionMatrix.shape[0]), range(confusionMatrix.shape[1])): #将cm.shape[0]、cm.shape[1]中的元素组成元组，遍历元组中每一个数字
            if normalize: #标准化
                plt.text(j, i, "{:0.2f}".format(confusionMatrix[i, j]), #保留两位小数
                        horizontalalignment="center",  #数字在方框中间
                        color="white" if confusionMatrix[i, j] > thresh else "black")  #设置字体颜色
            else:  #非标准化
                plt.text(j, i, "{:,}".format(confusionMatrix[i, j]),
                        horizontalalignment="center",  #数字在方框中间
                        color="white" if confusionMatrix[i, j] > thresh else "black") #设置字体颜色

        plt.tight_layout() #自动调整子图参数,使之填充整个图像区域
        plt.ylabel(ylable) #y方向上的标签
        plt.xlabel(xlable+"\n accuracy={:0.4f}\n misclass={:0.4f}".format(accuracy, misclass)) #x方向上的标签
        plt.savefig(save_fig_path+"/"+title+".jpg",bbox_inches = 'tight')
        plt.show() #显示图片






