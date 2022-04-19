
from socket import socket
import threading
import sys
import connection
import config

def close(server_connection):
    if server_connection is not None:
        connection.run_loop = False
        server_connection.close()    

def logout(server_connection):
    if server_connection is not None:
        connection.run_loop = False
        server_connection.close()    

def open():
    print("Enter host name and port number")
    data_field = input()
    try:
        host, port = data_field.split(' ')
    except:
        print("Cannot understand the input")
        return None
    
    s = connection.initialize_connection(host, port)
    return s


def send():
    pass

def status(server_connection):
    if server_connection is None:
        print(config.program_name, " is not connected to a remote host")
    else:
        ip, port = server_connection.getsockname()
        print(config.program_name, " is connected to ", ip, port)

def help():
    commands = """
close - close current connection
logout - forcibly logout remote user and close the connection
open - connect to a site
quit - exit telnet
status - prints current status
    """
    print(commands)

def quit(server_socket, server_thread):

    if server_socket is socket:
        server_socket.close()

    if server_thread is not None:
        connection.run_loop = False
        server_thread.join()
    
    sys.exit(0)
