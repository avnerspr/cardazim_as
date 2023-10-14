import socket
import sys
from _thread import *
import threading
from connection import Connection


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
		conn, addr = self.socket.accept()
		return Connection(conn)

	def __enter__(self):
		self.start()
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		if exc_type != None:
			print("\nExecution type:", exc_type)
			print("\nExecution value:", exc_value)
			print("\nTraceback:", exc_traceback)
		self.stop()

if __name__ == '__main__':
	with Listener('127.0.0.1', 6600) as listener:
		with listener.accept() as connection:
			print(connection.receive_message())
