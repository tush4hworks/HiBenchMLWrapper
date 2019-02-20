import sys
import shlex
import json

class modProp:
	def __init__(self):
		with open('params.json') as runSet:
			self.params=json.load(runSet)

	def modifyProperties(self,filepath,propDict):
		try:
			f=open(filepath,'r+')
			existingProps=[line.strip(' \n') for line in f.readlines()]
			f.close()
			w=open(filepath,'w+')
			for prop in existingProps:
				try:
					if not prop.strip(' \n'):
						w.write('\n')
						continue
					if prop.startswith('#') or not len(shlex.split(prop))==2 or '"' in prop:
						w.write(prop+'\n')
						continue
					key,val=shlex.split(prop)
					if key in propDict.keys():
						val=propDict[key]
					w.write('{}    {}'.format(key,val)+'\n')
				except Exception as e:
					print e.__str__()
			w.close()
		except Exception as e:
			print e.__str__()

	def getEnvSettings(self):
		return [self.params['environment']['FROVEDIS_COMMAND'],self.params['environment']['COMMAND']]

	def configure(self):
		for conf in self.params['wrap']:
			self.modifyProperties(conf['filepath'],conf['properties'])


