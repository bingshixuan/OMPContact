"""

This program is for running Blast program.

s.strip()==''

programPath + config + dbPath + inputFilePath + out + outPssm
"""

import sys, os
from numpy import *

class RunBlast:
  def __init__(self):
    self.BlastProgramPath=''
    self.InputFilePath=''
    self.config=' -evalue 0.001 -num_iterations 3 -outfmt 0 '
    self.dbPath='' # /home/songjz671/blast/db/uniprot -query 
    self.outPssm='' #  -out_ascii_pssm /home/jiayj267/test3.0/3HW9_A.pssm 
    self.out='' # -out /home/jiayj267/test3.0/3HW9_A.fm0 
    # setting for profile 
    self.profilePath=''
    
    
  def configure_BlastProgramPath(self, BlastPath):
    self.BlastProgramPath=BlastPath
    
  def configure_InputFilePath(self, InputFilePath):
    self.InputFilePath=InputFilePath
    
  def configure_config(self, config):
    self.config=config
    
  def configure_dbPath(self, db):
    self.dbPath=db
    
  def configure_outPath(self, out):
    self.out=out
    
  def configure_outPssm(self, pssm):
    self.outPssm=pssm

  def configure_profile(self, profile):
    self.profilePath=profile
    
  def Run(self):
    if self.BlastProgramPath.strip() == '':
      self.BlastProgramPath=sys.path[0]+'/blast/bin/psiblast '
      
    if  self.dbPath.strip() == '':
      self.dbPath=sys.path[0] + '/blast/db/uniprot -query '

    if  self.InputFilePath.strip() == '':
      self.InputFilePath=sys.path[0]+'/fastaInput/5WQ8_A.fasta '
      
    if  self.out.strip() == '':
      self.out=self.InputFilePath.split('.', 1)[0] + '.fm0'
#      self.out=' -out ' + sys.path[0] + '/fm/' + self.InputFilePath.split('.', 1)[0] + '.fm0'

    if self.outPssm.strip() == '':
      self.outPssm=self.InputFilePath.split('.', 1)[0] + '.pssm'
    
    #cmd = self.BlastProgramPath + self.config + self.dbPath + self.InputFilePath + self.out + self.outPssm
    cmd = self.BlastProgramPath + self.config + ' -db ' + self.dbPath + self.InputFilePath + ' -out ' + self.out + ' -out_ascii_pssm ' + self.outPssm

    os.system(cmd)
    
  def RunProfile(self):
    def calculate(pssmpath, profilepath):
      with open(pssmpath, 'r') as pssmlines:
        pssmlist = []
        newFile = open(profilepath, 'w+')
        for pssmline in pssmlines:
          content = pssmline.split()
          if len(content) == 44:
            linelist = []
            for i in range(22, 42):
              linelist.append(float(content[i]))
            pssmlist.append(linelist)
        pssmMatrix = array(pssmlist)
        linenum, colnum = pssmMatrix.shape
        for a in range(linenum):
          for b in range(colnum):
            if b != colnum - 1:
              pssmMatrix[a, b] = pssmMatrix[a, b] / 100
              c = '%.2f' % pssmMatrix[a, b]
              # pssmMatrix[a, b] = c
              newFile.write(str(c))
              newFile.write(' ')

            else:
              pssmMatrix[a, b] = pssmMatrix[a, b] / 100
              c = '%.2f' % pssmMatrix[a, b]
              # pssmMatrix[a, b] = c
              newFile.write(str(c))
              newFile.write('\n')
        newFile.close()

    if self.outPssm.strip() == '':
      print('Error, No Pssm to generate Profile file')
    else :
      # The following code is from pssm to profile code
      if self.profilePath.strip() == '':
        self.profilePath=self.InputFilePath.split('.', 1)[0] + '.prof'
        
      calculate(self.outPssm, self.profilePath) 

      # go on call another function


    
def main():
  
  a = RunBlast()
  a.Run()
  a.RunProfile()
  
if __name__  == '__main__':
  main()
    
