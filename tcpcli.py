#!/usr/bin/env python3

import socket
from socket import AF_INET, SOCK_STREAM
import sys
from ardei_utils import ardei_client_utils

Utils = ardei_client_utils

# Specify if recieved files are to be output to terminal or not.
PrintFile = False
#How large each chunk of TCP data is that gets recv:d.
recvBuffSize = 1024



"""
Main function
"""
def start_here (theConnection):
    prompt = input('PROMPT: ')
    promptBytes = str.encode(prompt)

    if len(prompt) > 0:
        try:
            typedInteger = int(prompt)
        except:
            typedInteger = False
            pass



    ### QUIT Request
        if str(prompt) == 'quit':
            Utils.quit_now_TCP(theConnection)



    ### STREAM Request
        elif str(prompt) == 'stream' or str(prompt) == 's':
            interval, segments, segmentSize = Utils.prompt_stream()

            streamRequest = str.encode('stream-' + str(interval) + '-' + str(segments) + '-' + str(segmentSize))
            theConnection.sendall(streamRequest)

            streamData, counter = Utils.recv_stream_TCP(theConnection, recvBuffSize)
            print("Recieved " + str(counter) + " segments.")



    ### FILE Request
        else:
            if typedInteger:
                # Send the command.
                theConnection.sendall(promptBytes)

                # Wait for server to generate confirmation message
                if Utils.monitor_server_response(theConnection):

                    # TIMETAKE.
                    with Utils.Timer() as t:
                        tempFile = Utils.recv_file_TCP(theConnection, recvBuffSize)

                    Utils.print_file_stats(tempFile, typedInteger)
                    Utils.print_transferRate(t.interval, typedInteger)
                    Utils.print_file_contents(tempFile, PrintFile)

                else:
                    Utils.quit_now_TCP(theConnection)



    ### ECHO message request
            else:
                # Send the command.
                theConnection.sendall(promptBytes)

                dataRecieved = theConnection.recv(recvBuffSize)
                Utils.print_dataRecieved(dataRecieved)

                Utils.quit_now_TCP (theConnection)



    ### NOTHING Request
    else:
        print ("Nothing sent. Please input a string or integer to transmit.")
        received = "Nothing recieved because nothing sent."



### Select HOST and PORT.
HOST, PORT = Utils.prompt_select_host()

# Create a socket (SOCK_STREAM means a TCP socket), connect to server.
clientSocket = socket.socket(AF_INET, SOCK_STREAM)

print ("\nStarted ardeidae_py TCP client.")
Utils.print_startup_msg(HOST, PORT)

try:
    clientSocket.connect((HOST, PORT))
except socket.error as serr:
    print ('Failed to connect to server: ' + str(serr))
    sys.exit()

print ("...connected.")
start_here(clientSocket)
