# ardeidae_py

## TCP and UDP server-client written in Python.

This is for learning purposes whereby simple data packets can be sent and recieved.
The recommended tool to complement this experiment is Wireshark.


### TCP versions of server-client run on python 3.
Execute with shellscript: ./tcpser.sh and ./tcpcli.sh
Server default listening port: 8120

### UDP versions of server-client run on python 3.
Right now the server just echo's back the clients message.
Server default listening port: 8121



### Client  TCP:
Look in the client code for HOST, PORT variable and change the values so that they correspond with the server which you are trying to connect to.


Input "ls" "chdir" "dl" and "quit" commands at prompt. Any other input returns echo.

* ls: requests and displays current working directory and all it's contents from the server
* chdir: changes current working directory of the server (args: the directory to change to)
* dl: downloads file (args: the file name to download)
* quit: disconnects from server and closes socket



### Client  UDP:
Takes one argument text-string on commandline which is then sent to server.



## Sources and inspiration.
http://docs.python.org/3.1/howto/sockets.html

The yifi people

Computer Networking: A Top Down Approach by Kurose, Ross.


