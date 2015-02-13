import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print ("{} wrote:".format(self.client_address[0]))
        print (data)
        socket.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    # HOST, PORT = "sweet.student.bth.se", 8121
    # HOST, PORT = "seekers.student.bth.se", 8121
    HOST, PORT = "localhost", 8121
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()