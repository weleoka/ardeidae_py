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
RcvTimeOut_file variable.

Be aware of the config variables PrintFile and RcvTimeOut_file.

PrintFile: if true will attempt to output the whole file. That is a bad idea for big files.

RcvTimeOut_file: (seconds) If requesting a large file from server it will take a while for the server to generate that file,
if the client times out before the file begins to be sent by the server then try increasing this value.

"""


# HOST, PORT = "sweet.student.bth.se", 8121
# HOST, PORT = "seekers.student.bth.se", 8121
# HOST, PORT = "ardeidae.computersforpeace.net", 8121
HOST, PORT = "localhost", 8121

# Specify if recieved files are to be output to terminal or not.
PrintFile = False
# How long to wait for the server to generate a file.
RcvTimeOut_file = 10
# Default timeout for client if nothing recieved.
RcvTimeOut_default = 2



"""
Startup function.
"""
def print_startup_msg():
    print (" ")
    print ("Started ardeidae_py UDP client.")
    print ("The client will try to connect to UDP server: ", HOST, " on port: ", PORT, " if you send anything.")



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



    ### QUIT Request
        if str(prompt) == 'quit':
            Utils.quit_now_UDP()



    ### STREAM Request
        elif str(prompt) == 'stream':
            print("Switching server to stream mode")
            interval = input('\nPlease input the paket TX interval (miliseconds) required: ')
            pakets = input('\nPlease input the number of pakets required: ')

            streamRequest = str.encode('stream-' + str(interval) + '-' + str(pakets))
            theConnection.sendto(streamRequest, (HOST, PORT))

            streamData = Utils.recv_stream_UDP(theConnection)
            print("Recieved: " + str(len(streamData)/len(streamRequest)) + " pakets.")



    ### FILE Request
        else:
            if typedInteger:
                # Set the timeout and send the command.
                theConnection.settimeout(RcvTimeOut_file)
                theConnection.sendto(promtBytes, (HOST, PORT))

                # Wait for server to generate confirmation message
                print ("Please wait for " + str(RcvTimeOut_file) + " seconds for the server to prepare your file.\n..........")
                if Utils.monitor_server_response(theConnection):
                    # Set the timeout back to default.
                    theConnection.settimeout(RcvTimeOut_default)

                    dataRecieved = Utils.recv_file_UDP(theConnection)

                    Utils.print_file_stats(dataRecieved)
                    Utils.print_file_contents(dataRecieved, PrintFile)

                else:
                    Utils.quit_now_UDP()



    ### ECHO message request
            else:
                # Set the timeout and send the command.
                theConnection.settimeout(RcvTimeOut_default)
                theConnection.sendto(promtBytes, (HOST, PORT))

                dataRecieved = theConnection.recv(1024)
                Utils.print_dataRecieved(dataRecieved)

                Utils.quit_now_UDP ()



    ### NOTHING Request
    else:
        print ("Nothing sent. Please input a string or integer to transmit.")
        received = "Nothing recieved because nothing sent."



# Create a socket (SOCK_DGRAM means a UDP socket).
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
print_startup_msg()

start_here(clientSocket)