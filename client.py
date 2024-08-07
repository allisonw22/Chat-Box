from datetime import datetime
import os
from socket import *
import threading
import time
import sys

def main():
    host = str(sys.argv[1])
    port = int(sys.argv[2])

    # client opens a TCP connection with the server
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))
    print('Connecting to ' + host + ' on port ' + str(port) + '...')

    # Next, it will send the password and its name to the server, each followed by a newline
    password = str(sys.argv[3]) + '\n'
    name = str(sys.argv[4]) + '\n'
    clientSocket.send(password.encode())
    clientSocket.send(name.encode())

    # and wait to receive the Welcome! message from the server.
    welcome = clientSocket.recv(1024)
    print(welcome.decode().strip())

    # starts/creates thread to monitor keyboard input
    x = threading.Thread(target=key_input_thread, args=(clientSocket,))
    x.start()

    # main thread that monitors responses from everyone on server
    while True:
        try:
            message = clientSocket.recv(1024)
            if not message:
                os._exit(1)
            print(message.decode().strip())
        except:
            clientSocket.close()
            exit(0)

def key_input_thread(socket):

    for line in sys.stdin:
        if line.rstrip() == ':Exit':
            socket.send(':Exit\n'.encode())
            socket.close()
            exit(0)
            # return
        elif line.rstrip() == ':)':
            socket.send('[feeling happy]\n'.encode())
        elif line.rstrip() == ':(':
            socket.send('[feeling sad]\n'.encode())
        elif line.rstrip() == ':mytime':
            now = datetime.now()
            hour = now.strftime("%H:%M")
            date = now.strftime("%a, %d %b, %Y.")
            message = "It's " + hour + " on " + date + '\n'
            socket.send(str(message).encode())
        else:
            socket.send(line.encode())
        time.sleep(1)

    socket.close()

main()
