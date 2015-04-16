#!/usr/bin/env python3
'''
This program generates a file of a certain length and sends it to a client.
If anything other than an integer is recieved from client it will echo the string back.
After processing one request the server will shut down.
'''

import socketserver, socket, sys, re, time
from ardei_utils import ardei_server_utils

# HOST, PORT = "sweet.student.bth.se", 8121
# HOST, PORT = "seekers.student.bth.se", 8121
# HOST, PORT = "ardeidae.computersforpeace.net", 8121
# HOST, PORT = "192.168.1.36", 8121
HOST, PORT = "localhost", 8121

Utils = ardei_server_utils

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # SETTINGS
        FileLimit = 123456789
        StreamServer = False
        StreamServerPaketLimit = 10000

        # self.request[1] is the UDP socket connected to the client
        data = self.request[0].strip()
        dataStr = data.decode('utf-8')
        client_address = self.client_address
        socket = self.request[1]

        filetosend = False
        print("HAANDLING")
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
                        socket.sendto(data, client_address)
                        txPakets = txPakets - 1
                else:
                    socket.sendto(data, client_address)



    ### FILE Server handling
            elif recievedInteger and recievedInteger < FileLimit:
                print ("detected integer")
                # Make the temporary file and generate confiramtion message
                tempFile = Utils.make_file(recievedInteger)
                confirmation = Utils.make_confirmation(tempFile)

                if socket.sendto(confirmation, client_address):
                    print ("File is prepared - confirmation sent to client. Now sending file.")

                    # Read the information from the file.
                    tempFile.seek(0)
                    buf = 1024
                    fileData = tempFile.read(buf)

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        while (fileData):
                            if(socket.sendto(fileData, client_address)):
                                fileData = tempFile.read(buf)
                    print ('Sending took %.03f sec.' % t.interval)

                    tempFile.close()

            elif recievedInteger and recievedInteger > FileLimit:
                faultReport = Utils.make_faultReport(FileLimit, recievedInteger)
                socket.sendto(faultReport, client_address)



    ### ECHO Server handling
            else:
                echoReport = Utils.make_echoReport(data, client_address)
                socket.sendto(echoReport, client_address)



    ### NOTHING Server handling
        else:
            Utils.print_emptyReport()



    def finish(self):
        Utils.print_jobDoneReport(self.client_address)



if __name__ == "__main__":

    try :
        server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
        Utils.print_startup_msg_UDP(PORT)
        server.serve_forever()
    except socket.error:
        print ('Failed to create socket.')
        sys.exit()



