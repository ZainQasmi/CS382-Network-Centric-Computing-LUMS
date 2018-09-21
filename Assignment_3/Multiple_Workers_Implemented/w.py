import socket 
import sys 
import errno
import time
import threading
import os
 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.bind(('127.0.0.1', 5000))
    s.setblocking(0)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;

msg = '__worker1__'
s.sendto(msg, (host, port))

job_done = 2 # 
reply = ''

def respondPing():
    threading.Timer(1, respondPing).start()
    if reply == '__ping__':
        if job_done == 0:
            msg = 'NOT_DONE'
            s.sendto(msg, (host, port))
        elif job_done == 1:
            msg = 'DONE_NOT_FOUND'
            s.sendto(msg, (host, port))
        elif job_done == 2:
            msg = 'DONE_FOUND'
            s.sendto(msg, (host, port))


currenDir = os.getcwd() + '/bbcsport'
def search(query,client_port, start_range, end_range):
    jobStatus = 1

    path = os.getcwd()
    time.sleep(5)
    # client_port = query[:5]
    # data = query[5:]
    data = query
    print "data::", data
    print "from connected user: " + str(data)
    data2 = " "
    counter = 0
    for directory, dirnames, filenames in os.walk(currenDir):
        os.chdir(directory)
        folder = os.getcwd()
        files_ = os.listdir(folder)
        for files in sorted(files_):
            counter +=1

            if counter >= start_range and counter <= end_range:
                # print "counter: ", counter
                continue


            if os.path.isfile(files):
                f = open (files, 'r')
                if (f.name + " " == data):
                    print "hey"
                file_contents = f.read()
                if data in file_contents:
                    jobStatus = 2
                    with open(files) as myFile:
                        for num, line in enumerate(myFile, 1):
                            if data in line:
                                data2 = data2 + " " + str(num) # make this a list               
                        # data1 = "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory
                        data1 = "__RESPONSE__" + client_port + "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory
                        data2 = ""
                        # print data1
                        # print data
                        # print 'doing job...'
                        time.sleep(0.001)
                        s.sendto(data1, (host, port))
                        # print 'job done!'
                        time.sleep(0.001)
                        f.close()
                else:
                    # jobStatus = 1
                    f.close()
    # print "counter:: ", counter
    print "jobstatus:: ", jobStatus
    endStr = "__RESPONSE__" + client_port + "__END_RESULTS__"
    s.sendto(endStr, (host, port))
    return jobStatus

listener = threading.Thread(target=respondPing)
listener.start()

while(1) :
    try :
        # print 'JOB STATUS:: ', job_done
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        print "Server reply :: ", reply

        # if reply == '__ping__':
            # respondPing()

        # elif reply.startswith('__QUERY__'):
        #     job_done = 0
        #     query = reply[9:]
        #     print "query:: ", query
        #     job_done = search(query)

        # reply ::  __QUERY__43986_00000_00100_Pakistan
        # query::  43986_00000_00100_Pakistan

        # elif reply.startswith('__QUERY__'):
        if reply.startswith('__QUERY__'):
            query_full = reply
            query_full = query_full[9:]
            print 'slice :: ', query_full
            client_port = query_full[:5]
            print 'cp    :: ', client_port
            query_full = query_full[6:]
            start_range = int(query_full[:5])
            print 'start :: ', start_range
            query_full = query_full[6:]
            end_range = int(query_full[:5])
            print 'end   :: ', end_range
            query = query_full[6:]
            print 'query :: ', query
            job_done = search(query, client_port, start_range, end_range)

        else:
            pass
            # print 'Server reply : ' + reply
     
    except socket.error, e:
        if e.args[0] == errno.EWOULDBLOCK: 
            time.sleep(0)
        else:
            print e
            break
