import os
from card import Card
import json

NO_NAME_ERROR_PROMPT = 'metadata to save must contain a field \'name\''


class FileSystem_Save:
	'''
	save metadata to file system
	metadata: dict that contain field 'name' 
	'''

	@classmethod
	def upsert(cls, metadata, dir_path='.fileSystem_saved_data'): #do later: get a defult name, get dir_path from saver
		'''
		save metadata to file system
		metadata: dict that contain field 'name' 

		'''
		try:
			name = metadata['name']
		except KeyError as error:
			print(NO_NAME_ERROR_PROMPT)
			return

		if not os.path.exists(dir_path):
			os.mkdir(dir_path)
		save_path = os.path.join(dir_path, name)
		try: 
			os.mkdir(card_path) 
		except OSError as error: 
			print(error)
			return
		json_path = os.path.join(save_path, r'metadata.json')
		with open(json_path, "w") as outfile:
			json.dump(metadata, outfile)


		

if __name__ == '__main__':
