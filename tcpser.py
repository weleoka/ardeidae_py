#!/usr/bin/env python3
'''
This program generates a file of a certain length and sends it to a client.
If anything other than an integer is recieved from client it will echo the string back.
After processing one request the server will shut down.
'''

import socketserver, socket, datetime, os, sys
from ardei_utils import ardei_server_utils

# HOST, PORT = "sweet.student.bth.se", 8120
# HOST, PORT = "seekers.student.bth.se", 8120
# HOST, PORT = "ardeidae.computersforpeace.net", 8120
# HOST, PORT = "192.168.1.36", 8120
HOST, PORT = "localhost", 8120

Utils = ardei_server_utils

FileLimit = 123456789



def print_startup_msg():
    print (" ")
    print("Started TCP Server... waiting for clients.")
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", PORT)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))



class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        socket = self.request
        recievedInteger = False
        filetosend = False

        if len(data) > 0:

            try:
                recievedInteger = int(data)
            except:
                pass

            if recievedInteger and recievedInteger < FileLimit:
                tempFile = Utils.make_file(recievedInteger)

                metadata = os.stat(tempFile.name)
                print ("\nSending a file \n (", tempFile.name, ") \n size: " + str(metadata.st_size) + " bytes.")

                # send confirmation message
                confirmation = str.encode('file_prepared', 'utf-8')

                if self.request.sendall(confirmation):
                    print ("confirmation sent.")

                    # Read the information from the file.
                    tempFile.seek(0)
                    buf = 1024
                    fileData = tempFile.read(buf)

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        while (fileData):
                            if(self.request.sendall(fileData)):
                                fileData = tempFile.read(buf)
                    print ('Sending took %.03f sec.' % t.interval)

                    tempFile.close()

            elif recievedInteger and recievedInteger > FileLimit:
                print ("Server recieved request for file larger than" + FileLimit + " chars. Rejected.")

            else:
                timestamp = datetime.datetime.now().strftime("%I:%M%p")
                print ("\n", timestamp, "{} wrote: ".format(self.client_address[0]))
                print (data)
                # just send back the same data, but upper-cased
                self.request.sendall(data.upper())

        else:
            print ("recieved client request of absolutely nothing.")


    def finish(self):
        print ("Server completed the job for ", self.client_address)
        print ("The TCP connection will be in Wait state, connect with the client again or ctrl + c to quit.")



if __name__ == "__main__":
    # Allow reuse of listening address.
    # socketserver.TCPServer.allow_reuse_address = True;

    try :
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        print_startup_msg()
        server.serve_forever()
    except socket.error:
        print ('Failed to create socket.')
        sys.exit()

