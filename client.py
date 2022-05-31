'''
CS 494P Final Networking Project
IRC CHAT
Client Implementation
'''

import socket
import threading
import datetime

HEADER = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 6060))
nickname = input("Enter user name: ")
channels = ['#general']
# msgTime = datetime.datetime.now()  # Do in thread and within message()


def receive():
    while True:
        try:
            message = client.recv(HEADER).decode('utf-8')
            if 'NICK' == message:
                client.send(nickname.encode('utf-8'))
            # elif 'QUIT' == message:
            #     exit(1)
            else:
                print(f"{message}")
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
            room = input("Enter channel name: ")
            print(f"client room <{room}>")
            client.send(room.encode('utf-8'))
        else:
            client.send(msg_input.encode('utf-8'))


# Start thread, get time, and update time when posting message
# def getTime():


receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()
