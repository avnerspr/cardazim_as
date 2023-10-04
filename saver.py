import os
from card import Card
import json



class Saver:

	def save(self, card, dir_path='.'): #fix to check if card name already in dir
		if not os.path.exists(dir_path):
			os.mkdir(dir_path)
		card_path = os.path.join(dir_path, card.name)
		if os.path.exists(card_path):
			print('card with same name already exist')
			return False
		try: 
			os.mkdir(card_path) 
		except OSError as error: 
			print(error)
		image_path = os.path.join(card_path, r'image.jpg')
		card.save_image(image_path)
		json_path = os.path.join(card_path, r'metadata.json')
		self.card_to_json_file(json_path, card, image_path)



	def card_to_json_file(self, json_path, card, image_path):
		'''
		image_path : path to a place where the image is saved
		json_path : path to create json file in
		make a json describeing card in outfile
		'''
		card_dict = {
			"name" : card.name,
			"creator" : card.creator,
			"riddle" : card.riddle,
			"solution" : card.solution,
			"image_path" : image_path
		}
		with open(json_path, "w") as outfile:
			json.dump(card_dict, outfile)

if __name__ == '__main__':
	card = Card.create_from_path('name', 'creator', 'riddle', 'solution', '/home/user/Downloads/download.jpeg')
	saver = Saver()
	saver.save(card, 'check_saver')