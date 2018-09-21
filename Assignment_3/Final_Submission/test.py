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

# reply = '__QUERY__43986_00234_99910_Pakistan'
# reply = reply[9:]
# print 'slice :: ', reply
# client_port = reply[:5]
# print 'cp    :: ', client_port
# reply = reply[6:]
# start_range = reply[:5]
# print 'start :: ', int(start_range)
# reply = reply[6:]
# end_range = reply[:5]
# print 'end   :: ', int(end_range)
# query = reply[6:]
# print 'query :: ', query

# counter = 0
# start_range = 342
# end_range = 375
# while counter < 1000:
# 	counter += 1
# 	if counter >= start_range and counter < end_range:
# 	    print "counter: ", counter
# 	    continue

# import sys
# from termcolor import colored, cprint

# text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
# print(text)
# cprint('Hello, World!', 'green', 'on_red')

# print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
# print_red_on_cyan('Hello, World!')
# print_red_on_cyan('Hello, Universe!')

# for i in range(10):
#     cprint(i, 'magenta', end=' ')

# cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)

import sys
from termcolor import colored, cprint

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

string ="Marry had lamb . A little lamb"
# part="had. lamb"
part="lamb"
# partwords = part.split()
for word in string.split():
	if word not in part:
		print c.Default+word,
	else:
		print c.red+word,

# from colorama import init, Fore, Back, Style
# init()

# def cprint(msg, foreground = "black", background = "white"):
#     fground = foreground.upper()
#     bground = background.upper()
#     style = getattr(Fore, fground) + getattr(Back, bground)
#     print(style + msg + Style.RESET_ALL)

# print 'pakistan' + cprint("colorful output, wohoo", "red", "black")
