#!/usr/bin/env python3
'''
This program generates a file of a certain length and sends it to a client.
If anything other than an integer is recieved from client it will echo the string back.
After processing one request the server will shut down.
'''

import socketserver, socket, sys, re, time
from ardei_utils import ardei_server_utils

Utils = ardei_server_utils

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # SETTINGS
        FileLimit = 123456790 #allows 123456789 to be sent.
        StreamServerPaketLimit = 10001 #Restriction on number of pakets to be streamed.
        txUnitSize = 1024 #How large each chunk of UDP data is that gets sent.

        # self.request[1] is the UDP socket connected to the client
        sReq = self.request[1]
        data = self.request[0].strip()
        dataStr = data.decode('utf-8')
        client_address = self.client_address

        filetosend = False

        if len(data) > 0:
            try:
                recievedInteger = int(data)
            except:
                recievedInteger = False
                pass



    ### STREAM Server handling
            if re.search('stream', dataStr):
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

                    # TIMETAKE - sending stream.
                    with Utils.Timer() as t:
                        Utils.send_stream_UDP(sReq, client_address, txInterval, txPakets, data)
                    print ('Sending stream took %.03f sec.' % t.interval)

                else:
                    faultReport = Utils.make_faultReportStream(streamRequest[1], streamRequest[2])
                    sReq.sendto(faultReport, client_address)



    ### FILE Server handling
            elif recievedInteger:
                # Make the temporary file and generate confiramtion message.
                if recievedInteger < FileLimit:
                    print("\nMaking tempFile of " + str(recievedInteger) + " characters...")
                    tempFile = Utils.make_tempFile(recievedInteger)
                    print("File is prepared - confirmation sent to client. Now sending file.")
                    confirmation = Utils.make_confirmationReport(tempFile)
                    sReq.sendto(confirmation, client_address)

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        Utils.send_file_UDP(sReq, client_address, txUnitSize, tempFile)
                    print('Sending took %.03f sec.' % t.interval)

                # Make an error report and send to client.
                elif recievedInteger > FileLimit:
                    faultReport = Utils.make_faultReportFile(FileLimit, recievedInteger)
                    sReq.sendto(faultReport, client_address)



    ### ECHO Server handling
            else:
                echoReport = Utils.make_echoReport(data, client_address)
                sReq.sendto(echoReport, client_address)



    ### NOTHING Server handling
        else:
            Utils.print_emptyReport()



    def finish(self):
        Utils.print_jobDoneReport(self.client_address)



if __name__ == "__main__":

    HOST, PORT = Utils.select_host()

    try :
        server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
        Utils.print_startup_msg_UDP(PORT)
        server.serve_forever()
    except socket.error:
        print ('Failed to bind to socket.')
        sys.exit()



