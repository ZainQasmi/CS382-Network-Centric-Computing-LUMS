#################################################################
# Course 			: CS-382 Network Centric Computing 			#
# Offering 			: Spring 2017								#
# University		: Lahore University of Management Sciences	#
# File name 		: client_v9.py                  			#
# Assignment title 	: Programming Assignment 1					#
# Author 			: Muhammad Zain Qasmi && Hassaan Hassaan 	#
# Roll No. 			: 18100276 && 18100059						#
# Submission 		: Februaru 15th, 2017						#
# Instructor 		: Fareed Zaffar								#
# Python Version 	: 2.7										#
#################################################################


#==============================================================================

import socket
import sys

def Main():
	#host = '127.0.0.1'
	#port = 5030
	host = sys.argv[1]
	port = int(sys.argv[2])
	s = socket.socket()
	s.connect((host, port))

	overkill = 0; #the breaker of loops, terminator of programs

	print "#################################################################"
	print "#								#"
	print "#                Welcome to CS 382 Search Engine Client		#"
	print "#								#"	
	print "#################################################################"

	while True:

		print "================================================================="
		print 'Press 1 to search something'
		print 'Press 2 to download a file'
		print 'Press 3 to exit search engine'
		print "================================================================="

		option = raw_input("-> ")

		if option == "1":

			identifierName = "----1----"
			identifiersize = len(identifierName)
			identifiersize = bin(identifiersize)[2:].zfill(16) 
			s.send(identifiersize)
			s.send(identifierName)

			print 'Please enter your search query'
			
			message = raw_input("-> ")
			mSize = len(message)
			mSize = bin(mSize)[2:].zfill(16) 
			s.send(mSize)
			s.send(message)

			while message != 'quit':

				mSize = s.recv(16)
				mSize = int(mSize, 2)
				data = s.recv(mSize)

				print str(data)
				if (data == "End of Results!!!"):
					print 'Please enter a new query or enter quit to exit the search engine'

					message = raw_input("-> ")
					if message == "quit":
						print "here"
						break
					message = message + " "
					mSize = len(message)
					mSize = bin(mSize)[2:].zfill(16) 
					s.send(mSize)
					s.send(message)
			
			# s.close()

		elif option == "2":

			identifierName = "----2----"
			identifiersize = len(identifierName)
			identifiersize = bin(identifiersize)[2:].zfill(16) 
			s.send(identifiersize)
			s.send(identifierName)


			while True:
			    
			    filename = raw_input("Enter Filename + Path seperated by space or 'quit' to exit:\n-> ")

			    if filename[:4] == "quit":
			    	break

			    while not " " in filename and filename != "quit":
			    	filename = raw_input("String must be seperated by SPACE:\n-> ")

			    if filename == "quit":
			    	break
			    	

			    size = len(filename)
			    size = bin(size)[2:].zfill(16) 
			    s.send(size)
			    s.send(filename)

			    totalSent = str.split(filename)
			    filename = totalSent[0]
			    filePath = totalSent[1]
			    
			    filesize = s.recv(32)
			    filesize = int(filesize, 2)
			    file_to_write = open(filename, 'wb')
			    chunksize = 4096
			    
			    while filesize > 0:
			        if filesize < chunksize:
			            chunksize = filesize
			        data = s.recv(chunksize)
			        if data == "File does not exist":
			        	print "ERROR: FILE DOES NOT EXIST"
			        	# print "Client Exited Gracefully"
			        	overkill = 1 # BREAKS FROM CURRENT WHILE LOOP AND GOES TO START OF OUTER WHILE LOOP
			        	break

			        file_to_write.write(data)
			        filesize -= chunksize

			    if overkill == 1:
			    	overkill = 0
			    	continue
			    file_to_write.close()
			    print 'File received successfully'

		elif option == "3":

			identifierName = "----3----"
			identifiersize = len(identifierName)
			identifiersize = bin(identifiersize)[2:].zfill(16) 
			s.send(identifiersize)
			s.send(identifierName)

			s.close()
			break

	print "Client Exited Gracefully"

if __name__ == '__main__':
	Main()


