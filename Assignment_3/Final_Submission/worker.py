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
def respondPing():
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
    # client_port = query[:5]
    # data = query[5:]
    data = query
    # print "data::", data
    # print "from connected user: " + str(data)
    data2 = " "
    counter = 0
    for directory, dirnames, filenames in os.walk(currenDir):
        os.chdir(directory)
        folder = os.getcwd()
        files_ = os.listdir(folder)
        for files in sorted(files_):
            counter +=1
            if kill_them_all == True and client_port == dead_client:
                print 'killing it'
                return
                break
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
                        data1 = "__RESPONSE__" + client_port + data + ' ' + "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory + '\n' #+ line
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
    endStr = "__RESPONSE__" + client_port + "__END_RESULTS__"
    s.sendto(endStr, (host, port))
    return jobStatus

kill_them_all = False
dead_client = '00000'
def terminate_search():
    kill_them_all = True
    job_done = 2


while(1) :
    try :
        # print 'JOB STATUS:: ', job_done
        d = s.recvfrom(1024*10)
        reply = d[0]
        addr = d[1]

        print "reply :: ", reply

        if reply == '__ping__':
            respondPing()

        elif reply.startswith('__TERMINATE__'):
            dead_client = reply[13:]
            terminate_search()


        # elif reply.startswith('__QUERY__'):
        #     job_done = 0
        #     query = reply[9:]
        #     print "query:: ", query
        #     job_done = search(query)

        # reply ::  __QUERY__43986_00000_00100_Pakistan
        # query::  43986_00000_00100_Pakistan

        elif reply.startswith('__QUERY__'):
            kill_them_all = False
            reply = reply[9:]
            # print 'slice :: ', reply
            client_port = reply[:5]
            # print 'cp    :: ', client_port
            reply = reply[6:]
            start_range = int(reply[:5])
            # print 'start :: ', start_range
            reply = reply[6:]
            end_range = int(reply[:5])
            # print 'end   :: ', end_range
            query = reply[6:]
            # print 'query :: ', query
            job_done = search(query, client_port, start_range, end_range)

        else:
            print 'Server reply : ' + reply
     
    except socket.error, e:
        if e.args[0] == errno.EWOULDBLOCK: 
            time.sleep(0)
        else:
            print e
            break
