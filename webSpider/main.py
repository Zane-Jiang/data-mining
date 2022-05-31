from cluster import cluster
from preprocess import TFIDF
import preprocess
from spider import spdier

# my_spider = spdier()
# # my_spider.get_title(1,41)
# my_spider.get_link_from_file()
# # break point download
# my_spider.get_all_news(368,100000)
# preprocess.rename()
tf_idf = TFIDF.tf_idf(base_path='result/news', max_nums=378)
pridict = cluster.kmeans(tf_idf=tf_idf,num_clusters=5)
print("文件分类完毕%s"%pridict)
cluster.movefile(pridict,method='kmeans')

# [0 2 0 1 1 1 1 3 1]
# [3 2 3 1 1 1 1 0 1]




