
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

def openCon():
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
cache - prints cached log-ins
rmcache n - removes n-th element from cache
opcache n - opens n-th element from cache 
    """
    print(commands)

def quit(server_socket, server_thread):

    if server_socket is socket:
        server_socket.close()

    if server_thread is not None:
        connection.run_loop = False
        server_thread.join()
    
    sys.exit(0)

def show_cache():
    try:
        with open(config.cached_file) as cache:
             for i, k in enumerate(cache.readlines()):
                print(i, k, end="")
    except:
        print("There are no cached connections")

def op_cache(n):
    with open(config.cached_file, "r") as cache:
        try:
            host, port = cache.readlines()[n].split()
            return connection.initialize_connection(host, port)
        except IndexError:
            print("The entered number is too big, or negative")

def rm_cache(n):
    with open(config.cached_file, "r+") as cache:
        lines = cache.readlines()
    try:
        lines[n] = ""
    except IndexError:
        print("The entered number is too big, or negative")
    with open(config.cached_file, "w") as new_cache:
        new_cache.writelines(lines)