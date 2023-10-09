import os
from card import Card
import json
import furl


class Saver:

	def __init__(self, database_url, image_dir):
		self.driver = get_driver(database_url)
		self.image_dir = image_dir

	def save(self, card):
		image_path = os.path.join(self.image_dir, card.name)
		card.save_image(image_path)
		metadata = get_metadata(card, image_path)
		self.driver.upsert(metadata)


def get_driver(url):
	for scheme, clas in drivers.items():
		if url.startswith(scheme):
			return clas(url)
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

drivers = {}

if __name__ == '__main__':
	card = Card.create_from_path('name', 'creator', 'riddle', 'solution', '/home/user/Downloads/download.jpeg')
	saver = Saver()
	saver.save(card, 'check_saver')