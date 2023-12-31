import socket
import struct
import sys



class Connection:

	def __init__(self,conn_socket):
		self.socket = conn_socket
		self.local_name = conn_socket.getsockname()
		self.local_ip, self.local_port = self.local_name
		self.peer_name = conn_socket.getpeername()
		self.peer_ip, self.peer_port = self.peer_name

	def __repr__(self):
		return f'<Connection from {self.local_ip}:{self.local_port} to {self.peer_ip}:{self.peer_port}>'

	@classmethod
	def connect(cls, host, port):
		conn_socket = socket.socket()
		conn_socket.connect((host, port))
		return Connection(conn_socket) 

	
	@staticmethod
	def encode_str(data):
		bytes_data = bytes(data, 'utf-8')
		return struct.pack('I',len(bytes_data)) + bytes_data


	def send_message(self, message):
		self.socket.send(Connection.encode_str(message))

	def send_data(self, data):
		self.socket.send(data)

	def receive_str_message(self):
		return receive_data().decode()

	def receive_data(self):
		data = b'' #maybe replace by None
		while True:
			try:
				part_dat = self.socket.recv(1024)
				data += part_dat
			except socket.error as e:
				print (f"Error receiving data: {e}")
				sys.exit(1)
			if len(part_dat) == 0:
				break
		return data

	def close(self):
		self.socket.close()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		if exc_type != None:
			print("\nExecution type:", exc_type)
			print("\nExecution value:", exc_value)
			print("\nTraceback:", exc_traceback)
		self.close()

if __name__ == '__main__':
	with Connection.connect('127.0.0.1', 6600) as connection:
		connection.send_message('hello')
		data = connection.receive_message()