import shutil

from sklearn.cluster import KMeans, DBSCAN
from sklearn.externals import joblib
import os

class cluster:
    def kmeans(self,tf_idf,num_clusters):
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
        cluster.movefile(self,result, method='kmeans')

    #
    # def pca(self, weight, n_components=2):
    #     """
    #     PCA对数据进行降维
    #     :param weights:
    #     :param n_components:
    #     :return:
    #     """
    #     pca = PCA(n_components=n_components)
    #     print('pca done')
    #     #pca = KernelPCA(kernel="rbf",n_components=n_components)
    #     return pca.fit_transform(weight)



    def movefile(self,clusters_result,method):
            souce_path = 'result/news/'
            # dic_path = 'result/clusters'
            for file in os.listdir('result'):
                if file == method:
                    shutil.rmtree('result\\'+file)
                    # print("删除文件%s"%file)

            filepaths = []
            # print(clusters_result)
            try:
                os.mkdir('result/'+method+'/')
            except FileExistsError as  f:
                print(f)
            for i in range(0, len(clusters_result)-1):
                filepath = 'result/'+method+'/'+str(clusters_result[i])
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