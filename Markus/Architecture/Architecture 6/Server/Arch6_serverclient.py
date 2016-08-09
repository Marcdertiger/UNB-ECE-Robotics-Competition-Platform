
#title           :Arch4_serverclient.py
#description     :Receive robot data, update robot status table in Controller database.
#author          :Marc-Andre Couturier
#date            :Summer 2016
#version         :4
#usage           :sudo python Arch4_serverclient.py argument1=robotname argument2=robotIP
#notes           :See architecture 4 diagram for complimentary files and structure.
#licence		 :Personal use and academic use only. Contact if unsure. 
#owner			 :UNB Electrical and Computer Engineering under Troy Lavigne.
#python_version  :2.6.6  

import sys
import zmq
import MySQLdb
import MySQLdb.cursors
import time
from time import *



topicfilter = str(sys.argv[1])
print topicfilter
robotIP = str(sys.argv[2])



atopic=None
aname=topicfilter
cdate=None
ctime=None
aenmotor=None
astatus=None
apwml=None
apwmr=None
apwma1=None
apwma2=None

timeout = 0
trigger=0

#
#Init ZMQ subscriber 
#
#this is meant to read data sent from the robot identified by the topicfilter
#

# NOTE A:
#This port number needs to be different for each robot used, update here and on the PS3_client file on the targetted robot.

port = "5551"

# Socket to talk to server
context = zmq.Context()
socketS = context.socket(zmq.SUB)


socketS.connect ("tcp://%s:%s" % (robotIP,port))    #Robot ip address
socketS.setsockopt(zmq.SUBSCRIBE, topicfilter)





def updateDB():
	
	db = MySQLdb.connect("localhost", "robot1", "therobot1", "Controller")
	curs=db.cursor()

	curs.execute("""UPDATE status SET cdate=%s,ctime=%s,enmotors=%s,pwml=%s,pwmr=%s,pwma1=%s,pwma2=%s,report=%s,IP=%s WHERE name =%s""",(cdate, ctime, aenmotor, apwml, apwmr, apwma1, apwma2, astatus, robotIP,aname))
	db.commit()
	
	curs.close()
	db.close()


while True:
	
	try:
		string = socketS.recv(flags=zmq.NOBLOCK) 
		atopic,aname,cdate,ctime,aenmotor,apwml,apwmr,apwma1,apwma2,astatus,robotIP = string.split()
		print atopic,aname,cdate,ctime,astatus,robotIP
		trigger=0
		updateDB()

	except:
		sleep(0.2)
		timeout = timeout + 1
		if trigger == 50: #timeout after 10 second of robot not sending status updates. robot status = 100 means offline du to timed out communication
			print " robot %s time out.",( topicfilter )
			robotIP= "0"
			astatus="100"
			updateDB()
			quit()
	trigger=trigger+1




	