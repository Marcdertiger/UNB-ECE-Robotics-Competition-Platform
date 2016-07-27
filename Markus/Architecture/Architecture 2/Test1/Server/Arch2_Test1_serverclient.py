import sys
import zmq

#
#Init ZMQ subscriber 
#
#this is meant to read data sent from the robot identified by the topicfilter
#

topicfilter = "robot1"


port = "5556"
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
socketS.connect ("tcp://131.202.14.160:%s" % port)

if len(sys.argv) > 2:
    socketS.connect ("tcp://131.202.14.160:%s" % port1)

socketS.setsockopt(zmq.SUBSCRIBE, topicfilter)





#
#Code for client to server data processing
#
# 

while True:
	
	try:
		string = socketS.recv(flags=zmq.NOBLOCK) #receive client No. topicfilter data
		topic,aname,cdate,ctime, aenmotor,astatus = string.split()
		print topic,aname,cdate,ctime,astatus		
	except:
		pass

socketS.close()     
