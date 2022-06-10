import preproces_pkg
from cluster import cluster
from gui import disp
from preproces_pkg import TFIDF
from spider import spdier

if __name__ == '__main__':
    # spider
    # my_spider = spdier()
    # my_spider.get_title(1, 41)#爬虫，获取每条新闻的标题，并保存到文件当中
    # # my_spider.get_link_from_file()
    # my_spider.get_all_news(798, 100000) #获取所有的新闻
    # my_preprocess = preproces_pkg.prepross('result/news') #去除空白，无效新闻
    # max_num = my_preprocess.rename()#重新命名排序新闻，便于统计
    #
    # tf_idf_ = TFIDF().tf_idf(base_path='result/news', max_nums=100)#数据预处理、分词、清洗、并构建向量
    # my_cluster = cluster()
    # my_cluster.kmeans(tf_idf=tf_idf_, num_clusters=3)#kmeans分类

    # my_cluster.db_scan(tf_idf=tf_idf_, eps=0.0000003, min_points=5)

    my_disp = disp()
    my_disp.disp_word_cloud('evaluation/predict/kmeans','kmeans')
    my_disp.disp_word_cloud('evaluation/true', 'true')
    labels = ['表彰活动等','学术活动','文化活动']
    #可视化效果展示
    my_disp.plot_confusion_matrix(labels,'evaluation/true','evaluation/predict/kmeans')

