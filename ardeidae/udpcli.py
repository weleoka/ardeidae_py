from socket import *
import sys
import time

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

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
with Timer() as t:
    clientSocket.sendto(messageBytes, (HOST, PORT))
print('Sending took %.03f sec.' % t.interval)

print ("Sent:     ", message)

# TIMETAKE
with Timer() as t:
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print('Recieving took %.03f sec.' % t.interval)

print ("Received: ", modifiedMessage)

clientSocket.close()


''' sending a file over udp.
buf = 1024
file = open (sys.argv[1], "rb")
data = file.read(buf)
while (data):
    if(clientSocket.sendto(data,addr)):
        print "sending ..."
        data = file.read(buf)
clientSocket.close()
file.close()
'''