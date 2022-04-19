import socket
import select
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("127.0.0.1", 20000))

s.listen(5)

print("waiting for accept")
a, b = s.accept()
print("accepted")

# a.setblocking(0)


while True:
    sleep(1)

    ready = select.select([a], [], [], 0)

    if ready[0]:
        a.send("Beep\n".encode())
        # print("Got message", ready[0])
    print("sending message")
    a.send("Boop\n".encode())


