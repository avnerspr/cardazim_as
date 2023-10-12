import os, sys
from PIL import Image
import hashlib
from Crypto.Cipher import AES
import struct




class Crypt_Image:

	def __init__(self, image, key_hash):
		self.image = image
		self.key_hash = key_hash

	@classmethod
	def create_from_path(cls, path):
		return Crypt_Image(Image.open(path), None)


	def encrypt(self, key):
		bytes_key = bytes(key, 'utf-8')
		size, mode = self.image.size, self.image.mode
		self.key_hash = hash_sha256(bytes_key)

		encrypted_image_bytes = self.encrypt_image_info()
		self.key_hash = hash_sha256(self.key_hash)
		self.image = Image.frombytes(mode, size, encrypted_image_bytes)

	def decrypt(self, key):
		check_key_hash = hash_sha256(key) #maybe need to remove
		if hash_sha256(check_key_hash) != self.key_hash: #maybe need to hash key twice
			print('incorrect key')
			return False
		mode, size = self.image.mode, self.image.size
		decrypted_image_bytes = self.decrypt_image_info(check_key_hash)
		
		self.image = Image.frombytes(mode, size, decrypted_image_bytes)
		self.key_hash = None
		return True

	def encrypt_image_info(self):
		image_bytes = self.image.tobytes()
		return AES_encrypt(self.key_hash, image_bytes)

	def decrypt_image_info(self, key):
		encrypted_image_bytes = self.image.tobytes()
		return AES_decrypt(key, encrypted_image_bytes)

	def serialize(self):
		ans = struct.pack('II', self.image.size[0], self.image.size[1])
		ans += self.image.tobytes() + self.key_hash
		return ans

	@classmethod
	def deserialize(cls,  data): #maybe add exeptions
		size, image_data, key_hash, rest_data = sep_crypt_image_data(data)
		image = Image.frombytes('RGB', size, image_data)
		return Crypt_Image(image, key_hash), rest_data

	def save_image(self, path):
		image_file = path +'.jpeg'
		try:
			self.image.save(image_file)
		except OSError:
			print('error saving image to ' + path)

	def check_key(self, key):
		return hash_sha256(hash_sha256(key) ) == self.key_hash




def hash_sha256(bytes_arr):
	hash_obj = hashlib.sha256(bytes_arr)
	return hash_obj.digest()

def AES_encrypt(key, bytes_info, AES_nonce=b'arazim'):
	cipher = AES.new(key, AES.MODE_EAX, nonce=AES_nonce)
	return cipher.encrypt(bytes_info)

def AES_decrypt(key, encrypted_bytes_info, AES_nonce=b'arazim'):
	cipher = AES.new(key, AES.MODE_EAX, nonce=AES_nonce)
	return cipher.decrypt(encrypted_bytes_info)

def sep_crypt_image_data(data):
	size = struct.unpack('II', data[:8])
	image_bytes_num = 3 * size[0] * size[1]
	return size, data[8: image_bytes_num + 8], data[image_bytes_num + 8: image_bytes_num + 40], data[image_bytes_num + 40:]

if __name__ == '__main__':
	image_try = Crypt_Image.create_from_path('/home/user/Downloads/download.jpeg')
	image_try.encrypt(b'cakjd')
	print(len(image_try.key_hash))
	image_try.decrypt(b'cakjad')
	image_try.image.show()