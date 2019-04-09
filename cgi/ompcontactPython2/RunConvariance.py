"""
This program is for running Convariance program.

"""

import sys, os

class RunConvariance:
    def __init__(self):
        #
        self.convarianceProgramPath=''
        self.convarianceInput=''
        self.convarianceOut=''
        self.config=''

    def configure_convarianceProgramPath(self, convarianceProgram):
        self.convarianceProgramPath=convarianceProgram

    def configure_config(self, config):
        self.config=config

    def configure_ConvarianceInput(self, convarianceinput):
        self.convarianceInput=convarianceinput

    def configure_ConvarianceOutput(self, convarianceOutput):
        self.convarianceOut=convarianceOutput

    def Run(self):
        if self.convarianceProgramPath.strip() == '':
            self.convarianceProgramPath='covariance.algorithms.'

        if self.convarianceInput.strip() == '':
            self.convarianceInput=sys.path[0] + '/fastaInput/5WQ8_A.convariance.fasta '

        if self.convarianceOut.strip() == '':
            self.convarianceOut=self.convarianceInput.split('.', 1)[0] + '.txt'

        if self.config.strip() == '':
            self.config='ELSC'

        cmd = 'java ' + self.convarianceProgramPath + self.config + 'Covariance ' + self.convarianceInput + ' ' + self.convarianceOut

        os.system(cmd)

def main():
    a = RunConvariance()
    a.Run()


if __name__ == '__main__':
    main()
