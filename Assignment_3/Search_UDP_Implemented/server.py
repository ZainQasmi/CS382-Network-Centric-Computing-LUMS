'''
    Simple udp socket server
'''
 
import socket
import sys
import time
import errno
import threading



 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
    s.setblocking(0)
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

def pingit():
    threading.Timer(3.0, pingit).start()
    # print "AL :: ", activeWorkerList
    myiter = 0
    for oneWorker in workerList:
        activeWorkerList[myiter] += 1
        s.sendto('__ping__', oneWorker[1])
        myiter += 1

    for i in range(0, len(activeWorkerList)):
        if activeWorkerList[i] > 3:
            del activeWorkerList[i]
            del workerList[i]
            print "worker " ,i , " removed"


    # print "Hello, World!"

def workerPingResponse(ping_data, workerID):
    # print "ID:: ", workerID[1]
    myiter = 0
    for oneWorker in workerList:
        if oneWorker[1] == workerID:
            activeWorkerList[myiter] = 0
            if ping_data == 'NOT_DONE':
                # pass
                print ping_data
            elif ping_data == 'DONE_NOT_FOUND':
                # pass
                print ping_data
            elif ping_data == 'DONE_FOUND':
                # pass
                print ping_data
        myiter += 1


workerList = []
activeWorkerList = []
clientList = []
queryClientList = []
#now keep talking with the client

pingit()
reply = ''

while 1:
    # receive data from client (data, addr)
    try:
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        # print 'data\t::\t', d[0]
        # print 'addr (port) \t::\t', d[1][1]

        if data == '__worker1__':
            # print 'IM HERE 5'
            if d not in workerList:
                workerList.append(d)
                activeWorkerList.append(0)
                print 'w_len :: ', len(workerList)
                # s.sendto('__QUERY__Pakistan', addr)

        elif data == '__client__':
            # print 'IM HERE 4'
            if d not in clientList:
                clientList.append(d)
                print "c_len :: ", len(clientList)

        elif data == 'NOT_DONE' or data == 'DONE_NOT_FOUND' or data == 'DONE_FOUND':
            # print 'IM HERE 3'
            workerPingResponse(data, addr)

        elif data == '__REQUESTER_PING__':
            # print 'IM HERE 2'
            reply = '___I_IZ_ALAIVE__'
            s.sendto(reply, addr)

        elif data.startswith('__SEARCH__'):
            print "HERE"
            query = '__QUERY__' + str(d[1][1]) + data[10:]
            s.sendto(query, workerList[0][1])

        elif data.startswith('__RESPONSE__'):
            client_port = data[12:]
            client_port = client_port[:5]
            for oneClient in clientList:
                if str(oneClient[1][1]) == str(client_port):
                    s.sendto(data[17:], oneClient[1])
            # print ans


        else:
            print 'IM HERE 1'
            if not data: 
                break
             
            reply = 'OK...' + data
             
            s.sendto(reply , addr)
            
            # for oneWorker in workerList:
                # s.sendto(reply, oneWorker[1])

            # print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()


    except socket.error, e:
        if e.args[0] == errno.EWOULDBLOCK: 
            # print 'Wating for data'
            time.sleep(0)
        else:
            print e
            break
     
s.close()

