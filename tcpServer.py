from socket import *

serverPort = 12001

"""
AF_INET= underlying network is using IPv4.
SOCK_DGRAM = UDP socket (rather than a TCP socket).
"""
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))

serverSocket.listen(1)

print 'The TCP server is ready to receive'

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = sentence.upper()

    connectionSocket.send(capitalizedSentence)

    connectionSocket.close()
