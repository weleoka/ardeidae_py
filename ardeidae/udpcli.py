import socket
import sys


# HOST, PORT = "sweet.student.bth.se", 8121
# HOST, PORT = "seekers.student.bth.se", 8121
# HOST, PORT = "ardeidae.computersforpeace.net", 8121
HOST, PORT = "localhost", 8121
data = " ".join(sys.argv[1:])
msg = data.strip()

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print (" ")
print ("Started ardeidae_py UDP client.")
# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().

sock.sendto(msg.encode('utf-8'), (HOST, PORT))
received = sock.recv(1024)

print ("Sent:     ", data)
print ("Received: ", received)