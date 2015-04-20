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
Startup function.
"""
def print_startup_msg():
    print (" ")
    print ("Started ardeidae_py TCP client.")
    print ("Trying to connect to TCP server: ", HOST, " on port: ", PORT, "...wait.")



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
        elif str(prompt) == 'stream':
            print("Switching server to stream mode")
            interval = input('\nPlease input the paket TX interval (miliseconds) required: ')
            pakets = input('\nPlease input the number of pakets required: ')

            streamRequest = str.encode('stream-' + str(interval) + '-' + str(pakets))
            theConnection.sendall(streamRequest)

            streamData, counter = Utils.recv_stream_TCP(theConnection, recvBuffSize)
            print("Recieved: " + str(len(streamData)/len(streamRequest)) + " pakets (count: " + str(counter) + ").")



    ### FILE Request
        else:
            if typedInteger:
                # Send the command.
                theConnection.sendall(promptBytes)

                # Wait for server to generate confirmation message
                print ("Please wait for the server to prepare your file.\n..........")
                if Utils.monitor_server_response(theConnection):

                    dataRecieved = Utils.recv_file_TCP(theConnection, recvBuffSize)

                    Utils.print_file_stats(dataRecieved)
                    Utils.print_file_contents(dataRecieved, PrintFile)

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


HOST, PORT = Utils.select_host()

# Create a socket (SOCK_STREAM means a TCP socket), connect to server.
clientSocket = socket.socket(AF_INET, SOCK_STREAM)
print_startup_msg()

try:
    clientSocket.connect((HOST, PORT))
    print ("...connected.")
    print ("(please input string to echo, or integer to request file of certain number Bytes).")
except:
    print ("Failed to connect to server.")
    sys.exit()

start_here(clientSocket)
