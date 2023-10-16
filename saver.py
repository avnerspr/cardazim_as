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
		os.makedirs(self.image_dir, exist_ok=True)

	def save(self, card):
		'''
		saves card using saver
		card: a solved card obj
		return: True if card was saved, False otherwise
		'''
		try:
			creator_images_path = os.path.join(self.image_dir, card.creator)
			os.makedirs(creator_images_path, exist_ok=True)
			image_path = os.path.join(creator_images_path, card.name + '.jpeg')
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


	def find_cards(self, filter):
		cards = self.driver.find_many(filter)
		print(cards)
		return cards



	def get_metadata(self, card_name, card_creator):
		return self.driver.get_metadata(card_name, card_creator)

	def get_image(self, card_name, card_creator):
		image_card = self.get_card(card_name, card_creator)
		return card.image
		

	def get_card(self, card_name, card_creator):
		card_metadata = self.get_metadata(card_name, card_creator)
		return Card.create_from_path(
			name = metadata['name'],
			creator = metadata['creator'],
			riddle = metadata['riddle'],
			solution = metadata['solution'],
			path = metadata['image_path'])

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
	print(url)
	saver = Saver('filesystem:solved_cards')
	saver.save(card)
	print('goten_metadata:')
	print(saver.get_metadata(card.name, card.creator))
	card2 = Card.create_from_path('other_name', 'Avner', '2 + 4?', '6', '/home/user/Downloads/download.jpeg')
	card3 = Card.create_from_path('cardy_card', 'not_me', '2 + 7?', '9', '/home/user/Downloads/download.jpeg')
	saver.save(card2)
	saver.save(card3)
	saver.find_cards({'creator': 'Avner'})