import sys
import config
import commands
import connection
import threading


print_mode = False
server_connection = None
server_thread = None

def command_mode():
    global server_connection
    global server_thread
    print(config.prompt_name, end="")
    command = input()

    if command == "quit":
        commands.quit(server_connection, server_thread)
    elif command == "close":
        commands.close(server_connection)
        server_connection = None
        server_thread = None
    elif command == "logout":
        commands.logout(server_connection)
        server_connection = None
        server_thread = None
        sys.exit(0)
    elif command == "open":
        connection.run_loop = True
        server_connection = commands.open()
        server_thread = threading.Thread(target=connection.receive_message, args=([server_connection]))
        server_thread.start()

    elif command == "send":
        commands.send()
    elif command == "status":
        commands.status(server_connection)
    elif command == "help":
        commands.help()
    else:
        pass
    
    if server_connection is None:
        command_mode()      
    else:
        send_mode()


# Start a new thread for server communication and user input 
def send_mode():
    global server_connection
    global server_thread
    
    if server_connection is None:
        command_mode()

    message = input()

    if message == "\x1d":
        command_mode()
    else:
        # send message to server
        message += config.message_end
        try:
            server_connection.send(message.encode())
        except:
            # Server closed
            server_connection = None
            server_thread = None
            command_mode()
        else:
            send_mode()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        server_connection = connection.initialize_connection(sys.argv[1], sys.argv[2])
        if server_connection is None:
            print("Connection failed")
            command_mode()
        else:
            connection.run_loop = True
            server_thread = threading.Thread(target=connection.receive_message, args=([server_connection]))
            server_thread.start()
            send_mode()
    elif len(sys.argv) == 1:
        command_mode()
    else:
        print("invalid amount of arguments")

    