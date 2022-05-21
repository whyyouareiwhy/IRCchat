'''
CS 494P Final Networking Project
IRC CHAT
Client Implementation
'''

import socket
import threading
import datetime

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(('127.0.0.1', 60000))

nickname = input("Select nickname: ")
msgTime = datetime.datetime.now()  # Do in thread and within message()

def receive():
    while True:
        try:
            message = CLIENT.recv(1024).decode('ascii')
            if 'NICK' == message:
                CLIENT.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("Error occurred.")
            CLIENT.close()
            break


def write():
    while True:
        message = f'{nickname} [{msgTime.hour}:{msgTime.minute}:{msgTime.second}]: {input("")}'
        CLIENT.send(message.encode('ascii'))


# Start thread, get time, and update time when posting message
# def getTime():


receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()
