import sys
import zmq
import random
import time
import socket
from random import randrange

#
#Init ZMQ publisher
#
#This is meant to publish data to the robot identified  by the topic variable
#


topic = "controller"

avalue = 0

port = "5555"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socketP = context.socket(zmq.PUB)
socketP.bind("tcp://*:%s" % port)



#
#Your controller code here
#
#


while True:
	avalue += 2
	messagedata = avalue
	print "%s %d" % (topic, messagedata)
	print "controller sends to PS3Client"
	socketP.send("%s %d" % (topic, messagedata))
	time.sleep(8)

