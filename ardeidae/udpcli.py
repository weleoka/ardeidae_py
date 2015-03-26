import socket
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



def quitNow (cnct):
    cnct.close()
    print ("Shutting down client...")
    sys.exit()



def startHere (theConnection):
    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto().
    message = input('PROMPT: ')
    messageBytes = str.encode(message)

    # TIMETAKE
    with Timer() as t:
        theConnection.sendto(messageBytes, (HOST, PORT))
    print('Sending took %.03f sec.' % t.interval)

    print ("Sent:     ", message)

    # TIMETAKE
    with Timer() as t:
        dataRecieved, serverAddress = theConnection.recvfrom(2048)

    print('Recieving took %.03f sec.' % t.interval)

    print ("Received: ", dataRecieved)
    print("Received {0} bytes of data recieved.".format(sys.getsizeof(dataRecieved)))

    quitNow(theConnection)



# SOCK_DGRAM is the socket type to use for UDP sockets
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# clientSocket = socket(AF_INET, SOCK_DGRAM)
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