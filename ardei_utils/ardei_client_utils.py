import time
import tempfile
import os
import re
import socket



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
File data recieved functions.
"""
def recv_file_with_size(cnct):
    tf = tempfile.NamedTemporaryFile()
    msg = b''

    while True:
        try:
            chunkStr = cnct.recv(1024)
            tf.write(chunkStr)
        except socket.timeout:
            return tf

    tf.flush() # Flush the write buffer to file.
    return tf

def print_file_stats (rf):
    metadata = os.stat(rf.name)
    print ("Recieved file \n (", rf.name, ")") # \n size: " + str(metadata.st_size) + " bytes.")

def print_file_contents (rf, PrintFile):
    buf = 10
    i = 0
    rf.seek(0)

    data = rf.read(buf)

    while (data):
        tmpstr = data.decode('utf-8')
        if PrintFile:
            print (tmpstr)
        i += len(tmpstr)
        data = rf.read(buf)

    print ("Total recieved: " +str(i) + " chars.")
    rf.close()



"""
String data recieved functions.
"""
def print_data_stats(rd):
    print ("Received {0} bytes of data.".format(sys.getsizeof(rd)))

def print_data_contents(rd):
    print (rd)



"""
Monitor the response from server for confirmation message.
"""
def monitor_server_response (cnct):
    while True:
        try:
            chunkStr = cnct.recv(1024)
            response = chunkStr.decode('utf-8')
            if re.search('file_prepared', response):
                return True
            else:
                print ("No valid response recieved from server")
                return False
        except socket.timeout:
            return False


