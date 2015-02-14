import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print ("{} wrote: ".format(self.client_address[0]))
        print (self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    # HOST, PORT = "sweet.student.bth.se", 8120
    # HOST, PORT = "seekers.student.bth.se", 8120
    HOST, PORT = "localhost", 8120

    # Create the server, binding to specified host and port
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    print (" ")
    print ("Started ardeidae_py TCP server.")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()