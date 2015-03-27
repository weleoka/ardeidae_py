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
    print ("Started ardeidae_py UDP server.")
    print("Started UDP Server... waiting for clients.")
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", PORT)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))



class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):

        # self.request is the UDP socket connected to the client
        data = self.request[0]
        socket = self.request[1]
        recievedInteger = False
        filetosend = False

        if len(data) > 0:

            try:
                recievedInteger = int(data)
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
                # socket.sendto(sendingConfirm.encode("utf-8"), self.client_address)

                print ("\nSending a file (", tempFile.name, ") to client of length: " + str(metadata.st_size) + " and size: " + str(sys.getsizeof(filetosend)) + " Bytes.")
                socket.sendto(filetosend, self.client_address)

            else:
                timestamp = datetime.datetime.now().strftime("%I:%M%p")
                print ("\n", timestamp, "{} wrote: ".format(self.client_address))
                print (data)
                # just send back the same data, but upper-cased
                socket.sendto(data.upper(), self.client_address)

        else:
            print ("recieved client request of absolutely nothing.")


    def finish(self):
        print ("Server completed the job for ", self.client_address)


'''
Find out how to buffer and send with UDP like the tcp.sock doest with "sendall".
'''

if __name__ == "__main__":
    # HOST, PORT = "sweet.student.bth.se", 8121
    # HOST, PORT = "seekers.student.bth.se", 8121
    # HOST, PORT = "ardeidae.computersforpeace.net", 8121
    # HOST, PORT = "192.168.1.36", 8121
    HOST, PORT = "localhost", 8121

    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)

    printStartupMsg()

    server.serve_forever()
