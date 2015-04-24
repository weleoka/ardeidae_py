
TCP and UDP server-client pair written in Python.

This is for learning purposes whereby data segments can be sent and recieved.
The recommended tool to complement this experiment is Wireshark.

All servers and clients call for python 3.

Note: be aware of the fact that headers add to the size/length of the data transmitted:
TCP(20 Bytes + options(rare)) and UDP(8 Bytes) for each segment.
IPv4(20Bytes + options) and IPv6(40 Bytes) for each datagram.
Link layer frames also have headers: Ethernet (22 Bytes).

1 character utf-8 is assumed in this project to be equal to 1 Byte.

Note: When a transfer rate is claimed it is probably wildly inaccurate - check with wireshark.


## Usage
Commands are "quit", "stream" / "s", integer or string on the prompt. Stream (or just s) swithes to streaming mode. Integer request file, string requests an echo from server.

Be aware of the config variable PrintFile, if true will attempt to output the whole file to console of client

The servers need to bind to a host and port. These are listed in hosts.txt. The first item is the default host/port which makes starting that easier by just hitting enter at the prompt.

send_stream_TCP and send_stream_UDP functions in ardei_server_utils.py can be modified to send sequence numbered datagram payload or not.

#### Stream
The client can send a request for a segment stream by typing "stream" at prompt. The servers can send segments at a set interval specified by client, in miliseconds. The servers have a segment limit in their settings.

#### File
Servers will echo back the clients command, however if an integer is recieved by the server then a file of the coresponding number of characters will be generated and sent to the client.

After making a request for a "file" transfer the client will wait for a confirmation from the server.

If the file requested is particularly large the server will take quite a long time to generate it, and the server will not start sending segments util the file is ready, and after notifying the client of this fact.

Once a segment is recieved that notifies the client that the file is ready the client switches to recieve mode.

The TCP stack accepts all the file data from the application almost instantaniously so that a timer on TCP transmissions is not plausable at application level. Recieveing time is easy enough to measure, and from that a transfer rate can be calculated.

#### Transmission ending
The most significant differance between UDP clients and TCP clients is in their method of detecting the end of a transmission.

UDP client will wait for UDP segments to arrive until socket.settimeout() expires, the timeout value is reset for every segment recieved.. Change this value by changing RcvTimeOut_file variable. If requesting a large file from server it will take a while for the server to generate that file, if the client times out before the file begins to be sent by the server then try increasing value of RcvTimeOut_file.

TCP client checks for an empty byte string from the socket. If this is detected it assumes the end of transmission.


## Code and Style
* The server imports dependencies from ardei_server_utils.py and the clients from ardei_client_utils.py.
* The servers by default do not accept requests for greater than 123456789 character transfers.


## Bugs and Issues
Please report an issue if one is found.


## Licence
LICENCE.md for details.
Copyright (c) 2015 A.K. Weeks


## Sources, inspiration and notes
Credits go to docs.python.org, stack-overflow.com,
Computer Networking: A Top Down Approach by Ross Kurose.


#### Articles on RAW, TCP & UDP socket programming
http://www.binarytides.com/raw-socket-programming-in-python-linux/
http://www.binarytides.com/python-socket-programming-tutorial/2/
http://www.binarytides.com/programming-udp-sockets-in-python/

http://pymotw.com/2/SocketServer/index.html

http://docs.python.org/3.1/howto/sockets.html

#### Python & UNIX docs
https://docs.python.org/3/library/socket.html

https://docs.python.org/3/library/socketserver.html

If you want to find out more about the flags available in .recv():
http://www.unix.com/man-page/Linux/2/recv/



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


Theoretically, the maximum size of an IP datagram is 65535 bytes, imposed by the 16-bit total length field in the IP header. With an IP header of 20 bytes and a UDP header of 8 bytes, this leaves a maximum of 65507 bytes of user data in a UDP datagram. Most implementations, however, provide less than this maximum.