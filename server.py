'''
CS 494P Final Networking Project
IRC CHAT
Server Implementation
'''

import socket
import threading


HOST = '127.0.0.1'  # localhost
PORT = 60000
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen()

clients = []
nicknames = []

def broadcastMsg(msg):
    for client in clients:
        client.send(msg)


def handleClient(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcastMsg(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nick = nicknames[index]
            nicknames.remove(nick)
            broadcastMsg(f'{nick} has left!'.encode('ascii'))
            break


def runServer():
    while True:
        client, address = SERVER.accept()

        client.send('NICK'.encode('ascii'))
        nick = client.recv(1024).decode('ascii')
        nicknames.append(nick)
        clients.append(client)

        # Display in server
        print(f'User [{nick}] has connected with: {str(address)}.')

        # Display in chatroom
        broadcastMsg(f'{nick} has joined the channel.'.encode('ascii'))
        # client.send('Connected to server.'.encode('ascii'))

        # Handle multiple clients with threading
        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()

print('Server running...')
runServer()
