import os
from socket import *
import threading 
import sys

port = int(sys.argv[1])
password = str(sys.argv[2])
name_list = []
client_list = []

def main():
    # create socket, bind & listen
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    connect_message = 'Server started on port ' + str(port) + '. Accepting connections...'
    print(connect_message)

    while True:
        # accept connection & create thread for client
        connectionSocket, addr = serverSocket.accept()
        client = threading.Thread(target=client_thread, args=(connectionSocket, ))
        client.start()

# thread that is created for every instance of connection
def client_thread(connection):

    # receiver client password & name from command line
    client_info = connection.recv(1024).decode().split()
    client_password = client_info[0]
    name = client_info[1]

    # conditions of correct password & not repetitive name
    if (client_password.strip() != password):
        connection.send('Incorrect password\n'.encode())
        connection.close()

    elif (name in name_list):
        connection.send('Name already in use\n'.encode())
        connection.shutdown(SHUT_RDWR)
        connection.close()
        # return

    else:
        # welcomes client & adds name & socket to list, broadcast client's connection
        connection.send('Welcome!\n'.encode())
        join_message = name + ' joined the chatroom\n'
        send_to_all(join_message)
        print(join_message.strip())
        name_list.append(name)
        client_list.append(connection)

        while True:
            # always listen for message from client
            try:
                message = connection.recv(1024).decode().strip()
            except:
                connection.close()
                exit(1)

            # if the message is to exit, will broadcast leaving & remove connection from lists & close
            if (message == ':Exit' or message == ''):
                connection.close()
                left_chat = name + ' left the chatroom\n'
                name_list.remove(name)
                client_list.remove(connection)
                send_to_all(left_chat)
                print(left_chat.strip())

            # extra credit: implement a dm functionality
            elif (':dm' in message):
                dm = message.rstrip().split(' ', 2)
                dm_receiver = dm[1]
                dm_message = dm[2]

                dm_message = name + ' -> ' + dm_receiver + ': ' + dm_message + '\n'
                dm_index = name_list.index(dm_receiver)
                connection.send(dm_message.encode())
                client_list[dm_index].send(dm_message.encode())
                print(dm_message.strip())

            # will format and send message to other clients in server
            else:
                format_message = name + ': ' + message + '\n'
                send_to_all(format_message)
                print(format_message.strip())

def send_to_all(message):
    for client in client_list:
        client.send(message.encode())

main()