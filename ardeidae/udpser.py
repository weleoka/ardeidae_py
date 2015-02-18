import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0]
        socket = self.request[1]

        print ("{} wrote:".format(self.client_address[0]))
        print (data)
        socket.sendto(data.upper(), self.client_address)

    def finish(self):
        print ("Server completed the job for ", self.client_address)

if __name__ == "__main__":
    # HOST, PORT = "sweet.student.bth.se", 8121
    # HOST, PORT = "seekers.student.bth.se", 8121
    # HOST, PORT = "ardeidae.computersforpeace.net", 8121
    HOST, PORT = "localhost", 8121
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)

    print (" ")
    print ("Started ardeidy_py UDP Server.", server.server_address, " Yes!")

    server.serve_forever()