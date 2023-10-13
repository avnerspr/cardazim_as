import pytest
import socket
import struct

NUM = 4

class MockSocket:
	sent_data = []
	addr = None
	
	def connect(self, addr):
		MockSocket.addr = addr

	def send(self, data):
		MockSocket.sent_data.append(data)

	def recv(self, num):
		return struct.pack('I', NUM)

	def close(self):
		pass

	def getsockname(self):
		

@pytest.fixture
def mock_socket(monkeypatch):
	monkeypatch.setattr(socket, 'socket', MockSocket)





#not sure if this class should be used
class MockConn:

	def __init__(self, mock_socket): #not implemented local_name, local_host, local_port attr
		self.socket = mock_socket
		self.peer_name = mock_socket.addr
		self.peer_host, self.peer_port = self.peer_name

	@classmethod
	def connect(cls, host, port):
		conn_socket = MockConn()
		conn_socket.connect((host, port))
		return Connection(conn_socket) #modify
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
