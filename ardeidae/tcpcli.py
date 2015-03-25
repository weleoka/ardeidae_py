import socket
import sys


# HOST, PORT = "sweet.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "seekers.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "192.168.1.36", 8120                           #connect to localhost, port
# HOST, PORT = "127.0.1.1", 8120
HOST, PORT = "localhost", 8120
# HOST, PORT = "bumblebea.st", 8120
# HOST, PORT = "ardeidae.computersforpeace.net", 8120


print (" ")
print ("Started ardeidae_py TCP client.")
print ("Trying to connect to TCP server: ", HOST, " on port: ", PORT, "...wait.")
# Create a socket (SOCK_STREAM means a TCP socket)


def startHere ():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        print ("...connected.")

        print ("(please input string to echo, or integer to request file of certain size)")
        message = input('PROMPT: ')
        # messageBytes = str.encode(message)
        if message:
            sock.sendall(message.encode('utf-8'))
            received = sock.recv(1024)
        else:
            print ("Nothing sent. Please input a string or integer to transmit.")
            received = "Nothing recieved because nothing sent."
            sock.close()

    finally:
        sock.close()

    if hasattr(received, 'decode'):
        print ("Sent: " + message )
        print ("Received: " + received.decode('utf-8'))
    print ("...disconnected from ", HOST)
    startHere()


startHere()