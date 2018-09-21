'''
    udp socket client
    Silver Moon

    for testing
    ncat localhost 8888 -u -v
'''
 
import socket   #for sockets
import sys  #for exit
import time
import threading
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    if ping_counter[0] > 3:
    	print "Server Not Responding...SHUTTING DOWN"
    	# s.exit()

query = ''

def query():
	query = raw_input('Enter message to send : ')

pingit()
 
while(1) :
    # msg = raw_input('Enter message to send : ')
    msg = 'China'
    # msg = 'Chinaafjewiweigowjeifj'
     
    try :
        #Set the whole string
        msg = '__SEARCH__' + msg
        s.sendto(msg, (host, port))
         
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]
         
        print 'Server reply : ' + reply

        if reply == '___I_IZ_ALAIVE__':
        	ping_counter[0] = 0



     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()