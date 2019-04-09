"""

This program is for running mview program.

"""

import os, sys

class RunMview:
  def __init__(self):
    self.MviewProgramPath=''
    self.config=' -in blast -out fasta '
    self.blastInput=''
    self.mviewOut=''
    self.convarianceOut=''

  def configure_MviewPath(self, Mview):
    self.MviewProgramPath=Mview

  def configure_config(self, config):
    self.config=config

  def configure_blastInput(self, blast):
    self.blastInput=blast

  def configure_mviewOut(self, mview):
    self.mviewOut=mview

  def configure_convarianceOut(self, convariance):
    self.convarianceOut=convariance

  def Run(self):
    # Run function
    if self.MviewProgramPath.strip() == '':
      self.MviewProgramPath=sys.path[0]+'/mview/bin/mview '

    if self.blastInput.strip() == '':
      self.blastInput=sys.path[0]+'/fastaInput/5WQ8_A.fm0 '

    if self.mviewOut.strip() == '':
      self.mviewOut=self.blastInput.split('.', 1)[0] + '.aln'

    cmd = self.MviewProgramPath + self.config + self.blastInput + ' > ' + self.mviewOut

    os.system(cmd)

  def ConvertConvariance(self):
    def ConvertViewFormat(mviewpath):
      mviewout = []
      with open(mviewpath, 'r') as mviewfiles:
        ll = []
        lines = mviewfiles.readlines()
        for i in range(len(lines)):
          if lines[i].startswith('>'):
            if ll !=[]:
              new_seq = ''.join(ll)
              mviewout.append(new_seq)
              # print(mviewout)
            mviewout.append(lines[i])
            ll = []
            i += 1
          else:
            line = str(lines[i].strip('\n'))
            ll.append(line)
        new_last = ''.join(ll)
        mviewout.append(new_last)
      return mviewout

    # 
    if self.mviewOut.strip() == '':
      print('Error, No mview out file to generate converiacne file ')
    else :
      if self.convarianceOut.strip() == '':
        self.convarianceOut=self.mviewOut.split('.', 1)[0] + '.convariance'
      
      # 
      mview = ConvertViewFormat(self.mviewOut)
      count = len(mview)
      i = 2
      inputFile = open(self.convarianceOut, 'w')
      while i < count - 1:
        part1 = mview[i].split()[0][1:]
        part2 = mview[i + 1]
        line = part1 + '        ' + part2
        inputFile.write(line+'\n')
        i = i + 2
      inputFile.close()


def main():
  a = RunMview()
  a.Run()
  a.ConvertConvariance()


if __name__ == '__main__':
  main()

