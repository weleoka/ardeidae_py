from socket import *

serverName = 'localhost'
serverPort = 12000

"""
AF_INET= underlying network is using IPv4.
SOCK_DGRAM = UDP socket (rather than a TCP socket).
"""
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = raw_input('Input lowercase sentence:')

clientSocket.sendto(message,(serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print (modifiedMessage)

clientSocket.close()

