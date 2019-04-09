"""
This program is for running betaware program.

"""

import os, sys

class RunBetaware:
  def __init__(self):
    self.BetawareProgramPath=''
    self.inputFastaPath=''
    self.config=' -t '
    self.inputProfilePath=''
    self.out=''

  def configure_BetawarePath(self, BetawarePath):
    self.BetawareProgramPath=BetawarePath

  def configure_InputFastaPath(self, fastaPath):
    self.inputFastaPath=fastaPath

  def configure_config(self, config):
    self.config=config

  def configure_InputProfilePath(self, profilePath):
    self.inputProfilePath=profilePath

  def configure_outPath(self, out):
    self.out=out

  def Run(self):
    if self.BetawareProgramPath.strip() == '':
      self.BetawareProgramPath=sys.path[0]+'/betaware/bin/betaware.py '

    if self.inputFastaPath.strip() == '':
      self.inputFastaPath=sys.path[0] + '/fastaInput/5WQ8_A.fasta '

    if self.inputProfilePath.strip() == '':
      self.inputProfilePath=self.inputFastaPath.split('.', 1)[0]+ '.prof '

    if self.out.strip() == '':
      self.out =self.inputFastaPath.split('.', 1)[0] + '.out'

    cmd = 'export BETAWARE_ROOT=' + sys.path[0] + '/betaware'
    os.system(cmd)

    cmd = 'python ' + self.BetawareProgramPath + self.config +  ' -o '  + self.out + ' -f ' + self.inputFastaPath + ' -p ' + self.inputProfilePath
    os.system(cmd)


def main():
  a = RunBetaware()
  a.Run()

if __name__ == '__main__':
  main()
