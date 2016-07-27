import MySQLdb
import zmq
import time
from time import sleep
import sys
import decimal
from decimal import *

db = MySQLdb.connect("localhost", "robot1", "therobot1", "Controller")
curs=db.cursor()


port = "555"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socketS = context.socket(zmq.SUB)

print "Collecting updates from weather server..."
socketS.connect ("tcp://127.0.0.1:%s" % port) #server IP

if len(sys.argv) > 2:
    socketS.connect ("tcp://127.0.0.1:%s" % port1)
topicfilter="robot1"
socketS.setsockopt(zmq.SUBSCRIBE,'')






query = ("""INSERT INTO status(name)""" "Values(%s)")

flag1=0

while True:
	try:	
		string = socketS.recv()
		topic,aname,adate,atime,aenmotors,areport = string.split()
		print topic,aname,adate,atime,aenmotors,areport
   		flag1=1
	except:
		flag1=0

	if flag1 == 1:
		try:
			curs.execute (query,aname)
   			db.commit()
			sleep(0.5)
   			print topic
			flag1=0
		except:
  			  pass
	