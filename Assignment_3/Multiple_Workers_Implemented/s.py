import socket
import sys
import time
import errno
import threading
import os
 
HOST = ''   
PORT = 8888 
 
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
try:
    s.bind((HOST, PORT))
    s.setblocking(0)
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

def pingit():
    threading.Timer(5.0, pingit).start()
    myiter = 0
    
    for oneWorker in workerList:
        activeWorkerList[myiter] += 1
        s.sendto('__ping__', oneWorker[1])
        myiter += 1

    for i in range(0, len(activeWorkerList)):
        if activeWorkerList[i] > 5:
            del activeWorkerList[i]
            del workerList[i]
            print "worker " ,i , " removed"

def chkActiveClients():
	threading.Timer(5.0, chkActiveClients).start()
	myiter2 = 0
	for oneRequester in clientList:
		activeClientList[myiter2] += 1
		myiter2 +=1

	for i in range(0, len(activeClientList)):
		if activeClientList[i] > 5:
			del activeClientList[i]
			del clientList[i]
			print "requester ",i, " removed"





def workerPingResponse(ping_data, workerID):
    # print "ID:: ", workerID[1]
    myiter = 0
    for oneWorker in workerList:
        if oneWorker[1] == workerID:
            activeWorkerList[myiter] = 0
            if ping_data == 'NOT_DONE':
                workerStatus[myiter] = 0
                # pass
                print ping_data
            elif ping_data == 'DONE_NOT_FOUND':
                workerStatus[myiter] = 1
                # pass
                print ping_data
            elif ping_data == 'DONE_FOUND':
                workerStatus[myiter] = 2
                # pass
                print ping_data
        myiter += 1

def clientPingResponse(ping_data, clientID):
    myiter = 0
    for oneRequester in clientList:
        if oneRequester[1] == clientID:
            activeClientList[myiter] = 0
        myiter += 1
    s.sendto(reply, addr)


workerList = []
activeWorkerList = []
workerStatus = []
clientList = []
queryClientList = []
activeClientList = []

pingit()
chkActiveClients()
reply = ''

while 1:
    # receive data from client (data, addr)
    try:
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        # print 'data\t::\t', d[0]
        # print 'addr (port) \t::\t', addr[1]

        if data == '__worker1__':
            if d not in workerList:
                workerList.append(d)
                activeWorkerList.append(0)
                workerStatus.append(2)
                print 'w_len :: ', len(workerList)

        elif data == '__client__':
            if d not in clientList:
                clientList.append(d)
                activeClientList.append(0)
                print "c_len :: ", len(clientList)

        elif data == 'NOT_DONE' or data == 'DONE_NOT_FOUND' or data == 'DONE_FOUND':
            workerPingResponse(data, addr)

        elif data == '__REQUESTER_PING__':
            reply = '___I_IZ_ALAIVE__'
            clientPingResponse(reply,addr)
            # s.sendto(reply, addr)

        # elif data.startswith('__SEARCH__'):
        #     print "HERE"
        #     query = '__QUERY__' + str(d[1][1]) + data[10:]
        #     s.sendto(query, workerList[0][1])
        #     # sample: __QUERY__36465Pakistan

        elif data.startswith('__SEARCH__'):
            print "NEW JOB"
            
            # s.sendto(query, workerList[0][1])

            myPath = os.getcwd() + '/bbcsport'
            num_files = sum([len(files) for r, d, files in os.walk(myPath)])
            num_files += 5 #five folders
            # search_range = num_files / (len(workerStatus)**2)
            print "num files :: ", num_files
            files_done = 0
            one_chunk = 100


            while (files_done < num_files):
                myiter = 0
                query_start = files_done
                query_end = query_start+one_chunk
                if query_end > num_files:
                    query_end = num_files
                for oneWorker in workerList:
                    while len(str(query_start)) < 5:
                        # print "stuck 1"
                        query_start = '0' + str(query_start)
                    while len(str(query_end)) < 5:
                        # print "stuck 2"
                        query_end = '0' + str(query_end)
                	print 'workerStatus :: ', workerStatus
                    # print "query_start :: ", query_start
                    # print "query_end :: ", query_end
                    query = '__QUERY__' + str(addr[1]) + '_' + query_start + '_' + query_end + '_' + data[10:]
                    # query = '__QUERY__' + query_start + query_end + data[10:]
                    print "query :: ", query
                    # print "here 3"
                    if workerStatus[myiter] != 0:
                        # print "here 4"
                        # workerStatus[myiter] = 0
                        s.sendto(query, workerList[0][1])
                        # time.sleep(1)
                        files_done += one_chunk
                        myiter += 1
                    # print "query_start

        elif data.startswith('__RESPONSE__'):
            client_port = data[12:]
            client_port = client_port[:5]
            for oneClient in clientList:
                if str(oneClient[1][1]) == str(client_port):
                    s.sendto(data[17:], oneClient[1])

        else:
            print 'IM HERE 1'
            if not data: 
                break
            reply = 'OK...' + data
            s.sendto(reply , addr)

    except socket.error, e:
        if e.args[0] == errno.EWOULDBLOCK: 
            time.sleep(0)
        else:
            print e
            break
     
s.close()

