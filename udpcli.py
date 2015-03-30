#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_DGRAM
import sys
import time
import tempfile
import os
import re


"""
This is a simple UDP client that takes arguments from a prompt.
Valid arguments are a string or an integer. The client sends this to an ardeidae_py UDP server,
the server will echo back a client string, or generate a file of certain size and transmit that to client
if the client enters a number.

The server will wait for UDP packets to arrive until socket.settimeout() expires. Change this value by changing
RcvTimeOut variable.

Be aware of the config variables PrintFile and RcvTimeOut.

PrintFile: if true will attempt to output the whole file. That is a bad idea for big files.

RcvTimeOut: (seconds) If requesting a large file from server it will take a while for the server to generate that file,
if the client times out before the file begins to be sent by the server then try increasing this value.

"""


# HOST, PORT = "sweet.student.bth.se", 8121
# HOST, PORT = "seekers.student.bth.se", 8121
# HOST, PORT = "ardeidae.computersforpeace.net", 8121
HOST, PORT = "localhost", 8121

# Specify if recieved files are to be output to terminal or not.
PrintFile = False
# How long to wait before quitting the recieve state.
RcvTimeOut = 5



"""
Time object.
"""
class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start



"""
Startup and quit functions.
"""
def print_startup_msg():
    print (" ")
    print ("Started ardeidae_py UDP client.")
    print ("The client will try to connect to UDP server: ", HOST, " on port: ", PORT, " if you send anything.")

def quit_now ():
    print ("Shutting down client...")
    sys.exit()



"""
File data recieved functions.
"""
def recv_file_with_size(cnct):
    tf = tempfile.NamedTemporaryFile()
    msg = b''

    while True:
        try:
            chunkStr, serverAddress = cnct.recvfrom(1024)
            tf.write(chunkStr)
        except socket.timeout:
            return tf

    tf.flush() # Flush the write buffer to file.
    return tf

def print_file_stats (rf):
    metadata = os.stat(rf.name)
    print ("Recieved file \n (", rf.name, ")") # \n size: " + str(metadata.st_size) + " bytes.")

def print_file_contents (rf):
    buf = 10
    i = 0
    rf.seek(0)

    data = rf.read(buf)

    while (data):
        tmpstr = data.decode('utf-8')
        if PrintFile:
            print (tmpstr)
        i += len(tmpstr)
        data = rf.read(buf)

    print ("Total recieved: " +str(i) + " chars.")
    rf.close()



"""
String data recieved functions.
"""
def print_data_stats(rd):
    print ("Received {0} bytes of data.".format(sys.getsizeof(rd)))

def print_data_contents(rd):
    print (rd)



"""
Monitor the response from server for confirmation message.
"""
def monitor_server_response (cnct):
    while True:
        try:
            chunkStr, serverAddress = cnct.recvfrom(1024)
            response = chunkStr.decode('utf-8')
            if re.search('file_prepared', response):
                return True
            else:
                print ("No valid response recieved from server")
                return False
        except socket.timeout:
            return False



"""
Main function
"""
def start_here (theConnection):
    typedInteger = False

    message = input('\nPROMPT: ')
    messageBytes = str.encode(message)

    try:
        typedInteger = int(message)
    except:
        pass

    if len(message) > 0:
        if str(message) == 'quit':
            quit_now()

        else:
            # TIMETAKE
            with Timer() as t:
                theConnection.sendto(messageBytes, (HOST, PORT))
            print ('Sending took %.03f sec.' % t.interval)

            print ("Please wait for " + str(RcvTimeOut) + " seconds for the server response.\n..........")

            if typedInteger:
                # Set the timeout.
                theConnection.settimeout(RcvTimeOut)

                # Wait for server to generate confirmation message
                if monitor_server_response(theConnection):
                    # TIMETAKE
                    with Timer() as t:
                        dataRecieved = recv_file_with_size (theConnection, typedInteger)
                    print ('Recieving took %.03f sec.' % t.interval)

                    print_file_stats(dataRecieved)
                    print_file_contents(dataRecieved)

                else:
                    print ("Server response delayed or missing.")
                    quit_now()

            else:
                # Set the timeout to 5 seconds.
                theConnection.settimeout(RcvTimeOut)

                # TIMETAKE
                with Timer() as t:
                    dataRecieved, serverAddress = theConnection.recvfrom(1024)
                print ('Recieving took %.03f sec.' % t.interval)

                print_data_stats(dataRecieved)
                print_data_contents(dataRecieved)
                quit_now ()

    else:
        print ("Nothing sent. Please input a string or integer(100 million max) to transmit.")
        received = "Nothing recieved because nothing sent."



# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
# SOCK_DGRAM is the socket type to use for UDP sockets
# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)

print_startup_msg()

start_here(clientSocket)