import socket   #for sockets
import sys  #for exit
import errno
import time
import threading
import os


currenDir = os.getcwd()


def search(data):

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
                                with open(files) as myFile:
                                    for num, line in enumerate(myFile, 1):
                                        if data in line:
                                            data2 = data2 + " " + str(num) # make this a list               
                                    data1 = "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory
                                    # print directory
                                    data2 = ""
                                    print data1
                                    # clientsocket.send(data1)

                                    time.sleep(0.001)
                                    f.close()
                            else:
                                f.close()
                # clientsocket.send("End of Results!!!")
                endStr = "End of Results!!!"
    # data2 = ""
    # jobStatus = 2
    # currenDir = os.getcwd()
    # path = os.getcwd()
    # data = query
    # for directory, dirnames, filenames in os.walk(currenDir):
    #     os.chdir(directory)
    #     folder = os.getcwd()
    #     files_ = os.listdir(folder)
    #     for files in sorted(files_):
    #         if os.path.isfile(files):
    #             f = open (files, 'r')
    #             file_contents = f.read()
    #             if data in file_contents:
    #                 jobStatus = 2
    #                 with open(files) as myFile:
    #                     for num, line in enumerate(myFile, 1):
    #                         if data in line:
    #                             data2 = data2 + " " + str(num) # make this a list               
    #                     data1 = "__RESPONSE__" + "Name: " + f.name + " Line(s):" + data2 + "   Loc: " + directory
                        
    #                     data2 = ""
    #                     print data1
    #                     time.sleep(0.001)
    #                     f.close()
    #             else:
    #                 jobStatus = 1
    #                 f.close()
    # return jobStatus




while(1) :
    query = raw_input('Enter message to send : ')
    job_done = search(query)
     
