'''
CS 494P Final Networking Project
IRC CHAT
Server Implementation
'''

import socket
import threading
import time

# HOST = socket.gethostbyname(socket.gethostname())
HOST = '127.0.0.1'  # local host
PORT = 6060
HEADER = 1024

# Only one server required, it will listen for 1 or more clients
# and broadcast the messages to everyone
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
default_channel = "#general"
channels = {}  # dictionary of channel -> nickname
users = []  # store tuples of (nickname, client)
# List of clients in the '#general' channel created by default
channels[default_channel] = []


def broadcastMsg(msg):
    for client in clients:
        client.send(msg)


def channelMsg(channel, msg):
    for i in range(len(channels[channel])):
        receiver = channels[channel][i]
        for j in range(len(users)):
            if users[j][0] == receiver:
                users[j][1].send(msg.encode('utf-8'))


# Send direct private msg to a user
def directlMsg(user, msg):
    for i in range(len(users)):
        if users[i][0] == user:
            users[i][1].send(msg.encode('utf-8'))


def chanExists(chan):
    for i in channels:
        if i == chan:
            return True
    return False


def clientsInChannel(client, channel):
    client.send(f"\tUsers in channel {channel}:".encode('utf-8'))
    for i in range(len(channels[channel])):
        user = channels[channel][i]
        user = "\t\t" + user
        client.send(user.encode('utf-8'))
        time.sleep(0.01)


def dispChannels(client):
    client.send("Active channels:\n".encode('utf-8'))
    for i in channels:
        i = "\t" + i
        client.send(i.encode('utf-8'))
        time.sleep(0.01)


# Called continuously in thread after server-client connection established
# for each individual client. Handles all client tasks.
def handleClient(client):
    connected = True  # *******Use later for quit command
    while connected:
        try:
            message = client.recv(HEADER).decode('utf-8')
            if chanExists(message):
                # Display all users in provided channel
                clientsInChannel(client, message)
            elif message == "/privatemsg":
                receiver = client.recv(HEADER).decode('utf-8')
                msg = client.recv(HEADER).decode('utf-8')
                directlMsg(receiver, msg)
            elif message == "/channelmsg":
                # Send private message to channel
                room = client.recv(HEADER).decode('utf-8')
                msg = client.recv(HEADER).decode('utf-8')
                if chanExists(room):
                    channelMsg(room, msg)
            elif message == "/channels":
                # Display all active channels
                dispChannels(client)
            elif message == "/add":
                # Add new room to channels
                room = client.recv(HEADER).decode('utf-8')
                if not chanExists(room):
                    channels[room] = []
                user = client.recv(HEADER).decode('utf-8')
                channels[room].append(user)
            elif message == "/leave":
                # Leave specified channel
                room = client.recv(HEADER).decode('utf-8')
                user = client.recv(HEADER).decode('utf-8')
                if chanExists(room):
                    channels[room].remove(user)
            else:
                broadcastMsg(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nick = nicknames[index]
            nicknames.remove(nick)
            broadcastMsg(f'{nick} has left!'.encode('utf-8'))
            break


# Listen for new clients joining server, track nickname and add user
# to #general channel
def runServer():
    print('Server running...')
    while True:
        client, address = server.accept()

        client.send('NICK'.encode('utf-8'))
        nick = client.recv(HEADER).decode('utf-8')
        nicknames.append(nick)
        clients.append(client)
        # Every new user gets added to #general channel
        channels[default_channel].append(nick)
        # Add a tuple of nickname and client to users for direct lookup
        users.append((nick, client))

        # Display in server
        print(f'User [{nick}] has connected with: {str(address)}.')

        # Display in chatroom
        broadcastMsg(f'{nick} has joined the channel.'.encode('utf-8'))
        client.send('Connected to #general.'.encode('utf-8'))

        # Handle multiple clients with threading
        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()


# Run server until stopped with ctr-c by user
runServer()
