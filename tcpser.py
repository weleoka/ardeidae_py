#!/usr/bin/env python3

import socketserver, socket, sys, re, time
from ardei_utils import ardei_server_utils

Utils = ardei_server_utils

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # SETTINGS
        FileLimit = 123456790 #allows 123456789 to be sent.
        StreamServerPaketLimit = 10001

        # self.request is the TCP socket connected to the client
        sReq = self.request
        data = sReq.recv(1024).strip()
        dataStr = data.decode('utf-8')
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
                        Utils.send_stream_TCP(sReq, txInterval, txPakets, data)
                    print ('Sending stream took %.03f sec.' % t.interval)

                else:
                    faultReport = Utils.make_faultReportStream(streamRequest[1], streamRequest[2])
                    sReq.sendall(faultReport)



    ### FILE Server handling
            elif recievedInteger:
                # Make the temporary file and generate confiramtion message.
                if recievedInteger < FileLimit:
                    print("\nMaking tempFile of " + str(recievedInteger) + " characters...")
                    tempFile = Utils.make_tempFile(recievedInteger)
                    print("File is prepared - confirmation sent to client. Now sending file.")
                    confirmation = Utils.make_confirmationReport(tempFile)
                    sReq.sendall(confirmation)

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        Utils.send_file_TCP(sReq, tempFile)
                    print('Sending took %.03f sec.' % t.interval)

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



if __name__ == "__main__":
    # Allow reuse of listening address. Useful if stoping and starting alot in development.
    socketserver.TCPServer.allow_reuse_address = True;

    HOST, PORT = Utils.select_host()

    try :
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        Utils.print_startup_msg_TCP(PORT)
        server.serve_forever()
    except socket.error as serr:
        print ('Failed to bind to socket: ' + str(serr))
        sys.exit()

