from socket import *
import sys

# HOST, PORT = "sweet.student.bth.se", 8121
# HOST, PORT = "seekers.student.bth.se", 8121
# HOST, PORT = "ardeidae.computersforpeace.net", 8121
HOST, PORT = "localhost", 8121

# SOCK_DGRAM is the socket type to use for UDP sockets
clientSocket = socket(AF_INET, SOCK_DGRAM)

print (" ")
print ("Started ardeidae_py UDP client.")
message = input('PROMPT: ')
messageBytes = str.encode(message)


# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().

# TIMETAKE
clientSocket.sendto(messageBytes, (HOST, PORT))
# TIMETAKE

# TIMETAKE
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
# TIMETAKE

print ("Sent:     ", message)
print ("Received: ", modifiedMessage)
clientSocket.close()