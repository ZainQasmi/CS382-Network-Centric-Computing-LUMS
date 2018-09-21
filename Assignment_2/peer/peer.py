#################################################################
# Course 			: CS-382 Network Centric Computing 			#
# Offering 			: Spring 2017								#
# University		: Lahore University of Management Sciences	#
# File name 		: peer.py                  			#
# Assignment title 	: Programming Assignment 2 Part 1					#
# Author 			: Muhammad Zain Qasmi && Hassaan Hassaan 	#
# Roll No. 			: 18100276 && 18100059						#
# Submission 		: March 18th, 2017						#
# Instructor 		: Fareed Zaffar								#
# Python Version 	: 2.7										#
#################################################################


#==============================================================================

import socket
import sys
import os


currenDir = os.getcwd()
fileList = []

def generateTorrent():
	assignKey = 1
	for directory, dirnames, filenames in os.walk(currenDir + '/upload'):
		os.chdir(directory)
		folder = os.getcwd()
		files_ = os.listdir(folder)
		for files in sorted(files_):
			# print os.path.splitext(files)[0], os.stat(files).st_size , os.path.splitext(files)[1]
			fileList.append(os.path.splitext(files)[0])
			text_file = open(currenDir + '/' + os.path.splitext(files)[0] + '.torrent', "w")
			text_file.write(files + '\n' + str(assignKey) + '\n' + str(os.stat(files).st_size) + '\n' + str(os.stat(files).st_size/10240))
			text_file.close()
			assignKey = assignKey + 1

def Main():
	generateTorrent()
	#host = '127.0.0.1'
	#port = 5030
	host = sys.argv[1]
	port = int(sys.argv[2])
	s = socket.socket()
	s.connect((host, port))

	overkill = 0; #the breaker of loops, terminator of programs

	print "#################################################################"
	print "#								#"
	print "#                Welcome to CS 382 Peer Client		#"
	print "#								#"	
	print "#################################################################"

	while True:

		print "================================================================="
		print 'Press 1 to search something'
		print 'Press 2 to upload all torrent files to server'
		print 'Press 3 to exit network'
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

			# while True:
			for i in range (0,len(fileList)):

			    # filename = 'abc.torrent'
			    # filePath = '/home/zainqasmi/Desktop/netcent2/peer'

			    filename = fileList[i] + '.torrent'
			    print fileList[i]
			    filePath = currenDir


			    size = len(filename)
			    size = bin(size)[2:].zfill(16) 
			    s.send(size)
			    s.send(filename)

			    # totalSent = str.split(filename)
			    # filename = totalSent[0]
			    # filePath = totalSent[1]

			    filename = os.path.join(filePath,filename)
			    filesize = os.path.getsize(filename)
			    filesize = bin(filesize)[2:].zfill(32)
			    s.send(filesize)

			    file_to_send = open(filename, 'rb')

			    l = file_to_send.read()
			    s.sendall(l)
			    file_to_send.close()
			    print 'File Sent'

			

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

