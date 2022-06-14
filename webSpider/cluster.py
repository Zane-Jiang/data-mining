import shutil

from lda import lda
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.externals import joblib
import os

class cluster:
    def kmeans(self,tf_idf,num_clusters,dic_path,subfile_name):
        km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40,
                            init='k-means++', n_jobs=-1)
        '''
        n_clusters: 指定K的值
        max_iter: 对于单次初始值计算的最大迭代次数
        n_init: 重新选择初始值的次数
        init: 制定初始值选择的算法
        n_jobs: 进程个数，为-1的时候是指默认跑满CPU,注意，这个对于单个初始值的计算始终只会使用单进程计算，并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40,  服务器上面有20个CPU可以开40个进程，最终只会开10个进程
        '''
        # 返回各自文本的所被分配到的类索引
        result = km_cluster.fit_predict(tf_idf)
        print("Kmeans文件分类完毕\n%s" % result)
        cluster.movefile(self,result,dic_path=dic_path, subfile_name=subfile_name)



    def lda(self,X,num_clusters,dic_path,subfile_name):
        model = lda.LDA(n_topics=num_clusters, n_iter=500, random_state=1)
        model.fit(X)
        doc_topic = model.doc_topic_
        result = []
        for n in range(doc_topic.shape[0]):
            result.append(doc_topic[n].argmax())
        print(result)
        cluster.movefile(self, result, dic_path=dic_path, subfile_name=subfile_name)

        # lda = LatentDirichletAllocation(
        #     n_components=num_clusters, max_iter=50,
        #     learning_method='online',
        #     learning_offset=50.,
        #     random_state=0)
        # x = lda.fit(tf_idf)
        #
        # for adoc in lda.components_:
        #     # print(max(adoc))
        #     i = 0
        #     for a in adoc:
        #         i = i +1
        #         print((str)(i)+"    "+str(adoc))

        # print(lda.n_components)




    def movefile(self,clusters_result,dic_path,subfile_name):
            souce_path = 'result/news/'
            # dic_path = 'result/clusters'
            for file in os.listdir(dic_path):
                if file == subfile_name:
                    shutil.rmtree(dic_path+"/"+file)

            filepaths = []
            try:
                os.mkdir(dic_path+'/'+subfile_name+'/')
            except FileExistsError as  f:
                print(f)
            for i in range(0, len(clusters_result)):
                filepath = dic_path+"/"+subfile_name+'/'+str(clusters_result[i])
                if filepath in filepaths:
                    shutil.copyfile(souce_path+str(i+1)+".txt", filepath+'/'+str(i+1) + ".txt")
                else:
                    filepaths.append(filepath)
                    try:
                        os.mkdir(filepath)
                    except OSError:
                        shutil.rmtree(filepath)
                        print("删除原文件: %s"%filepath)
                        os.mkdir(filepath)
                        print("创建文件成功: %s"%filepath)
                    shutil.copyfile(souce_path+str(i+1)+".txt", filepath+'/'+str(i+1) + ".txt")
            print('文件移动完毕')

    def db_scan(self,tf_idf,eps,min_points):
        dbscan = DBSCAN(eps=eps,min_samples=min_points)
        result = dbscan.fit_predict(tf_idf)
        print("db_scan文件分类完毕\n%s" % result)
        cluster.movefile(self,result, method='db_scan')