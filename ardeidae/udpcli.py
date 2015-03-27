from socket import *
import sys
import time

# HOST, PORT = "sweet.student.bth.se", 8121
# HOST, PORT = "seekers.student.bth.se", 8121
# HOST, PORT = "ardeidae.computersforpeace.net", 8121
HOST, PORT = "localhost", 8121



class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start



def printStartupMsg():
    print (" ")
    print ("Started ardeidae_py UDP client.")
    print ("The client will try to connect to UDP server: ", HOST, " on port: ", PORT, " if you send anything.")



def quitNow ():
    print ("Shutting down client...")
    sys.exit()



def outputFile(dataStr):
    print ("Length of recieved data is: ")
    print (len(dataStr))
    print ("Size is: ")
    print (str(sys.getsizeof(dataStr)))
    # print (dataStr.decode('utf-8'))



def recv_file_with_size(cnct, size):
    msg = b''
    while len(msg) < size:
        chunk, serverAddress = cnct.recvfrom(size-len(msg))
        if chunk == '':
            raise RuntimeError("Socket connection broken")
        msg = msg + chunk
    return msg



def startHere (theConnection):
    message = input('PROMPT: ')
    messageBytes = str.encode(message)

    typedInteger = False
    try:
        typedInteger = int(message)
    except:
        pass

    if len(message) > 0:
        if str(message) == 'quit':
            quitNow()
        else:
            # TIMETAKE
            with Timer() as t:
                theConnection.sendto(messageBytes, (HOST, PORT))
            print ('Sending took %.03f sec.' % t.interval)
    else:
        print ("Nothing sent. Please input a string or integer(10 million max) to transmit.")
        received = "Nothing recieved because nothing sent."

    if typedInteger:
        # TIMETAKE
        with Timer() as t:
            dataRecieved = recv_file_with_size (theConnection, typedInteger)
        print ('Recieving took %.03f sec.' % t.interval)

        outputFile(dataRecieved)
        quitNow()

    else:
        print ("Sent:     ", message)

        # TIMETAKE
        with Timer() as t:
            dataRecieved, serverAddress = theConnection.recvfrom(2048)
        print ('Recieving took %.03f sec.' % t.interval)

        print ("Received: ", dataRecieved)
        print ("Received {0} bytes of data recieved.".format(sys.getsizeof(dataRecieved)))

        quitNow()



    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto().
# SOCK_DGRAM is the socket type to use for UDP sockets
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket = socket(AF_INET, SOCK_DGRAM)
printStartupMsg()

startHere(clientSocket)









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