#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_DGRAM
import sys
from ardei_utils import ardei_client_utils
Utils = ardei_client_utils


"""
This is a simple UDP client that takes arguments from a prompt.
Valid arguments are a string or an integer. The client sends this to an ardeidae_py UDP server,
the server will echo back a client string, or generate a file of certain size and transmit that to client
if the client enters a number.

The client can send a request for a paket stream by typing "stream" at prompt.
The server can send pakets at a set interval specified by client, in miliseconds.
The server has a paket limit in it's settings.

The client will wait for UDP packets to arrive until socket.settimeout() expires. Change this value by changing
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
    prompt = input('\nPROMPT: ')
    promtBytes = str.encode(prompt)
    # Set the socket timeout to default.
    theConnection.settimeout(RcvTimeOut_default)

    if len(prompt) > 0:
        try:
            typedInteger = int(prompt)
        except:
            typedInteger = False
            pass

        if str(prompt) == 'quit':
            quit_now()

        elif str(prompt) == 'stream':
            print("Switching server to stream mode")
            interval = input('\nPlease input the paket TX interval (miliseconds) required: ')
            pakets = input('\nPlease input the number of pakets required: ')

            streamRequest = str.encode('stream-' + str(interval) + '-' + str(pakets))
            theConnection.sendto(streamRequest, (HOST, PORT))

            streamData = Utils.recv_stream(theConnection)
            print("Recieved: " + str(len(streamData)/len(streamRequest)) + " pakets.")

        else:
            if typedInteger:
                # Set the timeout and send the command.
                theConnection.settimeout(RcvTimeOut)
                theConnection.sendto(promtBytes, (HOST, PORT))
                print ("Please wait for " + str(RcvTimeOut) + " seconds for the server to prepare your file.\n..........")

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

            else:
                # Set the timeout and send the command.
                theConnection.settimeout(RcvTimeOut_default)
                theConnection.sendto(promtBytes, (HOST, PORT))

                dataRecieved = theConnection.recv(1024)
                Utils.print_data_stats(dataRecieved)
                Utils.print_data_contents(dataRecieved)

                quit_now ()

    else:
        print ("Nothing sent. Please input a string or integer to transmit.")
        received = "Nothing recieved because nothing sent."


# Create a socket (SOCK_DGRAM means a UDP socket).
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
print_startup_msg()

start_here(clientSocket)