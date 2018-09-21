
#################################################################
# Course 			: CS-382 Network Centric Computing 			#
# Offering 			: Spring 2017								#
# University		: Lahore University of Management Sciences	#
# File name 		: server_v9.py                  			#
# Assignment title 	: Programming Assignment 1					#
# Author 			: Muhammad Zain Qasmi && Hassaan Hassaan 	#
# Roll No. 			: 18100276 && 18100059						#
# Submission 		: February 15th, 2017						#
# Instructor 		: Fareed Zaffar								#
# Python Version 	: 2.7										#
#################################################################


#==============================================================================



import socket
import os 
import time
import sys

from thread import *




# host = ''  #'localhost' or '127.0.0.1' or '' are all same
# port = 52000 #Use port > 1024, below it all are reserved
 
#Creating socket object
# serversock = socket()
# #Binding socket to a address. bind() takes tuple of host and port.
# serversock.bind((host, port))
# #Listening at the address
# serversock.listen(5) #5 denotes the number of clients can queue

host = '127.0.0.1'
#port = 5030
#print "here", sys.argv[1]
port = int(sys.argv[1])
serversock = socket.socket()
serversock.bind((host, port))
serversock.listen(5)

print "#################################################################"
print "#								#"
print "#                Welcome to CS 382 Search Engine Server		#"
print "#								#"	
print "#################################################################"



print "Waiting for Connection..."

def clientthread(clientsocket):
	# host = '127.0.0.1'
	# #port = 5030
	# #print "here", sys.argv[1]
	# port = int(sys.argv[1])
	# serversock = socket.socket()
	# serversock.bind((host, port))
	# serversock.listen(1)
	# print "Waiting for Connection..."
	# clientsocket, addr = serversock.accept()
	# print "Connection from: " + str(addr)
	print "START THREAD"
	currenDir = os.getcwd()
	path = os.getcwd() 
	while True:
		print "Inside Thread Loop"
		# currenDir = os.getcwd() # CRITICAL. REMOVE AND SEARCH ENGINE GOES IN FLAMES
		data2 = ""
		# path = os.getcwd() 

		identifiersize = clientsocket.recv(16)
		# if not identifiersize:
		# 	break
		identifiersize = int(identifiersize, 2)
		identifierName = clientsocket.recv(identifiersize)

		while True:
			if identifierName == "----1----":
				print "Option 1", identifierName

				while True:
					mSize = clientsocket.recv(16)
					# print "here", mSize
					mSize = int(mSize, 2)
					data = clientsocket.recv(mSize)

					if data == "----2----":
						identifierName = "----2----"
						break

					if data == "----3----":
						identifierName = "----3----"
						break

					if not data:
						break
					print "from connected user: " + str(data)
					
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
									fSize = len(f.name)
									fSize = bin(fSize)[2:].zfill(16) 
									clientsocket.send(fSize)
									clientsocket.send(f.name)

								file_contents = f.read()
								if data in file_contents:
									with open(files) as myFile:
										for num, line in enumerate(myFile, 1):
											if data in line:
												data2 = data2 + " " + str(num) # make this a list				
										data1 = "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory
										# print directory
										data2 = ""
										# clientsocket.send(data1)
										dSize = len(data1)
										dSize = bin(dSize)[2:].zfill(16) 
										clientsocket.send(dSize)
										clientsocket.send(data1)

										time.sleep(0.001)
										f.close()
								else:
									f.close()
					# clientsocket.send("End of Results!!!")
					endStr = "End of Results!!!"
					eSize = len(endStr)
					eSize = bin(eSize)[2:].zfill(16) #
					clientsocket.send(eSize)
					clientsocket.send(endStr)


			if identifierName == "----2----":
				print "Option 2", identifierName

				while True:

				    size = clientsocket.recv(16) 
				    if not size:
				        break
				    size = int(size, 2)
				    filename = clientsocket.recv(size)

				    if filename == "----1----":
				    	identifierName = "----1----"
				    	break

				    if filename == "----3----":
				    	identifierName = "----3----"
				    	break

				    totalReceived = str.split(filename)

				    filename = totalReceived[0]
				    filePath = totalReceived[1]

				    filename = os.path.join(filePath,filename)
				    if not os.path.isfile(filename):
				    	fSize = len("File does not exist")
				    	fSize = bin(fSize)[2:].zfill(32) 
				    	clientsocket.send(fSize)
				    	clientsocket.send("File does not exist")
				    	print "ERROR: FILE DOES NOT EXIST"
				    	continue
				
				    filesize = os.path.getsize(filename)
				    filesize = bin(filesize)[2:].zfill(32)
				    clientsocket.send(filesize)

				    file_to_send = open(filename, 'rb')

				    l = file_to_send.read()
				    clientsocket.sendall(l)
				    file_to_send.close()
				    print 'File Sent'

			if identifierName == "----3----":
				print "Option 3", identifierName
				clientsocket.close()
				print "Client Socket Closed Gracefully"
				return


# def Main():
while True:
	clientsocket, addr = serversock.accept()
	print "Connection from: " + str(addr)
	start_new_thread(clientthread,(clientsocket,)) 
 
clientsocket.close()
serversock.close()

# if __name__ == '__main__':
# 	Main()