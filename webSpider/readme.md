# 好的参数设置
## kmeans
```python
tf_idf = TFIDF.tf_idf(base_path='result/news', max_nums=378)
pridict = cluster.kmeans(tf_idf=tf_idf,num_clusters=5)
print("文件分类完毕%s"%pridict)
cluster.movefile(pridict,method='kmeans')
```
