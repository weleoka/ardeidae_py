import time
import tempfile
import datetime
import os
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
Select a host and port to bind to.

If no or invalid integer is entered at the prompt the default host at index 0 is selected.

parameters:
    none

return:
    host: string.
    port: integer.

"""
def prompt_select_host():
    print("Choose host-port to bind to please: ")
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
        print ("Default host-port selected.")
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

return:
    tf: temporaryfile instance.
"""
def make_tempFile(ri):
    tf = tempfile.NamedTemporaryFile()
    arr = []
    chunkStr = 'A'


    while True:
        if len(arr) >= ri:
            break
        else:
            arr.append(chunkStr)

    string = ''.join(arr) # Turn the list of individual chars into string.

    tf.write(string.encode('utf-8'))
    tf.flush() # Flush the write buffer to file.

    return tf



"""
Make an incremented string of certain bytes(chars)

parameters:
    code: integer. The sequence number of the segment.
    size: integer. Size/length of segment requested by client.

return:
    str: string. The encoded string
"""
def make_segment(code, size):
    arr = []
    chunkStr = 'A'
    code = list(str(code)) # Turn the code integer into a string into a list.

    for char in code:
        arr.append(char)

    while True:
        if len(arr) >= size:
            break
        else:
            arr.append(chunkStr)

    string = ''.join(arr) # Turn the list of individual chars into string.

    return string.encode('utf-8')



"""
Read from file.

parameters:
    tf: tempFile instance.

return:
    fileData: bytes object of entire file.
"""
def readData_tempFile(tf):
    tf.seek(0)
    fileData = tf.read()
    tf.close()

    return fileData



"""
======== U D P =============
"""


"""
Send a stream to client UDP.

parameters:
    sReq: the client request instance.
    txInterval: integer, the second delay between sending.
    txPackets: integer, the number of segments to send.
    data: bytes object, the data to include in each segment.

return:
    void
"""
def send_stream_UDP(sReq, client_address, txInterval, txPackets, segmentSize):
    while txPackets > 0:
        time.sleep(txInterval)
        segment = make_segment(txPackets, segmentSize)
        sReq.sendto(segment, client_address)
        txPackets = txPackets - 1
    return



"""
Send file to connected client UDP.

parameters:
    sReq: the client request instance.
    client_address: the remote address of the client making the request.
    txUnitSize: bytes, the amount of data in each UDP segment.
    tempFile: the temporary file instance.

return:
    void
"""
def send_file_UDP(sReq, client_address, txUnitSize, tempFile):
    tempFile.seek(0)

    fileData = tempFile.read(txUnitSize)
    while (fileData):
        sReq.sendto(fileData, client_address)
        fileData = tempFile.read(txUnitSize)

    tempFile.close()
    return




"""
======== T C P =============
"""


"""
Send a stream to connected client TCP.

parameters:
    sReq: the client request instance.
    txInterval: integer, the second delay between sending.
    txPackets: integer, the number of segments to send.
    data: bytes object, the data to include in each segment.

return:
    void
"""
def send_stream_TCP(sReq, txInterval, txPackets, segmentSize):
    while txPackets > 0:
        time.sleep(txInterval)
        segment = make_segment(txPackets, segmentSize)
        sReq.send(segment)
        txPackets = txPackets - 1
    return



"""
Send a file to connected client TCP.

parameters:
    sReq: the client request instance.
    tempFile: the temporary file instance.

return:
    void
"""
def send_file_TCP(sReq, tempFile):
    tempFile.seek(0)
    fileData = tempFile.read()
    tempFile.close()

    sReq.sendall(fileData)




"""
======== F E E D B A C K =============
"""

"""
Make a file prepared confirmation.

parameters:
    tempFile: the temp file instance.

return:
    string, encoded confirmation message.
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

return:
    encoded string.
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

return:
    encoded string.
"""
def make_faultReportStream(txInterval, txPackets, segmentSize):
    feedback = "Request for transfer of " + str(txPackets) + " segments at interval: " + str(txInterval) + ", of size: " + str(segmentSize) + " has errors."
    print (feedback)
    return str.encode(feedback, 'utf-8')



"""
Make an echo report.
This function will take the recieved string, transform it to uppercase and return to client.

parameters:
    date: the recieved data.
    client_address: the address from which the data was recieved.

return:
    uppercase string.
"""
def make_echoReport(data, client_address):
    timestamp = datetime.datetime.now().strftime("%I:%M%p")
    print ("\n", timestamp, "{} wrote: ".format(client_address))
    print (data.decode('utf-8'))
    return data.upper()



"""
Print out server welcome screen.

parameters:
    port: The assigned port number.

return:
    void
"""
def print_startup_msg(port):
    print ("Server host name: ", socket.gethostname(), " on ", socket.gethostbyname(socket.gethostname()), " port: ", port)
    print ("fully qualified domain name: ", socket.getfqdn())
    print ("details: ", socket.gethostbyaddr(socket.gethostbyname(socket.gethostname())))



"""
Print an empty report.

parameters:
    none

return:
    void
"""
def print_emptyReport():
    print ("Recieved client request of absolutely nothing.")



"""
Print jobDone report.

parameters:
    client_address

return:
    void
"""
def print_jobDoneReport(client_address):
    print ("Server completed request from ", client_address)