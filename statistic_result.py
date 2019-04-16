# This is code is used to statistic the OMPContact test Result On 210.47.18.43
# It could fit in the local as the reference.
# 

import numpy as np
from sklearn.metrics import matthews_corrcoef
import sklearn.metrics as metrics
from multiprocessing import Pool

import os

mol = ["ELSC", "MI", "Omes"]

def predict(inputfile, outputfile):
    # add code here
    cmd = "./svm-predict " + inputfile + " model/ELSCcontact.model " + outputfile
    os.system(cmd)

    f = open(inputfile)
    lines = f.readlines()
    f.close()
    y_real = []
    for i in lines:
        y_real.append(float(i.split(' ',1)[0]))

    f = open(outputfile)
    lines = f.readlines()
    f.close()
    y = []
    for i in lines:
        y.append(float(i.split('\r', 1)[0]))

    f = open(outputfile, 'w')
    a, b, c, d = metrics.confusion_matrix(y_real, y).ravel()
    f.write([metrics.accuracy_score(y_real, y), a, b, c, d, metrics.precision_score(y_real, y), metrics.recall_score(y_real, y), metrics.f1_score(y_real, y), matthews_corrcoef(y_real, y)])
    f.close()

if __name__ == '__main__':
    rootdir = '/home/jiayj/OMPContact/ELSC/testing/'
    list = os.listdir(rootdir)
    p = Pool(len(list))
    for i in range(len(list)):
        p.apply_async(predict, args=(os.path.join(rootdir, list[i]), os.path.join(rootdir, list[i]).split('.',1)[0]))

    p.close()
    p.join()

