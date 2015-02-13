# ardeidae_py

TCP and UDP server-client written in Python.


TCP versions of server-client run on python 3.
Execute with shellscript: ./tcpser.sh and ./tcpcli.sh
Server default listening port: 8120

UDP versions of server-client run on python 3.
Right now the server just echo's back the clients message.
Server default listening port: 8121


Look in the client code for HOST, PORT variable and change the values.


Client  TCP:
Input "ls" "chdir" "dl" and "quit" commands at prompt. Any other input returns echo.

ls: requests and displays current working directory and all it's contents from the server
chdir: changes current working directory of the server (args: the directory to change to)
dl: downloads file (args: the file name to download)
quit: disconnects from server and closes socket



------------

Course work material. Sources: the interwebs and:

http://docs.python.org/3.1/howto/sockets.html

Computer Networking: A Top Down Approach by Kurose, Ross.


