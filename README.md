
TCP and UDP server-client pair written in Python.

This is for learning purposes whereby data packets can be sent and recieved.
The recommended tool to complement this experiment is Wireshark.

All servers and clients call for python 3.


## Usage
Commands are "quit", "stream", integer or string on the prompt. Stream swithes to streaming mode. Integer request file, string requests an echo from server.

Be aware of the config variable PrintFile, if true will attempt to output the whole file to console of client

The servers need to bind to a host and port. These are listed in hosts.txt. The first item is the default host/port which makes starting that easier by just hitting enter at the prompt.

#### Stream
The client can send a request for a paket stream by typing "stream" at prompt. The servers can send pakets at a set interval specified by client, in miliseconds. The servers have a paket limit in their settings.

#### File
Servers will echo back the clients command, however if an integer is recieved by the server then a file of the coresponding number of characters will be generated and sent to the client.

After making a request for a "file" transfer the client will wait for a confirmation from the server.

If the file requested is particularly large the server will take quite a long time to generate it, and the server will not start sending pakets util the file is ready, and after notifying the client of this fact.

Once a packet is recieved that notifies the client that the file is ready the client switches to recieve mode.

#### Transmission ending
The most significant differance between UDP clients and TCP clients is in their method of detecting the end of a transmission.

UDP client will wait for UDP packets to arrive until socket.settimeout() expires, the timeout value is reset for every packet recieved.. Change this value by changing RcvTimeOut_file variable. If requesting a large file from server it will take a while for the server to generate that file, if the client times out before the file begins to be sent by the server then try increasing value of RcvTimeOut_file.

TCP client checks for an empty byte string from the socket. If this is detected it assumes the end of transmission.



## Code and Style
* The server imports dependencies from ardei_server_utils.py and the clients from ardei_client_utils.py.
* The servers by default do not accept requests for greater than 123456789 character transfers.



## Bugs
* The TCP client-server pair when a request for a small file is made will sometimes appear to get data discrepancies. This could be from tempFile read/write or TCP send/recv buffers.



## Sources and inspiration
http://docs.python.org/3.1/howto/sockets.html

The yifi people

Computer Networking: A Top Down Approach by Kurose, Ross.



## Good to know and notes
#### https://docs.python.org/3/library/socket.html
#### flags: http://www.unix.com/man-page/Linux/2/recv/

#### socket.send(bytes[, flags])

Send data to the socket. The socket must be connected to a remote socket. The optional flags argument has the same meaning as for recv() above. Returns the number of bytes sent. Applications are responsible for checking that all data has been sent; if only some of the data was transmitted, the application needs to attempt delivery of the remaining data. For further information on this topic, consult the Socket Programming HOWTO.

#### socket.sendall(bytes[, flags])

Send data to the socket. The socket must be connected to a remote socket. The optional flags argument has the same meaning as for recv() above. Unlike send(), this method continues to send data from bytes until either all data has been sent or an error occurs. None is returned on success. On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent.

#### socket.sendto(bytes, address)
#### socket.sendto(bytes, flags, address)

Send data to the socket. The socket should not be connected to a remote socket, since the destination socket is specified by address. The optional flags argument has the same meaning as for recv() above. Return the number of bytes sent. (The format of address depends on the address family — see above.)


A fundamental truth of sockets: messages must either be fixed length (yuck),
or be delimited (shrug), or indicate how long they are (much better),
or end by shutting down the connection.
The choice is entirely yours, (but some ways are righter than others).



### Advanced Client/Server  TCP by ify:
Look in the client code for HOST, PORT variable and change the values so that they correspond with the server which you are trying to connect to.

Input "ls" "chdir" "dl" and "quit" commands at prompt. Any other input returns echo.

* ls: requests and displays current working directory and all it's contents from the server
* chdir: changes current working directory of the server (args: the directory to change to)
* dl: downloads file (args: the file name to download)
* quit: disconnects from server and closes socket