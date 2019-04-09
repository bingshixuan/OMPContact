"""
This program is for Integrate all Feature.

"""

import os, sys
import numpy as np

class IntegrateFeature:
    def __init__(self):
        # Integrate all Feature
        # First the pssm feature, second the betware feature
        self.blastFeature=[]
        self.betawareFeature=[]
        self.relativeFeature=[]
        self.zScoreFeature=[]

        self.pssmFilePath='' # *.pssm
        self.betawareFilePath='' # bataware.out
        self.covariancePath='' # *.txt
        self.svmFilePath=''

    def configure_pssmFilePath(self, pssm):
        self.pssmFilePath=pssm

    def configure_betawarePath(self, betaware):
        self.betawareFilePath=betaware

    def configure_covariancePath(self, covariance):
        self.covariancePath=covariance

    def configure_svmFilePath(self, svm):
        self.svmFilePath=svm

    def Run(self):

        if self.pssmFilePath.strip() == '':
            print('Error, config pssm path')
            self.pssmFilePath=sys.path[0]+'/fastaInput/5WQ8_A.pssm'
            self.dealPssmFile()
        else:
            self.dealPssmFile()

        if self.betawareFilePath.strip() == '':
            print('Error, config betaware file path')
            self.betawareFilePath=self.pssmFilePath.split('.', 1)[0] + '.out'
            self.BetawareFile()
            self.GetRelative()
        else:
            self.BetawareFile()
            self.GetRelative()

        if self.covariancePath.strip() == '':
            print('Error, config covariance file path')
            self.covariancePath=self.pssmFilePath.split('.', 1)[0] + '.txt'
            self.GetZScore()
        else:
            self.GetZScore()

        if self.svmFilePath.strip() == '':
            self.svmFilePath=self.covariancePath.split('.', 1)[0]+'.intxt'

        # deal
        num = len(self.blastFeature)
        covariancecount = len(self.zScoreFeature)
        featurelist = [["0.00" for col in range(3)] for row in range(num)]
        featurematrix = np.array(featurelist)
        for i in range(len(self.blastFeature)):
            featurematrix[i][0] = str(self.blastFeature[i])
            featurematrix[i][1] = self.betawareFeature[i]
            featurematrix[i][2] = self.relativeFeature[i]
        writefile = open(self.svmFilePath, "w+")
        for k in range(1, covariancecount):
            firstpos = self.zScoreFeature[k].split()[0]
            secpos = self.zScoreFeature[k].split()[1]
            covariance = self.zScoreFeature[k].split()[2]
            if  firstpos.isdigit() and int(float(firstpos))==0:
                ahead = " 2:-1 3:-2 4:-1"
                backline = featurematrix[int(firstpos)+1]
                back = " 8:"+backline[0]+" 9:"+backline[1]+" 10:"+backline[2]
            else:
                if  firstpos.isdigit() and int(firstpos) == num-1:
                    back = " 8:-1 9:-2 10:-1"
                else:
                    backline = featurematrix[int(firstpos)+1]
                    back = " 8:"+backline[0]+" 9:"+backline[1]+" 10:"+backline[2]
                aheadline = featurematrix[int(firstpos)-1]
                ahead = " 2:"+aheadline[0]+" 3:"+aheadline[1]+" 4:"+aheadline[2]
            ownline = featurematrix[int(firstpos)]
            own =" 5:"+ownline[0]+" 6:"+ownline[1]+" 7:"+ownline[2]
            if int(secpos) == num-1:
                backofsec = " 17:-1 18:-2 19:-1"
            else:
                backofsecline = featurematrix[int(secpos)+1]
                backofsec = " 17:"+backofsecline[0]+" 18:"+backofsecline[1]+" 19:"+backofsecline[2]
            ownsecline = featurematrix[int(secpos)]
            ownsec =" 14:"+ownsecline[0]+" 15:"+ownsecline[1]+" 16:"+ownsecline[2]
            aheadofsecline = featurematrix[int(secpos)-1]
            aheadofsec = " 11:"+aheadofsecline[0]+" 12:"+aheadofsecline[1]+" 13:"+aheadofsecline[2]
            outelscline = "0 1:"+covariance+ahead+own+back+aheadofsec+ownsec+backofsec
            writefile.write(outelscline+"\n")
        writefile.close()


    def dealPssmFile(self):
        def dealPssmFrequency(lines, position):
            ele1 = str((round((int(lines[position]) / 100), 2)))
            if len(ele1) == 4:
                ele = ele1
            elif len(ele1) == 1:
                ele = ele1 + '.00'
            else:
                ele = ele1 + '0'
            return ele
        
        residuePosition = {"A": 22, "R": 23, "N": 24, "D": 25, "C": 26, "Q": 27, "E": 28, "G": 29, "H": 30, "I": 31,
                           "L": 32, "K": 33, "M": 34, "F": 35, "P": 36, "S": 37, "T": 38, "W": 39, "Y": 40, "V": 41}
        with open(self.pssmFilePath, 'r') as pssmlines:
            for line in pssmlines:
                lines = line.split()
                if len(lines) == 44:
                    residue = lines[1]
                    if residue == "X":
                        outline = '1:0.00'
                    else:
                        position = residuePosition[residue]
                        ele = dealPssmFrequency(lines, position)
                        outline = ele
                    self.blastFeature.append(outline)

    
    def BetawareFile(self):
        betawarestring=''
        with open(self.betawareFilePath, 'r') as betawarelines:
            for lines in betawarelines:
                if len(lines.split()) > 0 and lines.split()[0] == 'SS':
                    lineseq = lines.split()[2]
                    lineseq = lineseq.replace('\n', '')
                    betawarestring = betawarestring + lineseq
            betawarestring = betawarestring.lower()
       
        residuePosition = {"i": 1, "t": 0, "o": -1}
        for i in range(len(betawarestring)):
            position = betawarestring[i]
            self.betawareFeature.append(residuePosition[position])

    # def next
    def GetRelative(self):
        def Prebetaware():
            seq = ''
            with open(self.betawareFilePath, 'r') as betawarelines:
                for lines in betawarelines:
                    if len(lines.split()) > 0 and lines.split()[0] == 'SS':
                        lineseq = lines.split()[2]
                        lineseq = lineseq.replace('\n', '')
                        seq = seq + lineseq
                seq = seq.lower()
            return seq

        topologystring = Prebetaware()
        i = 0
        length = len(topologystring)
        iternum = 0
        while i < length:
            if (i == int(length) - 1):
                self.relativeFeature.append(str(0))
                break
            if topologystring[i] == 't':
                tnum = 1
                while topologystring[i + 1] == 't':
                    tnum = tnum + 1
                    i = i + 1
                    if (i == int(length) - 1):
                        break
                if iternum % 2 == 0:
                    for t in range(1, tnum + 1):
                        self.relativeFeature.append(str(t))
                else:
                    for t in range(1, tnum + 1)[::-1]:
                        self.relativeFeature.append(str(t))
                iternum = iternum + 1
                i = i + 1
            else:
                i = i + 1
                self.relativeFeature.append(str(0))

    # def next

    def GetZScore(self):
        covariancescore = []
        with open(self.covariancePath, 'r') as f:
            covarianceLines = f.readlines()
            for linenum in range(1, len(covarianceLines)):
                covariancescore.append(float(covarianceLines[linenum].split()[2]))
            numarray = np.array(covariancescore)
            meannum = np.mean(numarray)
            stdnum = np.std(numarray)
            
        with open(self.covariancePath, 'r') as covariancelines:
            lines = covariancelines.readlines()
            for i in range(len(lines)):
                if i == 0:
                    zscorereturn = lines[0].replace('\n', '')
                else:
                    zscore = str((float(lines[i].split()[2]) - meannum) / stdnum)
                    zscorereturn = str(lines[i].split()[0]) + ' ' + str(lines[i].split()[1]) + ' ' + zscore
                self.zScoreFeature.append(zscorereturn)


def main():
    a = IntegrateFeature()
    a.Run()


if __name__ =='__main__':
    main()
