import os

import preproces_pkg
from cluster import cluster
from gui import disp
from preproces_pkg import TFIDF
from spider import spdier


def rename(path, table):
    for file in os.listdir(path):
        for i in range(0, 4):
            if file == str(i):
                os.rename(path + "/" + file, path + "/" + table[i])


if __name__ == '__main__':
    # spider
    # my_spider = spdier()
    # my_spider.get_title(1, 41)#爬虫，获取每条新闻的标题，并保存到文件当中
    # # my_spider.get_link_from_file()
    # my_spider.get_all_news(798, 100000) #获取所有的新闻
    # my_preprocess = preproces_pkg.prepross('result/news') #去除空白，无效新闻
    # max_num = my_preprocess.rename()#重新命名排序新闻，便于统计


    my_cluster = cluster()
    my_disp = disp()

    my_disp.disp_word_cloud(basepath='evaluation/true', dir_name='true')
    labels = ['学术报告', '党建会议', '课堂教学与专业建设', "学生与文化活动"]
    # rename("evaluation/predict/kmeans_with_tf_idf", ["学术会议", "党政", "专业建设", "学生活动"])

    # #tf-idf
    # tf_idf_ = TFIDF().tf_idf(base_path='result/news', max_nums=100)  # 数据预处理、分词、清洗、并构建向量
    # my_cluster.kmeans(tf_idf=tf_idf_, dic_path="evaluation/predict",subfile_name="kmeans_with_tf_idf",num_clusters=4)#kmeans分类
    my_disp.disp_word_cloud(basepath='evaluation/predict/kmeans_with_tf_idf', dir_name='kmeans_with_tf_idf')
    #
    # #tf_idf_with_textRank
    # tf_idf_with_textRank = TFIDF().tf_idf_with_textRank(base_path='result/news', max_nums=100)  # 数据预处理、分词、清洗、并构建向量
    # my_cluster.kmeans(tf_idf=tf_idf_with_textRank, dic_path="evaluation/predict", subfile_name="kmeans_with_tf_idf_textRank",num_clusters=4)  # kmeans分类
    my_disp.disp_word_cloud(basepath='evaluation/predict/kmeans_with_tf_idf_textrank',
                            dir_name='kmeans_with_tf_idf_textrank')

    # lda
    # my_cluster.lda(X=TFIDF().getX(base_path='result/news', max_nums=100), num_clusters=4, dic_path="evaluation/predict",subfile_name="lda")
    my_disp.disp_word_cloud(basepath='evaluation/predict/lda', dir_name='lda')

    # ##可视化效果展示
    # #人工与kmeans  tf-idf
    my_disp.plot_confusion_matrix(labels, true_path='evaluation/true', title="kmeans_with_tf_idf",
                                  predict_path='evaluation/predict/kmeans_with_tf_idf', xlable="kmeans_with_tf_idf",
                                  ylable="人工分类", save_fig_path="evaluation/confusion_matrix")

    # #人工与kmeans tf-idf textrank
    my_disp.plot_confusion_matrix(labels, true_path='evaluation/true', title="kmeans_with_tf_idf_textRank",
                                  predict_path='evaluation/predict/kmeans_with_tf_idf_textRank',
                                  xlable="kmeans_with_tf_idf_textRank", ylable="人工分类",
                                  save_fig_path="evaluation/confusion_matrix")

    # 人工与kmeans tf-idf lda
    my_disp.plot_confusion_matrix(labels, true_path='evaluation/true', title="tf-idf lda",
                                  predict_path='evaluation/predict/lda', xlable="lda", ylable="人工分类",
                                  save_fig_path="evaluation/confusion_matrix")



#500篇结果比较