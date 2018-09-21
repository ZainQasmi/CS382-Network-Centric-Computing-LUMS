# from threading import Timer

# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer     = None
#         self.interval   = interval
#         self.function   = function
#         self.args       = args
#         self.kwargs     = kwargs
#         self.is_running = False
#         self.start()

#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)

#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True

#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False

# from time import sleep

# def hello(name):
#     print "Hello %s!" % name

# print "starting..."
# rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
# try:
#     sleep(5) # your long-running job goes here...
# finally:
#     print "lol"
#     # rt.stop() # better in a try/finally block to make sure the program ends!


# import threading
# import time

# def printit():
#   threading.Timer(5.0, printit).start()
#   print "Hello, World!"

# printit()

# while(1):

# 	print "lol howdy"
# 	pagal = 0
# 	pagal = pagal+2
# 	print pagal

# 	time.sleep(2)

# import os
# myPath = os.getcwd() + '/bbcsport'
# cpt = sum([len(files) for r, d, files in os.walk(myPath)])
# print cpt

# num_files = 1000 #five folders
# search_start = 0
# search_range = int(search_start) + 10111

# while len(str(search_range)) < 5:
# 	search_range = '0' + str(search_range)

# print "search: ", search_range

reply = '__QUERY__43986_00234_99910_Pakistan'
reply = reply[9:]
print 'slice :: ', reply
client_port = reply[:5]
print 'cp    :: ', client_port
reply = reply[6:]
start_range = reply[:5]
print 'start :: ', int(start_range)
reply = reply[6:]
end_range = reply[:5]
print 'end   :: ', int(end_range)
query = reply[6:]
print 'query :: ', query

counter = 0
start_range = 342
end_range = 375
while counter < 1000:
	counter += 1
	if counter >= start_range and counter < end_range:
	    print "counter: ", counter
	    continue