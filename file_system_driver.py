import os
from card import Card
import json
from pathlib import Path
from furl import furl

DEFULT_OBG_NAME = 'unamed_file' # +{number of unamed}
METADATA_PATH_SUFIX = 'metadata'

class FileSystem_Driver:
	'''
	save metadata to file system
	metadata: dict that contain field 'name' 
	'''
	def __init__(self, dir_path, unamed_ctr=0):
		self.dir_path = dir_path
		if not os.path.isdir(self.dir_path):
			os.mkdir(self.dir_path)
		self.unamed_ctr = unamed_ctr
	
	@classmethod
	def create_from_url(cls, url):
		url = furl(url)
		assert url.scheme == 'filesystem'
		return FileSystem_Driver(str(url.path), url.args.get('unamed_ctr', 0))

	def upsert(self, metadata): 
		'''
		upsert metadata to file system
		metadata: dict that contain field 'name' 

		'''
		name = metadata.get('name', DEFULT_OBG_NAME)
		if name == DEFULT_OBG_NAME:  #names unamed objects with a (defult name) + (index) 
			name += str(self.unamed_ctr)
			self.unamed_ctr += 1

		save_path = os.path.join(self.dir_path, name)
		if not os.path.isdir(save_path):
			os.mkdir(save_path)
		json_path = os.path.join(save_path, METADATA_PATH_SUFIX + '.json')
		with open(json_path, "w") as outfile:
			json.dump(metadata, outfile)


		

if __name__ == '__main__':
	pass
