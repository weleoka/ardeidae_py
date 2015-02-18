import socket
import sys


# HOST, PORT = "sweet.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "seekers.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "192.168.1.36", 8120                           #connect to localhost, port
# HOST, PORT = "127.0.1.1", 8120
HOST, PORT = "localhost", 8120
# HOST, PORT = "bumblebea.st", 8120
# HOST, PORT = "ardeidae.computersforpeace.net", 8120

data = " ".join(sys.argv[1:])

print (" ")
print ("Started ardeidae_py TCP client.")
print ("Trying to connect to TCP server: ", HOST, " on port: ", PORT, "...wait.")
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    print ("...connected.")
    if len(sys.argv) >= abs(2):
        sock.sendall(data.encode('utf-8'))
        received = sock.recv(1024)
    else:
        print ("Nothing sent. Please execute with a string to transmit.")
        received = "Nothing sent, so nothing recieved."
        sock.close()
    # Receive data from the server and shut down
finally:
    sock.close()

print ("Sent:     {}".format(data))
print ("Received: {}".format(received))
print ("...disconnected from ", HOST)