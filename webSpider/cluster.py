import shutil

from sklearn.cluster import KMeans
from sklearn.externals import joblib
import os

class cluster:
    def kmeans(tf_idf,num_clusters):
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
        return result

        # print("Predicting result:", result)
        # '''
        # 每一次fit都是对数据进行拟合操作，
        # 所以我们可以直接选择将拟合结果持久化，
        # 然后预测的时候直接加载，进而节省时间。
        # '''
        #
        # # joblib.dump(tfidf_vectorizer, 'tfidf_fit_result.pkl')
        # joblib.dump(km_cluster, 'km_cluster_fit_result.pkl')
        #
        # # 程序下一次则可以直接load
        # # tfidf_vectorizer = joblib.load('tfidf_fit_result.pkl')
        # km_cluster = joblib.load('km_cluster_fit_result.pkl')
    def movefile(clusters_result,method):
            souce_path = 'result/news/'
            # dic_path = 'result/clusters'
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
                    except FileExistsError:
                        continue
                    shutil.copyfile(souce_path+str(i+1)+".txt", filepath+'/'+str(i+1) + ".txt")
            print('文件移动完毕')



