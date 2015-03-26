import socket
import sys

# HOST, PORT = "sweet.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "seekers.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "192.168.1.36", 8120                           #connect to localhost, port
# HOST, PORT = "127.0.1.1", 8120
HOST, PORT = "localhost", 8120
# HOST, PORT = "bumblebea.st", 8120
# HOST, PORT = "ardeidae.computersforpeace.net", 8120



def printStartupMsg():
    print (" ")
    print ("Started ardeidae_py TCP client.")
    print ("Trying to connect to TCP server: ", HOST, " on port: ", PORT, "...wait.")



def startHere (theConnection):
    message = input('PROMPT: ')

    typedInteger = False
    try:
        typedInteger = int(message)
    except:
        pass

    if len(message) > 0:
        if str(message) == 'quit':
            quitNow(theConnection)
        else:
            theConnection.sendall(message.encode('utf-8'))
            received = theConnection.recv(1024)

    else:
        print ("Nothing sent. Please input a string or integer to transmit.")
        received = "Nothing recieved because nothing sent."

    if typedInteger:
        dataRecieved = recv_file_with_size (theConnection, typedInteger)
        outputFile(dataRecieved)
        quitNow(theConnection)

    elif hasattr(received, 'decode'):
        print ("\n-> Sent: " + message )
        print ("<- Received: " + received.decode('utf-8'))
        quitNow(theConnection)



def outputFile(dataStr):
    print("Length of recieved data is: ")
    print(len(dataStr))
    print (dataStr.decode('utf-8'))



def recv_file_with_size(cnct, size):
    print("Size:", size)
    msg = b''
    while len(msg) < size:
        print("msg length:", len(msg))
        chunk = cnct.recv(size-len(msg))
        if chunk == '':
            raise RuntimeError("Socket connection broken")
        msg = msg + chunk
    return msg



def quitNow (cnct):
    cnct.close()
    print ("...disconnected from ", HOST)
    print ("Shutting down client...")
    sys.exit()



# Create a socket (SOCK_STREAM means a TCP socket), connect to server.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
    print ("...connected.")
    print ("(please input string to echo, or integer to request file of certain number of rows)")
except:
    print ("Failed to connect to server.")
    sys.exit()

startHere(sock)