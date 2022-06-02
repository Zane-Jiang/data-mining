import preproces_pkg
from cluster import cluster
from preproces_pkg import TFIDF
from spider import spdier

if __name__ == '__main__':
    # spider
    # my_spider = spdier()
    # my_spider.get_title(1, 41)
    # my_spider.get_link_from_file()
    # my_spider.get_all_news(798, 100000)
    my_preprocess = preproces_pkg.prepross('result/news')
    my_preprocess.rename()
    tf_idf_ = TFIDF().tf_idf(base_path='result/news', max_nums=300)
    my_cluster = cluster()
    my_cluster.kmeans(tf_idf=tf_idf_, num_clusters=5)
    my_cluster.db_scan(tf_idf=tf_idf_, eps=0.003, min_points=5)
