#!/usr/bin/env python3
import socket
import sys
import time

# HOST, PORT = "sweet.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "seekers.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "192.168.1.36", 8120                           #connect to localhost, port
# HOST, PORT = "127.0.1.1", 8120
HOST, PORT = "localhost", 8120
# HOST, PORT = "bumblebea.st", 8120
# HOST, PORT = "ardeidae.computersforpeace.net", 8120



class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start



def printStartupMsg():
    print (" ")
    print ("Started ardeidae_py TCP client.")
    print ("Trying to connect to TCP server: ", HOST, " on port: ", PORT, "...wait.")



def outputFile(dataStr):
    print("Length of recieved data is: ")
    print(len(dataStr))
    # print (dataStr.decode('utf-8'))



def recv_file_with_size(cnct, size):
    msg = b''
    while len(msg) < size:
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



def startHere (theConnection):
    typedInteger = False

    message = input('PROMPT: ')
    messageBytes = str.encode(message)

    try:
        typedInteger = int(message)
    except:
        pass

    if len(message) > 0:
        if str(message) == 'quit':
            quitNow(theConnection)

        else:
            # TIMETAKE
            with Timer() as t:
                theConnection.sendall(messageBytes)
            print ('Sending took %.03f sec.' % t.interval)

            if typedInteger:
                # TIMETAKE
                with Timer() as t:
                    dataRecieved = recv_file_with_size (theConnection, typedInteger)
                print ('Recieving took %.03f sec.' % t.interval)

                outputFile(dataRecieved)
                quitNow(theConnection)

            else:
                # TIMETAKE
                with Timer() as t:
                    received = theConnection.recv(1024)
                print ('Recieving took %.03f sec.' % t.interval)

                print ("\n-> Sent: " + message )
                if hasattr(received, 'decode'):
                    print ("<- Received: " + received.decode('utf-8'))
                quitNow(theConnection)

    else:
        print ("Nothing sent. Please input a string or integer(10 million max) to transmit.")
        received = "Nothing recieved because nothing sent."



# Create a socket (SOCK_STREAM means a TCP socket), connect to server.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
printStartupMsg()
try:
    sock.connect((HOST, PORT))
    print ("...connected.")
    print ("(please input string to echo, or integer to request file of certain number Bytes).")
except:
    print ("Failed to connect to server.")
    sys.exit()

startHere(sock)