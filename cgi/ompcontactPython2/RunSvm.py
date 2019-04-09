"""
This program is for Run Svm Program.

"""

import os, sys

# runLIBSVM': 'svm-train -s 0 -t 2 -h 0 -b 1 C:/Users/jiayj/Desktop/train.txt /home/jiayj267/OMPcontact/svm/MI/10/1/contact1.model'
# svm-train [options] training_set_file [model_file]
# svm-predict  test_file model_file  output_file
#

class RunSvm:
    def __init__(self):
        self.svmProgramPath=''
        self.modelConfig=''
        self.modelPath=''
        self.testInputPath=''
        self.finalRestultPath=''
        self.amino=0
        self.value=0
        # This

    def configure_svmProgramPath(self, programPath):
        self.svmProgramPath=programPath
        # This 

    def configure_modelConfig(self, modelConfig):
        self.modelConfig=modelConfig

    def configure_modelPath(self, modelPath):
        self.modelPath=modelPath

    def configure_testInputPath(self, testFile):
        self.testInputPath=testFile

    def configure_finalResultPath(self, resultPath):
        self.finalRestultPath=resultPath

    def configure_aminoCount(self, count):
        self.amino=count

    def configure_value(self, value):
        self.value=value

    def SvmPredict(self):
        if self.svmProgramPath.strip() == '':
            self.svmProgramPath='libsvm/svm-predict'

        if self.modelConfig.strip() == '':
            self.modelConfig='ELSC'

        if self.modelPath.strip() == '':
            self.modelPath=sys.path[0]+'/model/' + self.modelConfig + 'contact.model'
            
        if self.testInputPath.strip() == '':
            self.testInputPath=sys.path[0]+'/fastaInput/1A0S_P.intxt'

        if self.finalRestultPath.strip() == '':
            self.finalRestultPath=self.testInputPath.split('.', 1)[0] + '.predict.txt'

        cmd = self.svmProgramPath + ' -b 1 ' + self.testInputPath + ' ' + self.modelPath + ' ' + self.finalRestultPath
        os.system(cmd)

        #

    def DealResult(self):
        fileResult = open(self.finalRestultPath)
        lines = fileResult.readlines()
        fileResult.close()
        f = open(self.finalRestultPath.split('.',1)[0] + '.fasta')
        seq = f.readline()
        seq = f.readline()
        seq = seq.replace("\n", "")
        f.close()
        self.amino = len(seq)

        f = open(self.finalRestultPath, 'w')
        lines = lines[1:]
        count = 0

        strResult=''

        for x in range(self.amino+1):
            for y in range(self.amino+1):
                if x == 0 and y == 0:
                    strResult = strResult + '%5.4s' %('')
                elif x == 0 :
                    strResult = strResult + '%5.4s' %(seq[y-1])
                elif y == 0 :
                    strResult = strResult + '%5.4s' %(seq[x-1])
                elif y < x+1 :
                    strResult = strResult + '%5.4s' %('')
                else:
                    strResult = strResult + '%5.4s' %(str(float(lines[count].split(' ', 2)[1])))
                    count = count + 1
                    
            strResult = strResult + '\n'

        f.write(strResult)
        f.close()

        f = open(self.finalRestultPath+'_list', 'w')
        count =0

        result = []
        for x in range(self.amino+1):
            for y in range(self.amino+1):
                if not(x == 0 or y == 0  or y < x + 1):
                    tmp = x, seq[x-1], y, seq[y-1], float(lines[count].split(' ',2)[1])
                    result.append(tmp)
                    count = count + 1

        result_sorted = sorted(result, key=lambda result:result[4], reverse=True)

        strResult='%5s' %('NO') + '|%8s' %('amino') + '|%5s' %('NO') + '|%8s' %('amino') + '|%12s' %('percentage')
        strResult = strResult + '\n'
        for i in result_sorted:
            strResult = strResult + '%5s' %(str(i[0])) + '|%8s' %(i[1]) + '|%5s' %(str(i[2])) + '|%8s' %(i[3]) + '|%12s' %(str(i[4]))
            strResult = strResult + '\n'

        f.write(strResult)
        f.close()


"""   
    def DealResult(self):
        # transalate result file to triangle
        fileResult = open(self.finalRestultPath)
        lines=fileResult.readlines()
        fileResult.close()
        f=open(self.finalRestultPath, 'w')
        lines=lines[1:]
        count=0
        for x in range(self.amino-2):
            for y in range(self.amino-2):
                if y < x:
                    f.write(' '+ ' ')
                else:
                    if float(lines[count].split(' ',2)[1]) > self.value:
                        f.write('1'+' ')
                    else:
                        f.write('0'+' ')
                    count = count + 1
            f.write('\n')

        f.close()
"""

def main():
    a = RunSvm()
    #a.SvmPredict()
    a.configure_finalResultPath('fastaInput/1A0S_P.pred')
    a.DealResult()

if __name__ == '__main__':
    main()



