from socket import *

serverName = 'localhost'
serverPort = 12001

"""
AF_INET= underlying network is using IPv4.
SOCK_DGRAM = UDP socket (rather than a TCP socket).
"""
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = raw_input('Input lowercase sentence:')

clientSocket.send(sentence)

modifiedSentence = clientSocket.recv(1024)

print 'From TCP Server:', modifiedSentence

clientSocket.close()
