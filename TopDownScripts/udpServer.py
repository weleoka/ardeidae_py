from socket import *

serverPort = 12000

"""
AF_INET= underlying network is using IPv4.
SOCK_DGRAM = UDP socket (rather than a TCP socket).
"""
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', serverPort))

print ("The UDP server is ready to receive")

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.upper() + '-YAAAAAA!!'
    serverSocket.sendto(modifiedMessage, clientAddress)
