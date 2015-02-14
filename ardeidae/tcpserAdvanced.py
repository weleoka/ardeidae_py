#!/usr/bin/env python3
import socket
import re
import os
import glob


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


def handshake(socket, msgToSend):
    ''' performs client/server handshake

       parameters:
           socket: The socket connected to the client
           msgToSend: The Bytes object to send to the client

       returns True on success, False on failure

       Function written by theifyppl
   '''

    socket.sendall(msgToSend)
    received = recv_fixed_size(socket, 19) # Note the fixed length of key.
    receivedASCII = received
    # pattern = '^bthDataComClientKey'
    pattern = ''
    if re.search(pattern, receivedASCII):
        return True
    else:
        return False




if __name__ == '__main__':

    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          #create socket

    thisPort = 8120

    print("Started TCP Server... waiting for clients.")
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", thisPort)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))
    # servSocket.bind((socket.gethostname(), thisPort))
    servSocket.bind(('', thisPort))                   #bind socket to port 8120, accept connections from all hosts
    servSocket.listen(2)                                                    #listen on socket, number of queued requests. MAX 5.

    while True:
        (communicationSocket, addr) = servSocket.accept()                   #accept connection
                                                                            #communicationSocket can now be used to send/recv messages

        print("A connection from ", addr, " has been accepted.")

        handshakeMsg = b'bthDataComServerKey'
        # handshakeMsg = ''
        if handshake(communicationSocket, handshakeMsg):                    #if handshake is successful
            print("Receiving commands...")
            communicating = True
            while communicating:

                dataStr = recv_with_delimiter(communicationSocket, "929Z")  #delimiter is 929Z + end of string

                if re.search("^ls$", dataStr):                              #if command == "ls"
                    #list directories & files
                    listFiles = glob.glob("*.*")
                    listDir = glob.glob("*")
                    for x in listFiles:
                        listDir.remove(x)

                    sending = "Current Working Directory: " + os.getcwd() + "\n\n"
                    sending = sending + "Folders: \n\n"
                    for x in listDir:
                        sending = sending + x + "\n"

                    sending = sending + "\n"

                    sending = sending + "Files: \n\n"
                    for x in listFiles:
                        sending = sending + x + "\n"

                    sending = sending + "929Z"

                    communicationSocket.sendall(sending.encode('utf-8'))      #send client the list of files & folders

                    print("Sent list of files and directories!")

                elif re.search(r"^chdir\b", dataStr):                         #if command == "chdir" + directory to change to
                    #change directory
                    try:
                        s = dataStr.split(" ", 1)
                        if len(s) >= abs(2):
                            path = s[1]
                            # os.chdir(path)
                            # print("Changed current working directory to: ", os.getcwd())
                            print("Directory changing not allowed.")
                            newDir = "The new current working directory on the server is: " + os.getcwd() + "929Z"
                        else:
                            newDir = "Not a recognised directory.929Z"
                        communicationSocket.sendall(newDir.encode('utf-8'))
                    except OSError as e:                                       #if invalid path
                        print("Invalid path!")
                        communicationSocket.sendall(b'Invalid Path!929Z')

                elif re.search(r"^dl", dataStr):                               #if command == "dl" + file to download
                    #download file
                    try:
                        s = dataStr.split(" ",1)
                        file = s[1]
                        f = open(file, "rb")
                        data = f.read()
                        f.close()

                        metadata = os.stat(file)

                        sendingConfirm = "Sending " + file + "SpLiT" + str(metadata.st_size) + "929Z" #Message = "Sending " + filename + split + filesize

                        communicationSocket.sendall(sendingConfirm.encode("utf-8"))  #send confirmation message

                        communicationSocket.sendall(data)                            #send file

                    except Exception as err:
                        print(format(err))
                        communicationSocket.sendall(b'Invalid File!929Z')

                elif re.search("^quit$", dataStr):                                 #if command == "quit"
                    print("Client has quit the connection.")
                    communicationSocket.close()
                    communicating = False

                else:                                                               #if command is unrecognized
                    print("Unrecognized Command: ", dataStr)
                    response = "Unrecognized Command!" + "929Z"
                    communicationSocket.sendall(response.encode('utf-8'))

        else:
            print("The handshake was unsuccessful. Continuing to listen...")        #if connection/handshake was unsuccessful



