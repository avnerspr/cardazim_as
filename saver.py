import os
from card import Card
import json
from pathlib import Path
from furl import furl
from file_system_driver import FileSystem_Driver
from mongodb_driver import MongoDB_Driver

DEFULT_IMAGE_DIR = r'cards_images/'

drivers = {
	'filesystem' : FileSystem_Driver,
	'mongodb' : MongoDB_Driver
	}

class Saver:

	def __init__(self, database_url, image_dir=DEFULT_IMAGE_DIR):
		self.driver = get_driver(database_url)
		self.image_dir = image_dir

	def save(self, card):
		image_path = os.path.join(self.image_dir, card.name)
		card.save_image(image_path)
		metadata = get_metadata(card, image_path)
		self.driver.upsert(metadata)


def get_driver(url): 
	url = furl(url)
	for scheme, clas in drivers.items():
		if url.scheme == scheme:
			return clas.create_from_url(url)
	raise ValueError(f'invalid url: {url}')

def get_metadata(card, image_path):
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