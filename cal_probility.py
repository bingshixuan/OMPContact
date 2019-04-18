import os
import numpy as np
from sklearn.metrics import matthews_corrcoef
import sklearn.metrics as metrics
from multiprocessing import Pool


root='C:\\Users\\lenovo\\Desktop\\OMPContact\\Omes\\testing\\'
list = os.listdir(root)

y_all = []
y_all_pred = []

for i in list:
    if i.split('.',1)[0] == i:
        continue
    else:
        y_real = []
        y_pred = []
        f = open(root+i)
        lines = f.readlines()
        f.close()
        for j in lines:
            y_real.append(float(j.split(' ',1)[0]))
        
        f = open(root+i.split('.',1)[0])
        lines = f.readlines()
        f.close()
        for j in lines:
            if 'label' in j:
                continue
            y_pred.append(float(float(j.split(' ',2)[2].split('\\',1)[0])>0.7))
        
        a, b, c, d = metrics.confusion_matrix(y_real, y_pred).ravel()
        print([i, a, b, c, d, metrics.accuracy_score(y_real, y_pred), metrics.precision_score(y_real, y_pred), metrics.recall_score(y_real, y_pred), metrics.f1_score(y_real, y_pred), matthews_corrcoef(y_real, y_pred)])
        y_all.append(y_real)
        y_all_pred.append(y_pred)

y_all=[y for x in y_all for y in x]
y_all_pred=[y for x in y_all_pred for y in x]
a, b, c, d = metrics.confusion_matrix(y_all, y_all_pred).ravel()
print([a, b, c, d, metrics.accuracy_score(y_all, y_all_pred), metrics.precision_score(y_all, y_all_pred), metrics.recall_score(y_all, y_all_pred), metrics.f1_score(y_all, y_all_pred), matthews_corrcoef(y_all, y_all_pred)])
