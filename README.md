
TCP and UDP server-client pair written in Python.

This is for learning purposes whereby simple data packets can be sent and recieved.
The recommended tool to complement this experiment is Wireshark.

All servers and clients call for python 3.

## TCP
### Server
Execute as shellscript: ./tcpser.py
tcpser just echos back the clients command. Or if an integer is entered at the prompt then the server will generate a file of the corresponding number of characters and send that file to client.

The server can be switched to stream mode and will then send a set number of pakets at a set interval.

Server default listening port: 8120

### Client
Execute client as shellscript ./tcpcli.py

### Advanced Client/Server  TCP:
Look in the client code for HOST, PORT variable and change the values so that they correspond with the server which you are trying to connect to.


Input "ls" "chdir" "dl" and "quit" commands at prompt. Any other input returns echo.

* ls: requests and displays current working directory and all it's contents from the server
* chdir: changes current working directory of the server (args: the directory to change to)
* dl: downloads file (args: the file name to download)
* quit: disconnects from server and closes socket




## UDP
### Server
Execute as shellscript: ./udpser.py
The server just echo's back the clients message. Or if an integer is entered at the prompt then the server will generate a file of the corresponding number of characters and send that file to client.

The server can be switched to stream mode and will then send a set number of pakets at a set interval.

Server default listening port: 8121

### Client
Execute client as shellscript ./udpcli.py

After making a request for a "file" transfer the client will wait for RcvTimeOut.

If the "file" requested is particularly large the server will take quite a long time to generate it, and the server will not start sending pakets util the file is ready, this is why the client has a RcvTimeOut for waiting for a response from the server.

Once a UDP paket is recieved that notifies the client that the file is ready the client switches to recieve file mode.
For each paket arriving RcvTimeOut is reset.





## Code and Notes
* The server imports dependencies from ardei_server_utils.py and the clients from ardei_client_utils.py.
* The servers by default do not accept requests for greater than 123456789 character transfers.

- TCP: Fix the recieve file/stream function to not loop for ever.
- UDP: The timer on function: recv_file_with_size will include the RcvTimeOut value.



## Sources and inspiration
http://docs.python.org/3.1/howto/sockets.html

The yifi people

Computer Networking: A Top Down Approach by Kurose, Ross.




### https://docs.python.org/3/library/socket.html
flags: http://www.unix.com/man-page/Linux/2/recv/

socket.send(bytes[, flags])

    Send data to the socket. The socket must be connected to a remote socket. The optional flags argument has the same meaning as for recv() above. Returns the number of bytes sent. Applications are responsible for checking that all data has been sent; if only some of the data was transmitted, the application needs to attempt delivery of the remaining data. For further information on this topic, consult the Socket Programming HOWTO.

socket.sendall(bytes[, flags])

    Send data to the socket. The socket must be connected to a remote socket. The optional flags argument has the same meaning as for recv() above. Unlike send(), this method continues to send data from bytes until either all data has been sent or an error occurs. None is returned on success. On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent.

socket.sendto(bytes, address)
socket.sendto(bytes, flags, address)

    Send data to the socket. The socket should not be connected to a remote socket, since the destination socket is specified by address. The optional flags argument has the same meaning as for recv() above. Return the number of bytes sent. (The format of address depends on the address family — see above.)


A fundamental truth of sockets: messages must either be fixed length (yuck),
or be delimited (shrug), or indicate how long they are (much better),
or end by shutting down the connection.
The choice is entirely yours, (but some ways are righter than others).