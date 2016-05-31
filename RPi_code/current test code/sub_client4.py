import sys
import zmq

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting updates from Raspberry Pi Robotics Comp server..."
socket.connect ("tcp://131.202.12.117:%s" % port)

if len(sys.argv) > 2:
    socket.connect ("tcp://131.202.12.117:%s" % port1)

# Subscribe to zipcode, default is NYC, 10001
topicfilter = "131.202.12.117"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)


# Process 5 updates
last=0

while True:
	string = socket.recv()
    	topic, messagedata = string.split()
    	diff = int(messagedata)- int(last)
    	#if (int(messagedata)%1000) == 0:
	print messagedata, diff

    	if diff != 1:
		print "Robot skipped write"
		#sys.exit() 

#    total_value += int(messagedata)
    	#print messagedata, diff
    	last = messagedata
#print "Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr)
