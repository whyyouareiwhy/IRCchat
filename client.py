'''
CS 494P Final Networking Project
IRC CHAT
Client Implementation
'''

import socket
import threading
import time

HEADER = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 6060))
nickname = input("Enter user name: ")
channels = ['#general']
curr_channel = "#general"  # default channel
# msgTime = datetime.datetime.now()  # Do in thread and within message()


# Receive commands and messages from server
def receive():
    while True:
        try:
            message = client.recv(HEADER).decode('utf-8')
            if 'NICK' == message:
                client.send(nickname.encode('utf-8'))
            else:
                print(f"~~ {message}")
        except:
            print("Error occurred.")
            client.close()
            break


def write():
    while True:
        try:
            msg_input = f'{nickname}: {input("")}'
            message = msg_input[len(nickname)+2:]
            if message == "/users":
                # Display all users in a room
                room = input("Enter channel: ")
                client.send(room.encode('utf-8'))
            elif message == "/privatemsg":
                # Send direct private message to user
                user = input("Enter user name: ")
                client.send(message.encode('utf-8'))
                time.sleep(0.1)
                client.send(user.encode('utf-8'))
                time.sleep(0.1)
                msg = input("Enter message: ")
                nick_msg = nickname + ": " + msg
                client.send(nick_msg.encode('utf-8'))
            elif message == "/channelmsg":
                # Send a message to all users in specified channel
                room = input("Enter channel name: ")
                client.send(message.encode('utf-8'))
                time.sleep(0.1)
                msg = input("Enter message: ")
                client.send(room.encode('utf-8'))
                time.sleep(0.1)
                nick_msg = nickname + ": " + msg
                client.send(nick_msg.encode('utf-8'))
            elif message == "/channels":
                # List all channels
                client.send(message.encode('utf-8'))
            elif message == "/add":
                # Add new room/channel and join automatically
                client.send(message.encode('utf-8'))
                time.sleep(0.1)
                room_input = input("Enter new channel name: ")
                client.send(room_input.encode('utf-8'))
                time.sleep(0.1)
                print(f"Added {room_input}!")
                client.send(nickname.encode('utf-8'))
            elif message == "/leave":
                room = input("Leave which channel: ")
                client.send(message.encode('utf-8'))
                time.sleep(0.1)
                client.send(room.encode('utf-8'))
                time.sleep(0.1)
                client.send(nickname.encode('utf-8'))
            else:
                client.send(msg_input.encode('utf-8'))
        except:
            print("exception occurred")
            client.close()


receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()
