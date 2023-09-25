import socket
import sys
import argparse
import pathlib
import struct
from connection import Connection
from card import Card


def card_from_args(args):
	return Card.create_from_path(args.name, args.creator, args.riddle, args.solution, args.image_path)

def encode_str(data):
	bytes_data = bytes(data, 'utf-8')
	return struct.pack('I',len(bytes_data)) + bytes_data

def send_data(server_ip, server_port, data):
	'''
    Send data to server in address (server_ip, server_port).
    '''
	with Connection.connect(server_ip, server_port) as conn:
		conn.send_data(data)

def card_to_data_for_send(card): #proboably later I would need to implement client card bank and encrypting a copy of the card
	card.image.encrypt(card.solution)
	return card.serialize()

def send_card(server_ip, server_port, card):
	print(f'sending Card \'{card.name}\' by {card.creator}')
	send_data(server_ip, server_port, card_to_data_for_send(card))


def get_args():
	parser = argparse.ArgumentParser(description='Send Cardazim Card to server.')
	parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
	parser.add_argument('server_port', type=int,
                        help='the server\'s port')
	parser.add_argument('name', type=str,
                        help='the Card name')
	parser.add_argument('creator', type=str,
                        help='the Card creator')
	parser.add_argument('riddle', type=str,
                        help='the riddle of the card')
	parser.add_argument('solution', type=str,
                        help='the solution of the card riddle')
	parser.add_argument('image_path', type=pathlib.Path,
                        help='the path of the card image')
	return parser.parse_args()


def main():
	'''
	Implementation of CLI and sending data to server.
	Example: python client.py "127.0.0.1" 6600 my_card Erez “whats the time?” “15:00” ~/cool_image.jpg
	'''
	args = get_args()
	
	try:
		send_card(args.server_ip, args.server_port, card_from_args(args))
		print('Done.')
	except Exception as error:
		print(f'ERROR: {error}')
		return 1

if __name__ == '__main__':
    sys.exit(main())

