import sys
import subprocess
import modifyProps
import logging

class triggerMlBench:

	def __init__(self):
		self.mod=modifyProps.modProp()
		self.mod.configure()
		FORMAT = '%(asctime)-s-%(levelname)s-%(message)s'
		logging.basicConfig(format=FORMAT,filename='mlbench.log',filemode='w',level='INFO')
		logging.getLogger("requests").setLevel(logging.WARNING)
		self.logger=logging.getLogger(__name__)
		if len(sys.argv)==1:
			self.tests=["lr","als","svm","linear","ridge","kmeans","neclr","necals","neclsvm","neclinear","necridge","neckmeans"]
		else:
			self.tests=sys.argv[1].split(',')

	def runShell(self,cmd):
		try:
			self.logger.info("+Running command {}".format(cmd))
			result=subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
			self.logger.debubg(result)
			self.logger.info("-Finished running command {}".format(cmd))
		except Exception as e:
			self.logger.warn("-Error while running command {}".format(cmd))
			self.logger.warn(e.__str__())

	def benchmark(self):
		self.logger.info('**** Running tests ****')
		FROVEDIS_COMMAND,COMMAND=self.mod.getEnvSettings()
		self.runShell('export FROVEDIS_COMMAND={}'.format(FROVEDIS_COMMAND))
		self.runShell('export COMMAND={}'.format(COMMAND))
		for test in self.tests:
			self.logger.info("+Running {} test".format(test))	
			self.runShell('bin/workloads/ml/{}/prepare/prepare.sh'.format(test))
			self.runShell('bin/workloads/ml/{}/spark/run.sh'.format(test))
			self.logger.info("-Finished running {} test".format(test))	
		self.logger.info('**** Finished tests ****')
		self.logger.info('report/hibench.report','r+').read()

if __name__=='__main__':
	triggerMlBench().benchmark()