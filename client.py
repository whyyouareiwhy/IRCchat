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
        msg_input = f'{nickname}: {input("")}'
        message = msg_input[len(nickname)+2:]
        # User can display users in a chat room by typing '/users' and then
        # the name of the room.
        if message == "/users":
            room = input("Enter channel to display its users: ")
            client.send(room.encode('utf-8'))
        elif message == "/privatemsg":
            user = input("Enter user for private message: ")
            # print(f"user for priv msg <{user}>")
            client.send(message.encode('utf-8'))
            time.sleep(0.1)
            client.send(user.encode('utf-8'))
            time.sleep(0.1)
            msg = input("Enter message: ")
            nick_msg = nickname + ": " + msg
            # print(f"nick_msg <{nick_msg}>")
            client.send(nick_msg.encode('utf-8'))
        elif message == "/channelmsg":
            # Send a message to all users in specified channel
            room = input("Enter channel name to message: ")
            client.send(message.encode('utf-8'))
            time.sleep(0.1)
            msg = input("Enter message: ")
            client.send(room.encode('utf-8'))
            time.sleep(0.1)
            nick_msg = nickname + ": " + msg
            client.send(nick_msg.encode('utf-8'))
        elif message == "/channels":
            client.send(message.encode('utf-8'))
        elif message == "/add":
            client.send(message.encode('utf-8'))
            time.sleep(0.1)
            room_input = input("Enter new channel name: ")
            client.send(room_input.encode('utf-8'))
            time.sleep(0.1)
            print(f"Added {room_input}!")
            # time.sleep(0.1)
            client.send(nickname.encode('utf-8'))
            time.sleep(1)
        else:
            client.send(msg_input.encode('utf-8'))


# Start thread, get time, and update time when posting message
# def getTime():


receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()
