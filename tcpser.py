#!/usr/bin/env python3
'''
This program generates a file of a certain length and sends it to a client.
If anything other than an integer is recieved from client it will echo the string back.
After processing one request the server will shut down.
'''

import socketserver, socket, sys, re, time
from ardei_utils import ardei_server_utils

# HOST, PORT = "sweet.student.bth.se", 8120
# HOST, PORT = "seekers.student.bth.se", 8120
# HOST, PORT = "ardeidae.computersforpeace.net", 8120
# HOST, PORT = "192.168.1.36", 8120
HOST, PORT = "localhost", 8120

Utils = ardei_server_utils

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # SETTINGS
        FileLimit = 123456789
        StreamServer = False
        StreamServerPaketLimit = 10000

        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        dataStr = data.decode('utf-8')
        client_address = self.client_address[0]
        socket = self.request

        filetosend = False

        if len(data) > 0:
            try:
                recievedInteger = int(data)
            except:
                recievedInteger = False
                pass


    ### STREAM Server handling
            if re.search('stream', dataStr):
                StreamServer = True
                streamRequest = (dataStr.split("-", 2))
                try:
                    txInterval = int(streamRequest[1])/1000
                    txPakets = int(streamRequest[2])
                    print("TXinterval: " + str(txInterval) + " TXpakets: " + str(txPakets))
                except:
                    print ("Error in streamRequest command: " + str(streamRequest))
                    txInterval = False
                    txPakets = False
                    pass
                if txInterval:
                    if txPakets > StreamServerPaketLimit:
                        txPakets = StreamServerPaketLimit

                    while txPakets > 0:
                        time.sleep(txInterval)
                        socket.sendall(data)
                        txPakets = txPakets - 1
                else:
                    socket.sendall(data)



    ### FILE Server handling
            if recievedInteger and recievedInteger < FileLimit:

                # Make the temporary file and generate confiramtion message.
                tempFile = Utils.make_file(recievedInteger)
                confirmation = Utils.make_confirmation(tempFile)

                if socket.sendall(confirmation):
                    print ("File is prepared - confirmation sent to client. Now sending file.")

                    # Read the information from the file.
                    tempFile.seek(0)
                    buf = 1024
                    fileData = tempFile.read(buf)

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        while (fileData):
                            if(socket.sendall(fileData)):
                                fileData = tempFile.read(buf)
                    print ('Sending took %.03f sec.' % t.interval)

                    tempFile.close()

            elif recievedInteger and recievedInteger > FileLimit:
                faultReport = Utils.make_faultReport(FileLimit, recievedInteger)
                self.request.sendall(faultReport)



    ### ECHO Server handling
            else:
                echoReport = Utils.make_echoReport(data, client_address)
                self.request.sendall(echoReport)



    ### NOTHING Server handling
        else:
            Utils.print_emptyReport(client_address)



    def finish(self):
        Utils.print_jobDoneReport(self.client_address[0])
        print ("The TCP connection is in Wait state, connect with the client again or ctrl + c to quit.")



if __name__ == "__main__":
    # Allow reuse of listening address. Useful if stoping and starting alot in development.
    socketserver.TCPServer.allow_reuse_address = True;

    try :
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        Utils.print_startup_msg_TCP(PORT)
        server.serve_forever()
    except socket.error:
        print ('Failed to create socket.')
        sys.exit()

