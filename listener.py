import socket
import sys
from _thread import *
import threading


class Listener:

	def __init__(self, host, port, backlog = 1000):
		self.host = host
		self.port = port
		self.backlog = backlog
		self.socket = socket.socket()

	def __repr__(self):
		return f"Listener(port={self.port}, host={self.host}, backlog={self.backlog})"

	def start(self):
		self.socket.bind((self.host, self.port))
		self.socket.listen(2) # necsery?

	def stop(self):
		self.socket.close()

	def accept(self):
		self.socket.accept()
		return Connection(self.socket)

	def __enter__(self):
		self.start()

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.stop()

if __name__ == '__main__':
	with Listener('127.0.0.1', 6600) as listener:
		with listener.accept() as connection:
			print(connection.receive_message())
