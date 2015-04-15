#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_STREAM
import sys
from ardei_utils import ardei_client_utils
Utils = ardei_client_utils



# HOST, PORT = "sweet.student.bth.se", 8120               #connect to bth, port
# HOST, PORT = "seekers.student.bth.se", 8120            #connect to bth, port
# HOST, PORT = "192.168.1.36", 8120                           #connect to localhost, port
# HOST, PORT = "127.0.1.1", 8120                                #connect to localhost, port
HOST, PORT = "localhost", 8120                                  #connect to localhost, port
# HOST, PORT = "bumblebea.st", 8120
# HOST, PORT = "ardeidae.computersforpeace.net", 8120

# Specify if recieved files are to be output to terminal or not.
PrintFile = False
# How long to wait before quitting the recieve state.
RcvTimeOut = 5



"""
Startup and quit functions.
"""
def print_startup_msg():
    print (" ")
    print ("Started ardeidae_py TCP client.")
    print ("Trying to connect to TCP server: ", HOST, " on port: ", PORT, "...wait.")

def quit_now (cnct):
    cnct.close()
    print ("...disconnected from ", HOST)
    print ("Shutting down client...")
    sys.exit()



"""
Main function
"""
def start_here (theConnection):
    typedInteger = False

    message = input('PROMPT: ')
    messageBytes = str.encode(message)

    try:
        typedInteger = int(message)
    except:
        pass

    if len(message) > 0:
        if str(message) == 'quit':
            quit_now(theConnection)

        else:
            theConnection.sendall(messageBytes)

            if typedInteger:
                print ("Please wait for " + str(RcvTimeOut) + " seconds for the server to prepare your file.\n..........")

                # Wait for server to generate confirmation message
                if Utils.monitor_server_response(theConnection):
                    # TIMETAKE
                    with Utils.Timer() as t:
                        dataRecieved = Utils.recv_file_with_size_TCP(theConnection, typedInteger)
                    print ('Recieving took %.03f sec.' % t.interval)

                    Utils.print_file_stats(dataRecieved)
                    Utils.print_file_contents(dataRecieved, PrintFile)

                else:
                    print ("Server response delayed or missing.")
                    quit_now(theConnection)

            else:
                dataRecieved = theConnection.recv(1024)

                Utils.print_data_stats(dataRecieved)
                Utils.print_data_contents(dataRecieved)
                quit_now (theConnection)

    else:
        print ("Nothing sent. Please input a string or integer(10 million max) to transmit.")
        received = "Nothing recieved because nothing sent."


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
