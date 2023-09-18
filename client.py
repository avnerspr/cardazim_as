import socket
import sys
import argparse
import struct

def encode_str(data):
	bytes_data = bytes(data, 'utf-8')
	print(bytes_data)
	return struct.pack('I',len(bytes_data)) + bytes_data

def send_data(server_ip, server_port, data):
	'''
    Send data to server in address (server_ip, server_port).
    '''
	encoded_data = encode_str(data)
	client_socket = socket.socket()
	client_socket.connect((server_ip, server_port))
	client_socket.send(encoded_data)
	client_socket.close()

def get_args():
	parser = argparse.ArgumentParser(description='Send data to server.')
	parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
	parser.add_argument('server_port', type=int,
                        help='the server\'s port')
	parser.add_argument('data', type=str,
                        help='the data')
	return parser.parse_args()


def main():
	'''
	Implementation of CLI and sending data to server.
	'''
	args = get_args()

	try:
		send_data(args.server_ip, args.server_port, args.data)
		print('Done.')
	except Exception as error:
		print(f'ERROR: {error}')
		return 1

if __name__ == '__main__':
    sys.exit(main())

