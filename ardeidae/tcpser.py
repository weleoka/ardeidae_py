'''
This program generates a file of a certain length and sends it to a client.
If anything other than an integer is recieved from client it will echo the string back.
After processing one request the server will shut down.
'''

import socketserver, socket, datetime, tempfile, os, sys



def makeFile(ri):
    tf = tempfile.NamedTemporaryFile()

    for x in range(0, ri):
        chunkStr = 'A'
        chunk = chunkStr.encode('utf-8')
        tf.write(chunk)

    return tf



def printStartupMsg():
    print (" ")
    print ("Started ardeidae_py TCP server.")
    print("Started TCP Server... waiting for clients.")
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", PORT)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))



class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        recievedInteger = False
        filetosend = False

        if len(self.data) > 0:

            try:
                recievedInteger = int(self.data)
            except:
                pass

            if recievedInteger and recievedInteger < 10000001:
                tempFile = makeFile(recievedInteger)

                # Read the information from the file.
                tempFile.seek(0)
                filetosend = tempFile.read()
                metadata = os.stat(tempFile.name)
                tempFile.close()

                # send confirmation message
                # sendingConfirm = "Transfer of file: " + tempFile.name + " size: " + str(metadata.st_size) + " Bytes starting...\n"
                # self.request.sendall(sendingConfirm.encode("utf-8"))

                #send file
                print ("\nSending a file (", tempFile.name, ") to client of " + str(metadata.st_size) + " Bytes.")
                self.request.sendall(filetosend)

            else:
                timestamp = datetime.datetime.now().strftime("%I:%M%p")
                print ("\n", timestamp, "{} wrote: ".format(self.client_address[0]))
                print (self.data)
                # just send back the same data, but upper-cased
                self.request.sendall(self.data.upper())

        else:
            print ("recieved client request of absolutely nothing.")


    def finish(self):
        print ("Server completed the job for ", self.client_address)
        print ("The TCP connection will be in Wait state, connect with the client again or ctrl + c to quit.")



if __name__ == "__main__":
    # HOST, PORT = "sweet.student.bth.se", 8120
    # HOST, PORT = "seekers.student.bth.se", 8120
    # HOST, PORT = "ardeidae.computersforpeace.net", 8120
    HOST, PORT = "localhost", 8120

    # Create the server, binding to specified host and port, allow reuse of listening address.
    socketserver.TCPServer.allow_reuse_address = True;
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    printStartupMsg()

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

