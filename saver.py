import os
from card import Card
import json
from pathlib import Path
from furl import furl
from file_system_driver import FileSystem_Driver
from mongodb_driver import MongoDB_Driver

DEFULT_IMAGE_DIR = r'cards_images/'
METADATA_FIELDS = ['name', 'creator', 'riddle', 'solution', 'image_path']

drivers = {
	'filesystem' : FileSystem_Driver,
	'mongodb' : MongoDB_Driver
	}


class Saver:

	def __init__(self, database_url, image_dir=DEFULT_IMAGE_DIR):
		self.driver = get_driver(database_url)
		self.image_dir = image_dir

	def save(self, card):
		'''
		saves card using saver
		card: a solved card obj
		return: True if card was saved, False otherwise
		'''
		try:
			image_path = os.path.join(self.image_dir, card.creator, card.name + '.jpeg')
			card.save_image(image_path)
		except Exception as error:
			print(f'ERROR: {error}')
			print(f'card {repr(card)} image can\'t be saved to image directory, card not saved')
			return False
		
		try:
			metadata = get_metadata_from_card(card, image_path)
			self.driver.upsert(metadata)
		except Exception as error:
			print(f'ERROR: {error}')
			print(f'card {repr(card)} metadata can\'t be saved to database, card not saved')
			os.remove(image_path) #if card not saved we want his image to not be in image directory
			return False
		return True

	def get_key_values(self, key):
		'''
		returns all values off the fiels in the saver database
		'''
		if key not in METADATA_FIELDS: #prob unnecsery
			raise ValueError("key not in metadata keys")
			return
		return self.driver.key_values(key)

	def get_creators(self):
		return self.driver.creators()


	def find_many(self, filter):
		return self.driver.find_many(filter)


	def get_metadata(self, card_name, card_creator):
		return self.driver.get_card(name, creator)

	def get_image(self, card_name, card_creator): #not sure
		pass

	def get_card(self, card_name, card_creator):
		pass


#private
def get_driver(url): 
	url = furl(url)
	for scheme, clas in drivers.items():
		if url.scheme == scheme:
			return clas.create_from_url(url)
	raise ValueError(f'invalid url: {url}')

#private
def get_metadata_from_card(card, image_path):
	metadata = {
			"name" : card.name,
			"creator" : card.creator,
			"riddle" : card.riddle,
			"solution" : card.solution,
			"image_path" : image_path
		}
	return metadata



if __name__ == '__main__':
	card = Card.create_from_path('super_name', 'Avner', '2 + 3?', '5', '/home/user/Downloads/download.jpeg')
	url = furl()
	url.scheme = 'mongodb'
	url.host, url.port = "127.0.0.1", 27017
	saver = Saver(url)
	saver.save(card)