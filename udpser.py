#!/usr/bin/env python3

import socketserver, socket, sys, re
from ardei_utils import ardei_server_utils

Utils = ardei_server_utils

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # SETTINGS
        FileLimit = 123456790 # Allows 123456789 to be sent.
        StreamServerPaketLimit = 10001 # Restriction on number of segments to be streamed.
        txUnitSize = 1024 # How large each chunk of UDP data is that gets sent.
        sequenceNumber = False # Label each segment in streaming mode with a sequence number.

        # self.request[1] is the UDP socket connected to the client
        sReq = self.request[1]
        data = self.request[0].strip()
        dataStr = bytes.decode(data, 'utf-8')
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
                streamRequest = (dataStr.split("-", 3))
                try:
                    txInterval = float(streamRequest[1])/1000 # Convert milliseconds to seconds
                    txPackets = int(streamRequest[2])
                    segmentSize = int(streamRequest[3])
                    print("TXinterval: " + str(txInterval) + " TXsegments: " + str(txPackets) + " Size: " + str(segmentSize))
                except:
                    print("Error in streamRequest command: " + str(streamRequest))
                    txInterval = False
                    txPackets = False
                    segmentSize = False
                    pass

                if txInterval:
                    if txPackets > StreamServerPaketLimit:
                        txPackets = StreamServerPaketLimit

                    # TIMETAKE - sending stream.
                    with Utils.Timer() as t:
                        Utils.send_stream_UDP(sReq, client_address, txInterval, txPackets, segmentSize, sequenceNumber)
                    print('Sending stream took %.03f sec.' % t.interval)

                else:
                    faultReport = Utils.make_faultReportStream(streamRequest[1], streamRequest[2], streamRequest[3])
                    sReq.sendto(faultReport, client_address)



    ### FILE Server handling
            elif recievedInteger:
                # Make the temporary file and generate confiramtion message.
                if recievedInteger < FileLimit:
                    tempFile = Utils.make_tempFile(recievedInteger)
                    print("File is prepared - confirmation sent to client. Now sending file in %.1f segments." % (recievedInteger / txUnitSize))
                    confirmation = Utils.make_confirmationReport(tempFile)
                    sReq.sendto(confirmation, client_address)

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        Utils.send_file_UDP(sReq, client_address, txUnitSize, tempFile)
                    print("Sending took %.03f sec." % t.interval)

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



if __name__ == '__main__':

    HOST, PORT = Utils.prompt_select_host()

    try :
        server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    except socket.error as serr:
        print ('Failed to bind to socket: ' + str(serr))
        sys.exit()

    print ("\nStarted ardeidae_py UDP Server... waiting for clients.")
    Utils.print_startup_msg(PORT)
    server.serve_forever()

