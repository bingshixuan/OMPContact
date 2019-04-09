'''
This program is for Run Svm Program.

'''

import os, sys
from RunBlast import RunBlast
from RunBetaware import RunBetaware
from RunConvariance import RunConvariance
from RunMview import RunMview
from IntegrateFeature import IntegrateFeature
from RunSvm import RunSvm

from optparse import OptionParser

class OMPContact:
    def __init__(self):
        # This is the function
        self.options=None
        self.runBlast = RunBlast()
        self.runBetaware = RunBetaware()
        self.runConvariance = RunConvariance()
        self.runMview = RunMview()
        self.slideWindow = IntegrateFeature()
        self.svmPredict = RunSvm()

    def configure_option(self, option):
        self.options=option

    def check_software(self):
        # check java 
        try:
            # try to run java on version
            cmd='java -version'
            os.system(cmd)
        except:
            print('Error to run Java program, please install Java first.')
            return False

        # check svm
        if  os.path.exists('/usr/bin/svm-predict'):
            #
            return True
        elif os.path.exists(sys.path[0]+'/libsvm/svm-predict'):
            self.svmPredict.configure_svmProgramPath(sys.path[0]+'/libsvm/svm-predict ')
        else :
            print('svm program is not cmpiled on this machine.')
            oldpath = os.getcwd() # compile the libsvm
            os.chdir(oldpath+'/libsvm')
            os.system('make ')
            os.chdir(oldpath)
            self.svmPredict.configure_svmProgramPath(sys.path[0]+'/libsvm/svm-predict ')

        return True

    def check_options(self):
        # check options 
        if self.options.methodflag not in ['ELSC', 'MI', 'OMES']:
            print('Error, method should chosen in ELSC, MI, OMES')
            return False
        if not os.path.exists(self.options.inputfile):
            print('Error, a input file should be indicated')
            return False
        if self.options.outputfile == None:
            print('No output file name indicated, use input file name as default name.')
            self.options.outputfile = ''
        return True

    def RunPredict(self):
        self.runBlast.configure_InputFilePath(self.options.inputfile)
        self.runBlast.configure_outPath(self.options.inputfile.split('.',1)[0]+'.fm0')
        self.runBlast.configure_outPssm(self.options.inputfile.split('.',1)[0]+'.pssm')
        self.runBlast.configure_profile(self.options.inputfile.split('.',1)[0]+'.prof')
        self.runBlast.Run()
        self.runBlast.RunProfile()

        self.runBetaware.configure_InputFastaPath(self.options.inputfile)
        self.runBetaware.configure_InputProfilePath(self.options.inputfile.split('.',1)[0]+'.prof')
        self.runBetaware.configure_outPath(self.options.inputfile.split('.',1)[0]+'.out')
        self.runBetaware.Run()

        self.runMview.configure_blastInput(self.options.inputfile.split('.',1)[0]+'.fm0')
        self.runMview.configure_mviewOut(self.options.inputfile.split('.',1)[0]+'.aln')
        self.runMview.configure_convarianceOut(self.options.inputfile.split('.',1)[0]+'.convariance')
        self.runMview.Run()
        self.runMview.ConvertConvariance()

        self.runConvariance.configure_config(self.options.methodflag)
        self.runConvariance.configure_ConvarianceInput(self.options.inputfile.split('.',1)[0]+'.convariance')
        self.runConvariance.configure_ConvarianceOutput(self.options.inputfile.split('.',1)[0]+'.txt')
        self.runConvariance.Run()

        self.slideWindow.configure_pssmFilePath(self.options.inputfile.split('.',1)[0]+'.pssm')
        self.slideWindow.configure_betawarePath(self.options.inputfile.split('.',1)[0]+'.out')
        self.slideWindow.configure_covariancePath(self.options.inputfile.split('.',1)[0]+'.txt')
        self.slideWindow.configure_svmFilePath(self.options.inputfile.split('.',1)[0]+'.intxt')
        self.slideWindow.Run()

        self.svmPredict.configure_modelConfig(self.options.methodflag)
        self.svmPredict.configure_testInputPath(self.options.inputfile.split('.',1)[0]+'.intxt')
        if self.options.outputfile == '':
            self.svmPredict.configure_finalResultPath(self.options.inputfile.split('.',1)[0]+'.pred')#fullpath? 
        else :
            if not self.options.outputfile.startswith('/'):
                self.options.outputfile=sys.path[0] + '/' + self.options.outputfile

            self.svmPredict.configure_finalResultPath(self.options.outputfile)#fullpath?
        self.svmPredict.SvmPredict()
        fileFasta=open(self.options.inputfile)
        line=fileFasta.readline()
        line=fileFasta.readline()
        aminoCount=len(line)
        self.svmPredict.configure_aminoCount(aminoCount)
        if self.options.methodflag == 'ELSC':
            self.svmPredict.configure_value(0.65)
        elif self.options.methodflag == 'MI':
            self.svmPredict.configure_value(0.44)
        elif self.options.methodflag == 'OMES':
            self.svmPredict.configure_value(0.44)
        self.svmPredict.DealResult()



    def Run(self):
        if self.options == None:
            print('Please configure options.')
            return

        if not self.check_software():
            return 

        if self.options.inputfile == None:
            print('No input File, please use -i indicate input file')
            print('eg. python OMPContact.py -i a.fasta ')
            return 

        else :
            if not self.options.inputfile.startswith('/'):
                self.options.inputfile = sys.path[0] + '/' + self.options.inputfile

            if not self.check_options():
                return  
            self.RunPredict()

        os.remove(self.options.inputfile.split('.',1)[0]+'.fm0')
        os.remove(self.options.inputfile.split('.',1)[0]+'.out')
        os.remove(self.options.inputfile.split('.',1)[0]+'.prof')
        os.remove(self.options.inputfile.split('.',1)[0]+'.aln')
        os.remove(self.options.inputfile.split('.',1)[0]+'.convariance')
        os.remove(self.options.inputfile.split('.',1)[0]+'.txt')
        os.remove(self.options.inputfile.split('.',1)[0]+'.pssm')
        os.remove(self.options.inputfile.split('.',1)[0]+'.intxt')


def main():
    usage = 'usage: %prog [option] argument'
    parser = OptionParser(usage)
    parser.add_option('-c', '--method', dest='methodflag', default='ELSC', help='Choose the method of covariance predict.')
    parser.add_option('-i', '--input', type='string', dest='inputfile', help='input the fastafile to be predicted')
    parser.add_option('-o', '--output', type='string', dest='outputfile', help='input the predict file path')
    (options, args) = parser.parse_args()
    omp = OMPContact()
    omp.configure_option(options)
    omp.Run()

if __name__ == '__main__':
    main()
    

    
