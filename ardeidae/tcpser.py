'''
This program generates a random file of certain length and sends it to a client.

for line in temp_file.readlines():
    print line

import time
#use time.time() on Linux
start = time.clock()
for x in range(1000):
    pass
stop = time.clock()

print stop-start

start = time.clock()
for x in xrange(1000):
    pass
stop = time.clock()

print stop-start

'''

import socketserver
import socket
import datetime
import tempfile
import os

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        recievedInteger = 0
        filetosend = False

        if len(self.data) > 0:

            try:
                recievedInteger = int(self.data)
            except:
                pass

            if recievedInteger > 0:
                tf = tempfile.NamedTemporaryFile()
                for x in range(1, recievedInteger + 1):
                    if x < 10:
                        chunkStr = 'line : 0' + str(x) + '\n'
                    else:
                        chunkStr = 'line : ' + str(x) + '\n'

                    chunk = chunkStr.encode('utf-8')
                    tf.write(chunk)

                tf.seek(0)
                filetosend = tf.read()
                metadata = os.stat(tf.name)
                tf.close()

                sendingConfirm = "Transfer of file: " + tf.name + " size: " + str(metadata.st_size) + " Bytes \n" #Message = "Sending " + filename + split + filesize

                self.request.sendall(sendingConfirm.encode("utf-8"))  #send confirmation message
                self.request.sendall(filetosend)                            #send file
                print ("Sent a file to client of " + str(metadata.st_size) + " Bytes.")

            else:
                timestamp = datetime.datetime.now().strftime("%I:%M%p")
                print (timestamp, "{} wrote: ".format(self.client_address[0]))
                print (self.data)
                # just send back the same data, but upper-cased
                self.request.sendall(self.data.upper())
        else:
            print ("recieved client request of absolutely nothing")


if __name__ == "__main__":
    # HOST, PORT = "sweet.student.bth.se", 8120
    # HOST, PORT = "seekers.student.bth.se", 8120
    # HOST, PORT = "ardeidae.computersforpeace.net", 8120
    HOST, PORT = "localhost", 8120

    # Create the server, binding to specified host and port, allow reuse of listening address.
    socketserver.TCPServer.allow_reuse_address = True;
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    print (" ")
    print ("Started ardeidae_py TCP server.")
    print("Started TCP Server... waiting for clients.")
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", PORT)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()