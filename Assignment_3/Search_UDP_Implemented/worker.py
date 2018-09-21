import socket   #for sockets
import sys  #for exit
import errno
import time
import threading
import os
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.bind(('127.0.0.1', 5000))
    # s.setblocking(0)
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


currenDir = os.getcwd()
def search(query):
    jobStatus = 1
    # currenDir = os.getcwd()
    path = os.getcwd()
    client_port = query[:5]
    data = query[5:]
    print "data::", data
    print "from connected user: " + str(data)
    data2 = " "
    for directory, dirnames, filenames in os.walk(currenDir):
        os.chdir(directory)
        folder = os.getcwd()
        # print "Current working dir : %s" % os.getcwd()
        files_ = os.listdir(folder)
        for files in sorted(files_):
            if os.path.isfile(files):
                f = open (files, 'r')
                if (f.name + " " == data):
                    print "hey"
                    # clientsocket.send(f.name)
                file_contents = f.read()
                if data in file_contents:
                    jobStatus = 2
                    with open(files) as myFile:
                        for num, line in enumerate(myFile, 1):
                            if data in line:
                                data2 = data2 + " " + str(num) # make this a list               
                        # data1 = "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory
                        data1 = "__RESPONSE__" + client_port + "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory
                        # print directory
                        data2 = ""
                        print data1
                        print data
                        print 'doing job...'
                        time.sleep(0.001)
                        s.sendto(data1, (host, port))
                        print 'job done!'

                        # clientsocket.send(data1)

                        time.sleep(0.001)
                        f.close()
                else:
                    # jobStatus = 1
                    f.close()
    # clientsocket.send("End of Results!!!")
    # endStr = "End of Results!!!"
    endStr = "__RESPONSE__" + client_port + "__END_RESULTS__"
    s.sendto(endStr, (host, port))
    return jobStatus


while(1) :
    # msg = raw_input('Enter message to send : ')
     
    try :
        print 'JOB STATUS:: ', job_done
        #Set the whole string
        # s.sendto(msg, (host, port))
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]

        if reply == '__ping__':
            respondPing()

        elif reply.startswith('__QUERY__'):
            job_done = 0
            query = reply[9:]
            print "query:: ", query
            job_done = search(query)
        else:
            print 'Server reply : ' + reply
     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
        # if msg.args[0] == errno.EWOULDBLOCK:
        #     time.sleep(0)
        # else:
        #     print msg
        #     break


