import time
import tempfile
import os
import re
import socket
import sys



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
                    # TIMETAKE - sending file.
                    # with Utils.Timer() as t:
                       # Utils.send_stream_TCP(sReq, txInterval, txPackets, segmentSize)
                    # print('Sending took %.03f sec.' % t.interval)

"""
Print startup message.

parameters:
    HOST: string. The server domainname to connect to.
    PORT: int. The portnumber on server to connect to.

return:
    void.
"""
def print_startup_msg(HOST, PORT):
    try:
        remote_ip = socket.gethostbyname( HOST )
    except socket.gaierror:
        #could not resolve
        remote_ip = False
        print ('Hostname could not be resolved to an address.')

    if remote_ip:
        print ("Trying to connect to server: ", HOST, " (" + remote_ip + ") on port: ", PORT, "...wait.")
    else:
        print ("Trying to connect to server: ", HOST, " on port: ", PORT, "...wait.")



"""
Prompt select a host and port connect to.

If no or invalid integer is entered at the prompt the default host at index 0 is selected.

parameters:
    none

return:
    host: string.
    port: integer.
"""
def prompt_select_host():
    print("Choose server please:")
    fh = open( "hosts.txt" );

    listHosts = []
    for line in fh.readlines():
        y = [value for value in line.split()]
        listHosts.append( y )

    fh.close()

    for index, item in enumerate(listHosts):
        print (index, item)

    prompt = input('SERVER: ')

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
Prompt user for stream specs
parameters:
    none

return:
    interval.
    segments.
    segmentSize.
"""
def prompt_stream():
    print("Switched to stream mode.")
    interval = input('\nPlease input the segment TX interval (miliseconds) required: ')
    segments = input('\nPlease input the number of segments required: ')
    segmentSize = input('\nPlease input the size of each segment (Bytes): ')
    try:
        float(interval)
    except:
        interval = 10
    try:
        int(segments)
    except:
        segments = 1000
    try:
        int(segmentSize)
    except:
        segmentSize = 1024

    return float(interval), int(segments), int(segmentSize)



"""
Output to console data recieved per second.
parameters:
    interval: int.
    typedInteger: float. The size of requested data in Bytes.

return:
    void.
"""
def print_transferRate(interval, typedInteger, rxFileLength):
    print ('Recieving file took %.03f sec.' % interval)
    bytesPerSec = False
    kBytesPerSec = False
    mBytesPerSec = False

    if typedInteger != rxFileLength:
        typedInteger = rxFileLength

    if interval > 0:
        bytesPerSec = typedInteger / interval
        # Format the transfer rate to be human readable.
        if bytesPerSec > 2000:
            kBytesPerSec = bytesPerSec / 1000
            bytesPerSec = False
            if kBytesPerSec > 2000:
                mBytesPerSec = kBytesPerSec / 1000
                kBytesPerSec = False
    if bytesPerSec:
        print("B/s: " + str(bytesPerSec))
    elif kBytesPerSec:
        print("kB/s: " + str(kBytesPerSec))
    elif mBytesPerSec:
        print("MB/s: " + str(mBytesPerSec))
    else:
        print("No transfer rate data.")



"""
Output to console file stats.
parameters:
    rf: the recieved file.
    ti: int, the typed typedInteger value from user.

return:
    rfFileLength: int, the length of all the recieved data.
"""
def print_file_stats (rf, ti):
    rf.seek(0)
    rfFileData = rf.read()
    rfFileLength = len(rfFileData)

    loss = ti - rfFileLength

    if loss > 0:
        percentageLoss = 100 * (loss / ti)
        print ("Loss detected: " + str(loss) + " chars missing from file. (%.02f percent loss)" % percentageLoss)
    elif loss == 0:
        print ("Recieved complete file (" + str(rfFileLength) + " chars). Saved as: \n (", rf.name, ")")

    return rfFileLength



"""
Output to console stream stats.
parameters:
    segments: int, requested segment count.
    counter: int, recieved segment count.

return:
   void.
"""
def print_stream_stats (segments, counter):
    loss = segments - counter
    if loss > 0:
        percentageLoss = 100 * (loss / segments)
        print ("Recieved " + str(counter) + " of " + str(segments) + " segments. \n Loss: %.02f percent." % percentageLoss)
    else:
        print("Recieved all " + str(counter) + " segments.")



"""
Output to console file contents.
Depends on settings specified. Will either print contents, or only length of conents.
parameters:
    rf: the recieved file.
    PrintFile: the settings parameter.

