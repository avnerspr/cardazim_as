import os
from card import Card
import json
from pathlib import Path
from furl import furl

DEFULT_OBG_NAME = 'unamed_file' # +{number of unamed}
DEFULT_CREATOR = 'unknown_creator'
METADATA_PATH_SUFIX = 'metadata.json'

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
		creator = metadata.get('creator', DEFULT_CREATOR)

		save_path = os.path.join(self.dir_path, creator, name)
		os.makedirs(save_path, exist_ok=True)
		json_path = os.path.join(save_path, METADATA_PATH_SUFIX)
		try:
			with open(json_path, "w") as outfile:
				json.dump(metadata, outfile)
		except:
			os.rmdir(save_path)
			raise RuntimeError('unable to save metadata') 

	def key_values(self, key: str):
		if key == 'creator':
			return self.creators()
		if key == 'name':
			return self.names()

		vals = set()
		for root, dirs, files in os.walk(self.dir_path):
			for file in files:
				with open(file, 'r') as metadata_file:
					metadata = json.loads(metadata_file.read())
				if key in metadata.keys():
					vals.add(metadata[key])
		return vals

	def creators(self):
		return list(os.listdir(self.dir_path))

	def names(self):
		ans = set()
		for creator in os.listdir(self.dir_path):
			creator_path = os.join(self.dir_path, creator)
			ans.update(os.listdir(creator_path))
		return list(ans)

	def find_many(self, filter):
		ans = list()
		for root, dirs, files in os.walk(self.dir_path):
			for file_name in files:
				file_path = os.path.join(root, file_name)
				with open(file_path, 'r') as metadata_file:
					doc = json.loads(metadata_file.read())
				if check_filter(doc, filter):
					ans.append(doc)
		return list(ans)

	def get_metadata(self, name: str, creator: str):
		card_path = os.path.join(self.dir_path, creator, name, METADATA_PATH_SUFIX)
		with open(card_path, 'r') as metadata_file:
			return json.loads(metadata_file.read())

def check_filter(doc, filter):
	return set(filter.items()).issubset(set(doc.items()))
		

if __name__ == '__main__':
	pass
