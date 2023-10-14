#!/usr/bin/env python

import socket
import sys
import os
import argparse
from _thread import *
import threading
import pathlib
from card import Card
import time
from connection import Connection
from listener import Listener


print_lock = threading.Lock()

def get_dir_filenum(dir_path):
	return len(os.listdir(dir_path))

def thread_print_msg(conn):	
	print(conn.receive_message())
	print_lock.release()
	
def thread_print_card_metadata(conn): #need to change from print
	card = recive_card(conn)
	print(f'Recived\n{str(card)}')
	print_lock.release()

def recive_card(conn):
	card_data = conn.receive_data()
	return Card.deserialize(card_data)

def thread_recv_and_save_card(listener, save_dir_path):
	with listener.accept() as conn:
		card_data = conn.receive_data()
		print('recived card data')
		save_path = os.path.join(save_dir_path, str(get_dir_filenum(save_dir_path)))
		with open(save_path, 'wb') as write_file:
			write_file.write(card_data)
		print_lock.release()

def run_server(ip, port, save_dir_path):
	with Listener(ip, port) as listener:
		while True:	
			print_lock.acquire()
			start_new_thread(thread_recv_and_save_card, (listener, save_dir_path))


def get_args():
	'''
	Example: python server.py "127.0.0.1" 6600 './unsolved_cards'
	'''
	parser = argparse.ArgumentParser(description='Send data to server.')
	parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
	parser.add_argument('server_port', type=int,
                        help='the server\'s port')
	parser.add_argument('unsolved_dir', type=pathlib.Path,
                        help='the path of the unsolved cards directory')
	return parser.parse_args()


def main():
	'''
    Implementation of CLI and sending data to server.
	'''
	args = get_args()
	if not os.path.exists(args.unsolved_dir):
		os.makedirs(args.unsolved_dir)
	run_server(args.server_ip,args.server_port, args.unsolved_dir)

if __name__ == '__main__':
    sys.exit(main())

