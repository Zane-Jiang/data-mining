# from sklearn.metrics import confusion_matrix
# import numpy as np
# import itertools
# import matplotlib.pyplot as plt
# class disp:
#     def plot_confusion_matrix(self,cm, target_names,title='Confusion matrix',cmap=None,normalize=False):
#         accuracy = np.trace(cm) / float(np.sum(cm)) #����׼ȷ��
#         misclass = 1 - accuracy #���������
#         if cmap is None:
#             cmap = plt.get_cmap('Blues') #��ɫ���ó���ɫ
#         plt.figure(figsize=(10, 8)) #���ô��ڳߴ�
#         plt.imshow(cm, interpolation='nearest', cmap=cmap) #��ʾͼƬ
#         plt.title(title) #��ʾ����
#         plt.colorbar() #������ɫ��
#         if target_names is not None:
#             tick_marks = np.arange(len(target_names))
#             plt.xticks(tick_marks, target_names, rotation=45) #x�����ǩ��ת45��
#             plt.yticks(tick_marks, target_names) #y����
#         if normalize:
#             cm = cm.astype('float32') / cm.sum(axis=1)
#             cm = np.round(cm,2) #�����ֱ�����λС��
#         thresh = cm.max() / 1.5 if normalize else cm.max() / 2
#         for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])): #��cm.shape[0]��cm.shape[1]�е�Ԫ�����Ԫ�飬����Ԫ����ÿһ������
#             if normalize: #��׼��
#                 plt.text(j, i, "{:0.2f}".format(cm[i, j]), #������λС��
#                         horizontalalignment="center",  #�����ڷ����м�
#                         color="white" if cm[i, j] > thresh else "black")  #����������ɫ
#             else:  #�Ǳ�׼��
#                 plt.text(j, i, "{:,}".format(cm[i, j]),
#                         horizontalalignment="center",  #�����ڷ����м�
#                         color="white" if cm[i, j] > thresh else "black") #����������ɫ
#
#         plt.tight_layout() #�Զ�������ͼ����,ʹ֮�������ͼ������
#         plt.ylabel('True label') #y�����ϵı�ǩ
#         plt.xlabel("Predicted label\naccuracy={:0.4f}\n misclass={:0.4f}".format(accuracy, misclass)) #x�����ϵı�ǩ
#         plt.show() #��ʾͼƬ
#         labels = ['NORMAL','PNEUMONIA']
#         # Ԥ����֤����������׼ȷ��
#         Y_pred = model.predict_generator(test_data_gen, total_test // batch_size + 1)
#         # ��Ԥ��Ľ��ת��Ϊone hit����
#         Y_pred_classes = np.argmax(Y_pred, axis = 1)
#         # �����������
#         confusion_mtx = confusion_matrix(y_true = test_data_gen.classes,y_pred = Y_pred_classes)
#         # ���ƻ�������
#         plot_confusion_matrix(confusion_mtx, normalize=True, target_names=labels)
