#!/usr/bin/env python3
'''
This program generates a file of a certain length and sends it to a client.
If anything other than an integer is recieved from client it will echo the string back.
After processing one request the server will shut down.
'''

import socketserver, socket, datetime, os, sys
from ardei_utils import ardei_server_utils

# HOST, PORT = "sweet.student.bth.se", 8121
# HOST, PORT = "seekers.student.bth.se", 8121
# HOST, PORT = "ardeidae.computersforpeace.net", 8121
# HOST, PORT = "192.168.1.36", 8121
HOST, PORT = "localhost", 8121

Utils = ardei_server_utils

FileLimit = 123456789



def print_startup_msg():
    print (" ")
    print("Started ardeidae_py UDP Server... waiting for clients.")
    print ("Server running on host: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", PORT)
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
        # self.request[1] is the UDP socket connected to the client
        data = self.request[0].strip()
        socket = self.request[1]
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

                if socket.sendto(confirmation, self.client_address):
                    print ("confirmation sent!!!")

                    # Read the information from the file.
                    tempFile.seek(0)
                    buf = 1024
                    fileData = tempFile.read(buf)

                    # TIMETAKE - sending file.
                    with Utils.Timer() as t:
                        while (fileData):
                            if(socket.sendto(fileData, self.client_address)):
                                fileData = tempFile.read(buf)
                    print ('Sending took %.03f sec.' % t.interval)

                    tempFile.close()

            elif recievedInteger and recievedInteger > FileLimit:
                print ("Server recieved request for file larger than" + FileLimit + " chars. Rejected.")

            else:
                timestamp = datetime.datetime.now().strftime("%I:%M%p")
                print ("\n", timestamp, "{} wrote: ".format(self.client_address))
                print (data)
                # just send back the same data, but upper-cased
                socket.sendto(data.upper(), self.client_address)

        else:
            print ("Recieved client request of absolutely nothing.")



    def finish(self):
        print ("Server completed request from ", self.client_address)



if __name__ == "__main__":

    try :
        server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
        print_startup_msg()
        server.serve_forever()
    except socket.error:
        print ('Failed to create socket.')
        sys.exit()



