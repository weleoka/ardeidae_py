import time
import tempfile
import os
import re
import socket
import sys
"""
These are the reqired functions for the Ardeiday_py clients to run properly.

Functions include a simple timer module, as well as functions for recieving a file over UDP or TCP,
and also to test a response from a server for confirmations and status updates.
"""



"""
Time object.
"""
class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start



"""
Output to console file stats.
parameters:
    rf: the recieved file.

returns void.
"""
def print_file_stats (rf):
    metadata = os.stat(rf.name)
    print ("Recieved file \n (", rf.name, ")") # \n size: " + str(metadata.st_size) + " bytes.")



"""
Output to console file contents.
Depends on settings specified. Will either print contents, or only length of conents.
parameters:
    rf: the recieved file.
    PrintFile: the settings parameter.

returns void.
"""
def print_file_contents (rf, PrintFile):
    buf = 1024
    i = 0
    rf.seek(0)

    data = rf.read(buf)

    while data:
        tmpstr = data.decode('utf-8')
        if PrintFile:
            print (tmpstr)
        i = i + len(tmpstr)
        data = rf.read(buf)

    print ("Total recieved: " +str(i) + " chars.")
    rf.close()



"""
Output to console recieved data.
parameters:
    rd: the recieved data.

returns void.
"""
def print_dataRecieved(rd):
    print ("Received {0} bytes of data.".format(sys.getsizeof(rd)))
    print (str(rd))



"""
Decide what to do after a response from server.
parameters:
    cnct: The connection.

returns boolean.
"""
def monitor_server_response (cnct):
    while True:
        try:
            chunkStr = cnct.recv(1024)
            response = chunkStr.decode('utf-8')
            if re.search('file_prepared', response):
                print ("Server has prepared the file, recieving...")
                return True
            else:
                print (str(response))
                return False
        except socket.timeout:
            print ("Client timed out. Try increasing RcvTimeOut")
            return False



"""
======== U D P =============
"""



"""
UDP Recieve data and write to named temporary file.
parameters:
    cnct: The connection.

returns tf, temporaryfile instance.
"""
def recv_file_UDP(cnct):
    tf = tempfile.NamedTemporaryFile()

    while True:
        try:
            chunk = cnct.recv(1024)
            tf.write(chunk)
        except socket.timeout:
            tf.flush() # Flush the write buffer to file.
            return tf



"""
Recieve data STREAM over UDP and write to named temporary file.

parameters:
    cnct: The connection.

returns tf, temporaryfile instance.
"""
def recv_stream_UDP(cnct):
    msg = ''

    while True:
        try:
            chunk = cnct.recv(1024)
        except socket.timeout:
            print("Socket timed out on recv_stream.")
            return msg



"""
======== T C P =============
"""



"""
TCP Recieve data and write to named temporary file.
parameters:
    cnct: The connection.
    MSGLEN: the file size requested.

returns tf, temporaryfile instance.
"""
def recv_file_TCP(cnct):
    tf = tempfile.NamedTemporaryFile()
    while True:
        chunk = cnct.recv(1024)#MSGLEN-len(msg))
        tf.write(chunk)

        if chunk == b'':
            print (chunk)
            tf.flush()
            return tf



"""
Recieve data STREAM over TCP and write to named temporary file.

parameters:
    cnct: The connection.

returns msg, string.
returns counter, integer.
"""
def recv_stream_TCP(cnct):
    msg = ''
    counter = 0

    while True:
        chunk = cnct.recv(1024)
        chunkStr = chunk.decode('utf-8')

        if chunk == b'':
           return msg, counter

        msg = msg + chunkStr
        counter = counter + 1