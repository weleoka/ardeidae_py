import socket
import sys


# HOST, PORT = "sweet.student.bth.se", 8120
# HOST, PORT = "seekers.student.bth.se", 8120
HOST, PORT = "localhost", 8121
data = " ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
msg = data + "\n"
sock.sendto(msg.encode('utf-8'), (HOST, PORT))
received = sock.recv(1024)

print ("Sent:     {}".format(data))
print ("Received: {}".format(received))