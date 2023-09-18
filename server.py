import socket
import sys
import argparse
from _thread import *
import threading
import time

print_lock = threading.Lock()

def thread_print_msg(conn):	
	data = conn.recv(1024).decode()
	print(str(data))
	print_lock.release()
	conn.close()

def run_server(ip, port):
	server_socket = socket.socket()
	server_socket.bind((ip, port))
	server_socket.listen(5)
	while True:	
		conn, address = server_socket.accept()
		print_lock.acquire()
		start_new_thread(thread_print_msg, (conn,))
	server_socket.close()

def get_args():
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

