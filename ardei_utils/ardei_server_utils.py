import time
import tempfile
import datetime
import os
import socket
"""
Here are some functions reqired for the ardeidae_py servers to run.
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
Print out the UDP server welcome screen.
parameters:
    port: The assigned port number.

return void
"""
def print_startup_msg_UDP(port):
    print (" ")
    print("Started ardeidae_py UDP Server... waiting for clients.")
    print ("Server running on host: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", port)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))



"""
Print out the TCP server welcome screen.
parameters:
    port: The assigned port number.

return void
"""
def print_startup_msg_TCP(port):
    print (" ")
    print("Started TCP Server... waiting for clients.")
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", port)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))



"""
Make a named temporary file and fill it with chars.
parameters:
    ri: The recieved integer from client.

return temporaryfile instance.
"""
def make_file(ri):
    tf = tempfile.NamedTemporaryFile()
    chunkStr = 'A'
    for x in range(0, ri):
        chunk = chunkStr.encode('utf-8')
        tf.write(chunk)

    tf.flush() # Flush the write buffer to file.
    return tf



"""
Make a fault report.
parameters:
    FileLimit: global value limiting the temporary file size.
    recievedInteger: the integer recieved from client.

return encoded string.
"""
def make_faultReport(FileLimit, recievedInteger):
    feedback = "Request for file of " + str(recievedInteger) + " chars. Server limit is: " + str(FileLimit) + " chars."
    print (feedback)
    return str.encode(feedback, 'utf-8')



"""
Make an echo report.
Transform the recieved string to upper case.
parameters:
    date: the recieved data.
    client_address: the address from which the data was recieved.

return uppercase string.
"""
def make_echoReport(data, client_address):
    timestamp = datetime.datetime.now().strftime("%I:%M%p")
    print ("\n", timestamp, "{} wrote: ".format(client_address))
    print (data)
    return data.upper()



"""
Make a file prepared confirmation.

parameters:
    tempFile: the temp file instance.

return encoded confirmation message.
"""
def make_confirmation(tempFile):
    metadata = os.stat(tempFile.name)
    print ("\nSending a file \n (", tempFile.name, ") \n size: " + str(metadata.st_size) + " bytes.")

    return str.encode('file_prepared', 'utf-8')



"""
Make an empty report.

parameters:
    none

return void
"""
def print_emptyReport():
    print ("Recieved client request of absolutely nothing.")



"""
Make jobDone report.

parameters:
    client_address

return void
"""
def print_jobDoneReport(client_address):
    print ("Server completed request from ", client_address)