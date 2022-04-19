import socket
import sys
import config
from main import server_connection
import threading
import re

run_loop = True

def initialize_connection(host: str, port : str):
    
    for result in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        family, type, protocol, canonical, socket_address = result
        
        try:
            s = socket.socket(family, type, protocol)
        except OSError as msg:
            s = None
            continue

        if s is not None:
            try:
                s.connect(socket_address)
            except OSError as msg:
                s.close()
                s = None
                continue
        break
    return s

def receive_message(sock):
    global server_connection
    while run_loop and sock is not None:
        try:
            message = sock.recv(config.message_size)
        except None:
            break

        if message == b'':
            print("Connection closed by foreign host")
            server_connection = None
            # sys.exit(0)
        else:
            print(message.decode(), end="")
