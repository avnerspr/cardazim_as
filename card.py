from crypt_image import Crypt_Image
import struct
import json


class Card:

	def __init__(self, name, creator, image, riddle, solution=None):
		self.name = name
		self.creator = creator
		self.image = image
		self.riddle = riddle
		self.solution = solution

	def __repr__(self):
		return f"<Card name={self.name}, creator={self.creator}>"

	def __str__(self):
		if self.solution == None:
			return f"Card {self.name} by {self.creator}\n\triddle: {self.riddle}\n\tsolution: unsolved"
		else:
			return f"Card {self.name} by {self.creator}\n\triddle: {self.riddle}\n\tsolution: {self.solution}"

	@classmethod
	def create_from_path(cls, name, creator, riddle, solution, path):
		image = Crypt_Image.create_from_path(path)
		return Card(name, creator, image, riddle, solution)
	
	def serialize(self):
		return b''.join([string_to_bytes(self.name), string_to_bytes(self.creator), self.image.serialize(), string_to_bytes(self.riddle)])

	@classmethod
	def deserialize(cls, data):
		name, data = str_deserialize(data)
		creator, data = str_deserialize(data)
		image, data = Crypt_Image.deserialize(data)
		riddle, data = str_deserialize(data)
		return Card(name, creator, image, riddle)

	def save_image(self, path):
		self.image.image.save(path)

	def solve(self, solution):
		if self.solution != None:
			print('card ' + repr(self) + ' was already solved')
			return self
		bytes_sol = bytes(solution, 'utf-8')
		is_true_sol = self.image.decrypt(bytes_sol)
		if not is_true_sol:
			print('wrong solution for ' + self.repr())
			return
		self.solution = solution



	def check_solution(self, solution):
		'''
		self: unsolved card
		returns True if soulution is correct. else returns False
		'''
		return self.image.check_key(bytes(solution, 'utf-8'))



def string_to_bytes(text):
	bytes_data = bytes(text, 'utf-8')
	return struct.pack('I',len(bytes_data)) + bytes_data

def str_deserialize(data): 
	size = struct.unpack('I', data[0:4])[0]
	return data[4:size + 4].decode(), data[size + 4:]


if __name__ == '__main__':
	card = Card.create_from_path('name', 'creator', 'riddle', 'solution', '/home/user/Downloads/download.jpeg')
	card.image.encrypt(card.solution)
	data = card.serialize()
	card2 = Card.deserialize(data)
	if card2.image.decrypt(b'solution'):
		card2.solution = card.solution
	assert(repr(card) == repr(card2))
	card2.image.image.show() # will show the same image as in path