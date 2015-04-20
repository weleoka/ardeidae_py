#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_DGRAM
import sys
from ardei_utils import ardei_client_utils

Utils = ardei_client_utils

# Specify if recieved files are to be output to terminal or not.
PrintFile = False
# How long to wait for the server to generate a file.
RcvTimeOut_file = 15
# Default timeout for client if nothing recieved.
RcvTimeOut_default = 2
#How large each chunk of UDP data is that gets recv:d.
recvBuffSize = 1024



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

            streamData = Utils.recv_stream_UDP(theConnection, recvBuffSize)
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

                    dataRecieved = Utils.recv_file_UDP(theConnection, recvBuffSize)

                    Utils.print_file_stats(dataRecieved)
                    Utils.print_file_contents(dataRecieved, PrintFile)

                else:
                    Utils.quit_now_UDP()



    ### ECHO message request
            else:
                # Set the timeout and send the command.
                theConnection.settimeout(RcvTimeOut_default)
                theConnection.sendto(promtBytes, (HOST, PORT))

                dataRecieved = theConnection.recv(recvBuffSize)
                Utils.print_dataRecieved(dataRecieved)

                Utils.quit_now_UDP ()



    ### NOTHING Request
    else:
        print ("Nothing sent. Please input a string or integer to transmit.")
        received = "Nothing recieved because nothing sent."


HOST, PORT = Utils.select_host()

# Create a socket (SOCK_DGRAM means a UDP socket).
clientSocket = socket.socket(AF_INET, SOCK_DGRAM)
print_startup_msg()

start_here(clientSocket)