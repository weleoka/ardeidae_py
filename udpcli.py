#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_DGRAM
import sys
import time
import tempfile
import os
import re
from ardei_utils import ardei_client_utils
Utils = ardei_client_utils


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
# How long to wait for the server to generate a file.
RcvTimeOut = 10
# Default timeout for client if nothing recieved.
RcvTimeOut_default = 2
#Default mode is off. change to 1 to Rcv stream.
RcvStream = False


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
Main function
"""
def start_here (theConnection):
    typedInteger = False

    message = input('\nPROMPT: ')
    messageBytes = str.encode(message)

    if len(message) > 0:
        if str(message) == 'quit':
            quit_now()
        elif str(message) == 'stream':
            print("Switching server to stream mode")
            print("Please input the paket time interval required at prompt.")
            theConnection.sendto(messageBytes, (HOST, PORT))
            RcvStream = True
            start_here(theConnection)

        else:
            try:
                typedInteger = int(message)
            except:
                pass

            if typedInteger and RcvStream = False:
                print ("Please wait for " + str(RcvTimeOut) + " seconds for the server to prepare your file.\n..........")
                # Set the timeout.
                theConnection.settimeout(RcvTimeOut)

                # Wait for server to generate confirmation message
                if Utils.monitor_server_response(theConnection):
                    # Set the timeout to default.
                    theConnection.settimeout(RcvTimeOut_default)

                    # TIMETAKE
                    with Utils.Timer() as t:
                        dataRecieved = Utils.recv_file_with_size_UDP(theConnection)
                    print ('Recieving took %.03f sec.' % t.interval)

                    Utils.print_file_stats(dataRecieved)
                    Utils.print_file_contents(dataRecieved, PrintFile)

                else:
                    quit_now()

            elif typedInteger and RcvStream = True:
                theConnection.sendto(messageBytes, (HOST, PORT))
                while True:
                    streamData = cnct.recv(1024)

            else:
                theConnection.sendto(messageBytes, (HOST, PORT))
                # Set the timeout default.
                theConnection.settimeout(RcvTimeOut_default)

                dataRecieved, serverAddress = theConnection.recvfrom(1024)

                Utils.print_data_stats(dataRecieved)
                Utils.print_data_contents(dataRecieved)
                quit_now ()

    else:
        print ("Nothing sent. Please input a string or integer(100 million max) to transmit.")
        received = "Nothing recieved because nothing sent."


# Create a socket (SOCK_DGRAM means a UDP socket).
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
print_startup_msg()

start_here(clientSocket)