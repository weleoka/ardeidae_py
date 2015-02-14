#!/usr/bin/env python3
import socket
import re
import os



# HOST, PORT = "sweet.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "seekers.student.bth.se", 8120                           #connect to bth, port
# HOST, PORT = "192.168.1.36", 8120                           #connect to localhost, port
HOST, PORT = "127.0.1.1", 8120

def recv_fixed_size(socket, MSGLEN):
    '''
       recv_fixed_size: function that uses socket.recv to continuiously receive data until a fixed amount of bytes are received

       parameters: socket, MSGLEN
           socket: the connected socket object used to receive the data
           MSGLEN: the number of bytes to be received

       returns: received data in a String object

       FUNCTION TAKEN FROM: http://docs.python.org/3.1/howto/sockets.html
   '''

    msg = ''
    while len(msg) < MSGLEN:
        chunk = socket.recv(MSGLEN-len(msg))
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg = msg + chunk.decode('utf-8')
    return msg


def recv_with_delimiter(socket, delimiter):
    '''
       recv_with_delimiter: function that uses socket.recv to continuously receive data until a delimiter is detected that signifies
       the end of the data being sent.  It is up to the sender to attach the delimiter to the data

       parameters: socket, delimiter
           socket: the connected socket object used to receive data
           delimiter: string containing the delimiter

       returns: received data in a String object

       Function written by theifyppl
   '''

    msg = ''
    notEoF = True

    while notEoF:
        chunk = socket.recv(4096)
        chunkStr = chunk.decode('utf-8')
        pattern = delimiter + '$'
        if re.search(pattern, chunkStr):
            chunkStr = re.sub(pattern, "", chunkStr) #delete delimiter
            chunk = chunkStr.encode('utf-8')
            notEoF = False

        msg = msg + chunk.decode('utf-8')
    return msg


def recv_file_with_size(socket, size):
    '''
       recv_file_with_size: function that uses socket.recv to continuously receive data for a file until a fixed size is reached
       Same as recv_fixed_size() except data is kept as a Bytes object, not a string

       parameters: socket, size
           socket: the connected socket object used to receive data
           size: projected file size

       returns: received data in a Bytes object

       Function heavily derived from: http://docs.python.org/3.1/howto/sockets.html
   '''

    msg = b''
    while len(msg) < size:
        chunk = socket.recv(size-len(msg))
        if chunk == '':
            raise RuntimeError("Socket connection broken")
        msg = msg + chunk
    return msg


def handshake(socket, msgToSend):
    ''' performs client/server handshake

       parameters:
           socket: The socket connected to the client
           msgToSend: The Bytes object to send to the client

       returns True on success, False on failure

       Function written by theifyppl
   '''

    received = recv_fixed_size(socket, 19)  # Note the fixed lenth of key.
    receivedASCII = received
    # pattern = '^bthDataComServerKey'
    pattern = ''

    socket.sendall(msgToSend)

    if re.search(pattern, receivedASCII):
        return True
    else:
        return False




if __name__ == '__main__':
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #create socket
    print(" ")
    print ("Trying to connect to: ", HOST, " on port ", PORT)
    clientSocket.connect((HOST, PORT))

    #handshakeMsg = b'bthDataComClientKey'
    handshakeMsg = ''
    if handshake(clientSocket, handshakeMsg):                           #if handshaking is successful
        print (" ")
        print ("___CONNECTED_TO_SERVER___")
        print ("Commands are: ls, chdir, dl, and quit:")
        print ("ls: requests and displays current server working directory and it's contents.")
        print ("chdir: changes current working directory of the server (args: the directory to change to).")
        print ("dl: downloads file (args: the file name to download).")
        print ("quit: disconnects from server and closes socket.")

        while True:
            print("")
            msg = input("Command: ")                                    #prompt user for command

            msg = msg + "929Z"                                          #add delimiter to command

            if msg == "quit929Z":                                       #if command == "quit" (plus delimiter), then send and close socket
                clientSocket.sendall(msg.encode('utf-8'))
                clientSocket.close()
                break;

            elif re.search(r"^dl", msg):                                #if command == "dl", download file using recv_file_with_size()
                clientSocket.sendall(msg.encode('utf-8'))

                confirm = recv_with_delimiter(clientSocket, "929Z")     #receive confirmation, file name, and file size from server

                if re.search(r"^Sending\b", confirm):                   #if confirmed

                    filePath = confirm.split(" ",1)
                    split = filePath[1].split("SpLiT", 1)               #split file name and file size
                    fileTuple = os.path.split(split[0])                 #if file name includes path, split it
                    fileName = fileTuple[1]                             #file name
                    fileSize = int(split[1])                            #file size

                    print("Downloading ", fileName, " into current directory...")
                    print("File size: ", str(fileSize), " bytes.")
                    f = open(fileName,"wb")                             #open/create file
                    fileData = recv_file_with_size(clientSocket, fileSize) #receive file data
                    f.write(fileData)                                   #write file data
                    f.close()                                           #close file
                    print("Done!")

                else:
                    print(confirm)                                      #if confirmation wasn't sent, print what was

            else:
                clientSocket.sendall(msg.encode('utf-8'))               #if command != "quit" or "dl", simply send it and wait for reply


                while True:
                    data = recv_with_delimiter(clientSocket, "929Z")
                    print(data)
                    break;