return:
    void.
"""
def print_file_contents (rf, PrintFile):
    if PrintFile:
        buf = 1024

        rf.seek(0)
        data = rf.read(buf)

        while data:
            tmpstr = bytes.decode('utf-8')
            print (tmpstr)
            data = rf.read(buf)

        rf.close()



"""
Output to console recieved data.
parameters:
    rd: the recieved data.

return:
    void.
"""
def print_dataRecieved(rd):
    print ("Received {0} bytes of data.".format(sys.getsizeof(rd)))
    print (bytes.decode(rd, 'utf-8'))





"""
======== U D P =============
"""

"""
UDP Recieve data and write to named temporary file.
parameters:
    cnct: The connection.
    recvBuffSize: integer. Size of recieve buffer.

return:
    tf: temporaryfile instance.
"""
def recv_file_UDP(cnct, recvBuffSize):
    tf = tempfile.NamedTemporaryFile()

    while True:
        try:
            chunk = cnct.recv(recvBuffSize)
            tf.write(chunk)
        except socket.timeout:
            tf.flush() # Flush the write buffer to file.
            return tf



"""
Recieve data STREAM over UDP.
Count the iterations of the recv loop.
Also get the sequence number from the segment and check against previous segment.

parameters:
    cnct: The connection.
    recvBuffSize: integer. Size of recieve buffer.
    segments: integer. Number of segments requested.

return:
    counter: integer. Number of iterations of the loop.
"""
def recv_stream_UDP(cnct, recvBuffSize, segments, sequenceNumber):
    msg = b''
    counter = 0
    oldSequence = segments

    while True:
        try:
            chunk = cnct.recv(recvBuffSize)
        except socket.timeout:
            print("Socket timed out on recv_stream.")
            return counter

        if sequenceNumber:
            chunkStr = bytes.decode(chunk, 'utf-8')
            sequence = chunkStr.split("A", 1)

            try:
                sequence = int(sequence[0])
            except:
                sequence = False
                pass

            if sequence:
                if sequence == oldSequence:
                    oldSequence = oldSequence - 1
                else:
                    print("Detected missing segment: " + str(oldSequence - 1))
                    oldSequence = sequence

        counter = counter + 1



"""
Quit the client UDP.

parameters:
    cnct: The connection.

return:
    void
"""
def quit_now_UDP ():
    print ("Shutting down client...")
    sys.exit()






"""
======== T C P =============
"""

"""
TCP Recieve data and write to named temporary file.
parameters:
    cnct: The connection.
    recvBuffSize: integer. Size of recieve buffer.

return:
    tf: temporaryfile instance.
"""
def recv_file_TCP(cnct, recvBuffSize):
    tf = tempfile.NamedTemporaryFile()

    while True:
        chunk = cnct.recv(recvBuffSize)
        tf.write(chunk)

        if chunk == b'':
            tf.flush()
            return tf



"""
Recieve data STREAM over TCP and write to named temporary file.

parameters:
    cnct: The connection.
    recvBuffSize: integer. Size of recieve buffer.

return:
    msg: string. The recieved data.
    counter: integer. The number of iterations of the loop.
"""
def recv_stream_TCP(cnct, recvBuffSize):
    msg = b''
    counter = 0

    while True:
        chunk = cnct.recv(recvBuffSize)

        if chunk == b'':
           return msg, counter

        msg = msg + chunk
        counter = counter + 1



"""
Quit the client TCP.

parameters:
    cnct: The connection.

return:
    void
"""
def quit_now_TCP(cnct):
    cnct.close()
    print ("...disconnected.")
    print ("Shutting down client...")
    sys.exit()





"""
Decide what to do after a response from server.
parameters:
    cnct: The connection.

return:
    boolean.
"""
def monitor_server_response (cnct):
    print ("Please wait for the server to prepare your file.\n..........")
    while True:
        try:
            chunkStr = cnct.recv(1024)
            response = bytes.decode(chunkStr, 'utf-8')
            if re.search('file_prepared', response):
                print ("Server has prepared the file, recieving...")
                return True
            else:
                print (str(response))
                return False
        except socket.timeout:
            print ("Client timed out. Try increasing RcvTimeOut")
            return False