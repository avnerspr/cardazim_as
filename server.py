import socket
import sys
import argparse
from _thread import *
import threading
import time
from connection import Connection
from listener import Listener


print_lock = threading.Lock()

def thread_print_msg(conn):	
	print(conn.receive_message())
	print_lock.release()
	

def run_server(ip, port):
	with Listener(ip, port) as listener:
		while True:	
			with listener.accept() as conn:
				print_lock.acquire()
				start_new_thread(thread_print_msg, (conn,))#remove socket
				print_lock.acquire()
				print_lock.release()

def get_args():
	'''
	Example: python server.py "127.0.0.1" 6600
	'''
	parser = argparse.ArgumentParser(description='Send data to server.')
	parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
	parser.add_argument('server_port', type=int,
                        help='the server\'s port')
	return parser.parse_args()


def main():
	'''
    Implementation of CLI and sending data to server.
	'''
	args = get_args()
	run_server(args.server_ip,args.server_port)

if __name__ == '__main__':
    sys.exit(main())

