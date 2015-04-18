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
Select a host and port to bind to.

If no or invalid integer is entered at the prompt the default host at index 0 is selected.

parameters:
    none

return:
    host: string.
    port: integer.

"""
def select_host():
    print("Choose host and port to bind to please: ")
    fh = open( "hosts.txt" );

    listHosts = []
    for line in fh.readlines():
        y = [value for value in line.split()]
        listHosts.append( y )

    fh.close()

    for index, item in enumerate(listHosts):
        print (index, item)

    prompt = input('PROMPT: ')

    try:
        typedInteger = int(prompt)
    except:
        typedInteger = 0
        print ("Default server selected.")
        pass

    selectedHost = listHosts[typedInteger]
    print (selectedHost)
    for item in selectedHost:
        hostString = item.split(":", 1)

    return str(hostString[0]), int(hostString[1])



"""
Make a named temporary file and fill it with chars.

parameters:
    ri: The recieved integer from client.

return tf: temporaryfile instance.
"""
def make_tempFile(ri):
    tf = tempfile.NamedTemporaryFile()
    chunkStr = 'A'
    for x in range(0, ri):
        chunk = chunkStr.encode('utf-8')
        tf.write(chunk)

    tf.flush() # Flush the write buffer to file.
    return tf




"""
======== U D P =============
"""



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
Send a stream to client UDP.

parameters:
    sReq: the client request instance.
    txInterval: integer, the second delay between sending.
    txPakets: integer, the number of packets to send.
    data: bytes object, the data to include in each packet.

return void
"""
def send_stream_UDP(sReq, txInterval, txPakets, data):
    while txPakets > 1:
        time.sleep(txInterval)
        sReq.sendto(data)
        txPakets = txPakets - 1



"""
Send file to connected client UDP.

parameters:
    sReq: the client request instance.
    client_address: the remote address of the client making the request.
    tempFile: the temporary file instance.

return boolean
"""
def send_tempFile_UDP(sReq, client_address, tempFile):
    # Read the information from the file.
    tempFile.seek(0)
    buf = 1024
    fileData = tempFile.read(buf)

    while (fileData):
        if(sReq.sendto(fileData, client_address)):
            fileData = tempFile.read(buf)

    tempFile.close()



"""
======== T C P =============
"""



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
Send a stream to connected client TCP.

parameters:
    sReq: the client request instance.
    txInterval: integer, the second delay between sending.
    txPakets: integer, the number of packets to send.
    data: bytes object, the data to include in each packet.

return:
    void
"""
def send_stream_TCP(sReq, txInterval, txPakets, data):
    while txPakets > 1:
        time.sleep(txInterval)
        sReq.send(data)
        txPakets = txPakets - 1



"""
Send a file to connected client TCP.

parameters:
    sReq: the client request instance.
    tempFile: the temporary file instance.

return:
    boolean
"""
def send_tempFile_TCP(sReq, tempFile):
    # Read the information from the file.
    tempFile.seek(0)
    buf = 1024
    toSend =b''
    fileData = tempFile.read(buf)
    while (fileData):
        toSend = toSend + fileData
        fileData = tempFile.read(buf)

    tempFile.close()
    sReq.sendall(toSend)



"""
======== F E E D B A C K =============
"""



"""
Make a file prepared confirmation.

parameters:
    tempFile: the temp file instance.

return encoded confirmation message.
"""
def make_confirmationReport(tempFile):
    metadata = os.stat(tempFile.name)
    print ("\nSending file \n (", tempFile.name, ") \n size: " + str(metadata.st_size) + " bytes.")

    return str.encode('file_prepared', 'utf-8')



"""
Make a fault report for FILE request.

parameters:
    FileLimit: global value limiting the temporary file size.
    recievedInteger: the integer recieved from client.

return encoded string.
"""
def make_faultReportFile(FileLimit, recievedInteger):
    feedback = "Request for file of " + str(recievedInteger) + " chars. Server limit is: " + str(FileLimit) + " chars."
    print (feedback)
    return str.encode(feedback, 'utf-8')



"""
Make a fault report for STREAM request.

parameters:
    FileLimit: global value limiting the temporary file size.
    recievedInteger: the integer recieved from client.

return encoded string.
"""
def make_faultReportStream(txInterval, txPakets):
    feedback = "Request for transfer of " + str(txPakets) + " pakets at: " + str(txInterval) + " has errors."
    print (feedback)
    return str.encode(feedback, 'utf-8')



"""
Make an echo report.
This function will take the recieved string, transform it to uppercase and return to client.

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