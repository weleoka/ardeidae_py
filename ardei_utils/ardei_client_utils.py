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
                       # Utils.send_stream_TCP(sReq, txInterval, txPackets, packetSize)
                    # print('Sending took %.03f sec.' % t.interval)


"""
Select a host and port connect to.

If no or invalid integer is entered at the prompt the default host at index 0 is selected.

parameters:
    none

return:
    host: string.
    port: integer.

"""
def select_host():
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
    packets.
    packetSize.
"""
def prompt_stream():
    interval = input('\nPlease input the paket TX interval (miliseconds) required: ')
    packets = input('\nPlease input the number of packets required: ')
    packetSize = input('\nPlease input the size of each packet (Bytes): ')
    return int(interval), int(packets), int(packetSize)



"""
Output to console data recieved per second.
parameters:
    interval: int.
    typedInteger: float. The size of requested data in Bytes.

return:
    void.
"""
def print_transferRate(interval, typedInteger):
    print ('Recieving file took %.03f sec.' % interval)
    bytesPerSec = False
    kBytesPerSec = False
    mBytesPerSec = False
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
    void.
"""
def print_file_stats (rf, ti):
    rf.seek(0)
    rfFileData = rf.read()
    rfFileLength = len(rfFileData)

    loss = ti - rfFileLength

    if loss > 0:
        percentageLoss = 100 * (loss / ti)
        print ("Loss detected: " + str(loss) + " chars missing from file. ( %.02f percent loss)" % percentageLoss)
    elif loss == 0:
        print ("Recieved complete file (" + str(rfFileLength) + " chars). Saved as: \n (", rf.name, ")")



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
            tmpstr = data.decode('utf-8')
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
    print (str(rd.decode('utf-8')))





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
Also get the sequence number from the packet and check against previous packet.

parameters:
    cnct: The connection.
    recvBuffSize: integer. Size of recieve buffer.
    packets: integer. Number of packets requested.

return:
    counter: integer. Number of iterations of the loop.
"""
def recv_stream_UDP(cnct, recvBuffSize, packets):
    msg = b''
    counter = 0
    oldSequence = packets

    while True:
        try:
            chunk = cnct.recv(recvBuffSize)
        except socket.timeout:
            print("Socket timed out on recv_stream.")
            return counter

        chunkStr = chunk.decode('utf-8')
        sequence = chunkStr.split("A", 1)

        if int(sequence[0]) == oldSequence:
            oldSequence = oldSequence - 1
        else:
            print("Detected missing packet: " + int(oldSequence - 1))
            oldSequence = sequence[0]

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
        chunk = cnct.recv(recvBuffSize)#MSGLEN-len(msg))
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