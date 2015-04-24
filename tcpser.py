#!/usr/bin/env python3

import socketserver, socket, sys, re
from ardei_utils import ardei_server_utils

Utils = ardei_server_utils

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # SETTINGS
        FileLimit = 123456790 # Allows 123456789 to be sent.
        StreamServerPaketLimit = 10001 # Restriction on number of segments to be streamed.
        sequenceNumber = False # Label each segment in streaming mode with a sequence number.

        # self.request is the TCP socket connected to the client
        sReq = self.request
        data = sReq.recv(1024).strip()
        dataStr = bytes.decode(data, 'utf-8')
        client_address = self.client_address[0]

        filetosend = False

        if len(data) > 0:
            try:
                recievedInteger = int(data)
            except:
                recievedInteger = False
                pass



    ### STREAM Server handling
            if re.search('stream', dataStr):
                streamRequest = (dataStr.split("-", 3))
                try:
                    txInterval = float(streamRequest[1])/1000
                    txPackets = int(streamRequest[2])
                    segmentSize = int(streamRequest[3])
                    print("TXinterval: " + str(txInterval) + " TXsegments: " + str(txPackets) + " Size: " + str(segmentSize))
                except:
                    print ("Error in streamRequest command: " + str(streamRequest))
                    txInterval = False
                    txPackets = False
                    segmentSize = False
                    pass

                if txInterval >= 0:
                    if txPackets > StreamServerPaketLimit:
                        txPackets = StreamServerPaketLimit

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        Utils.send_stream_TCP(sReq, txInterval, txPackets, segmentSize, sequenceNumber)
                    print('Sending took %.03f sec.' % t.interval)

                elif not txInterval or not txPackets or not segmentSize:
                    faultReport = Utils.make_faultReportStream(streamRequest[1], streamRequest[2], streamRequest[3])
                    sReq.sendall(faultReport)



    ### FILE Server handling
            elif recievedInteger:
                # Make the temporary file and generate confiramtion message.
                if recievedInteger < FileLimit:
                    tempFile = Utils.make_tempFile(recievedInteger)
                    print("File is prepared - confirmation sent to client. Now sending file.")
                    confirmation = Utils.make_confirmationReport(tempFile)
                    sReq.sendall(confirmation)

                    Utils.send_file_TCP(sReq, tempFile)

                # Make an error report and send to client.
                elif recievedInteger > FileLimit:
                    faultReport = Utils.make_faultReportFile(FileLimit, recievedInteger)
                    sReq.sendall(faultReport)



    ### ECHO Server handling
            else:
                echoReport = Utils.make_echoReport(data, client_address)
                self.request.sendall(echoReport)



    ### NOTHING Server handling
        else:
            Utils.print_emptyReport()



    def finish(self):
        Utils.print_jobDoneReport(self.client_address[0])
        print("The TCP connection is in Wait state, ctrl + c to quit.")



if __name__ == '__main__':
    # Allow reuse of listening address. Useful if stoping and starting a lot in development.
    socketserver.TCPServer.allow_reuse_address = True;

    HOST, PORT = Utils.prompt_select_host()

    try :
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    except socket.error as serr:
        print ('Failed to bind to socket: ' + str(serr))
        sys.exit()

    print("\nStarted TCP Server... waiting for clients.")
    Utils.print_startup_msg(PORT)
    server.serve_forever()


