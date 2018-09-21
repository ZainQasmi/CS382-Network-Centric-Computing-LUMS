import socket
import sys 
import time
import threading
import errno
 
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
    msg = '__REQUESTER_PING__'
    s.sendto(msg, (host, port))
    ping_counter[0] += 1
    print ping_counter
    if ping_counter[0] > 4:
    	print "Server Not Responding...SHUTTING DOWN"
    	# s.exit()

pingit()

msg = ''
def queryFun():
    msg = raw_input("Please enter your query-> ")
    msg = '__SEARCH__' + msg
    s.sendto(msg, (host, port))


listener = threading.Thread(target=queryFun)
listener.start()
 
while(1) :
    # msg = raw_input('Enter message to send : ')
    try :
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]
        print 'Server reply : ' + reply

        if reply == '___I_IZ_ALAIVE__':
        	ping_counter[0] = 0
        else:
            if reply == '__END_RESULTS__':
                listener = threading.Thread(target=queryFun)
                listener.start()
                # print "LOLOLOL"
            else:
                print "ELSE: ", reply

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