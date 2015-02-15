import socketserver
import socket
import datetime

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        timestamp = datetime.datetime.now().strftime("%I:%M%p")
        print (timestamp, "{} wrote: ".format(self.client_address[0]))
        print (self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    # HOST, PORT = "sweet.student.bth.se", 8120
    # HOST, PORT = "seekers.student.bth.se", 8120
    # HOST, PORT = "bumblebea.st", 8120
    HOST, PORT = "localhost", 8120

    # Create the server, binding to specified host and port
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    # socket = socketserver.BaseServer
    print (" ")
    print ("Started ardeidae_py TCP server.")
    print("Started TCP Server... waiting for clients.")
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", PORT)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()