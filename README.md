# ardeidae_py

## TCP and UDP server-client written in Python.

This is for learning purposes whereby simple data packets can be sent and recieved.
The recommended tool to complement this experiment is Wireshark.

All servers and clients are optimised for python 3.

## TCP
### Server
Execute with shellscript: ./tcpser.sh
tcpser just echos back the clients command. The tcpSer Advanced accepts arguments.
Server default listening port: 8120

### Client
Execute client with bashscript ./tcpcli.sh

### Advanced Client/Server  TCP:
Look in the client code for HOST, PORT variable and change the values so that they correspond with the server which you are trying to connect to.


Input "ls" "chdir" "dl" and "quit" commands at prompt. Any other input returns echo.

* ls: requests and displays current working directory and all it's contents from the server
* chdir: changes current working directory of the server (args: the directory to change to)
* dl: downloads file (args: the file name to download)
* quit: disconnects from server and closes socket




## UDP
### Server
Right now the server just echo's back the clients message.
Execute with shellscript: ./udpser.sh
Server default listening port: 8121

### Client
Execute client with bashscript ./udpcli.sh


## Sources and inspiration
http://docs.python.org/3.1/howto/sockets.html

The yifi people

Computer Networking: A Top Down Approach by Kurose, Ross.


