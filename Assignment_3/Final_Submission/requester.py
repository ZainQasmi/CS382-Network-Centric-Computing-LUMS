import socket
import sys 
import time
import threading
import errno
from termcolor import colored, cprint

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;

msg = '__client__'
s.sendto(msg, (host, port))

ping_counter = []
ping_counter.append(0)

def pingit():
    threading.Timer(3.0, pingit).start()
    pingStr = '__REQUESTER_PING__'
    s.sendto(pingStr, (host, port))
    ping_counter[0] += 1
    print ping_counter
    if ping_counter[0] > 3:
    	print "Server Not Responding...SHUTTING DOWN"
    	# s.close()
    	# s.shutdown(socket.SHUT_RDWR)
    	# quit()
    	# s.exit()

pingit()

msg = ''
def queryFun():
    myQuery = raw_input("Please enter your query-> ")
    myQuery = '__SEARCH__' + myQuery
    s.sendto(myQuery, (host, port))


listener = threading.Thread(target=queryFun)
listener.start()

class c:
    blue = '\033[94m'
    rust =  '\033[93m'
    red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'
    Default = '\033[99m'
 
while(1) :
    # msg = raw_input('Enter message to send : ')
    try :
        d = s.recvfrom(1024*10)
        reply = d[0]
        addr = d[1]
        # print 'Server reply : ' + reply

        # replyArray = reply.split('__')
        # msg = replyArray[0]

        if reply == '___I_IZ_ALAIVE__':
        	ping_counter[0] = 0
        else:
            if reply == '__END_RESULTS__':
                listener = threading.Thread(target=queryFun)
                listener.start()
                # print "LOLOLOL"
            else:

                myarray = reply.split()
                msg = myarray[0]

                for word in reply.split():
                	if word not in msg:
                		print c.Default+word,
                	else:
                		print c.red+word,

                print '\n'


                f = open('myfile.txt', 'a')
            	print >> f, reply
                # for i in range(0, 1000000):
            	# f.write(reply)
                # f.close() 
                

    except socket.error, e:
        if e.args[0] == errno.EWOULDBLOCK: 
            # print 'Wating for data(server)'
            time.sleep(0.001)
        else:
            print e
            continue

    # except socket.error, msg:
    #     print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    #     sys.exit()