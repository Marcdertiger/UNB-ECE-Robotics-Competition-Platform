
#title           :Arch4_Test1_serverclient_robot1.py
#description     :Receive robot data, update robot status table in Controller database.
#author          :Marc-Andre Couturier
#date            :Summer 2016
#version         :4
#usage           :sudo python Arch4_Test1_serverclient_robot1.py
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

topicfilter = "robot1"


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



db = MySQLdb.connect("localhost", "robot1", "therobot1", "Controller",cursorclass = MySQLdb.cursors.SSCursor)
curs=db.cursor()

insertquery = ("""INSERT INTO status(name,cdate,ctime,enmotors,pwml,pwmr,pwma1,pwma2,report) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s)""")

deletequery = ("DELETE FROM status WHERE name = 'robot1' ")


#
#Init ZMQ subscriber 
#
#this is meant to read data sent from the robot identified by the topicfilter
#

# NOTE A:
#This port number needs to be different for each robot used, update here and on the PS3_client file on the targetted robot.

port = "5551"
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
socketS.connect ("tcp://131.202.14.140:%s" % port)    #Robot ip address

if len(sys.argv) > 2:
    socketS.connect ("tcp://131.202.14.140:%s" % port1)

socketS.setsockopt(zmq.SUBSCRIBE, topicfilter)




flag1=0



def updateDB():
	curs.execute(deletequery)
	addLineDB()

def addLineDB():
	curs.execute(insertquery,( aname, cdate, ctime, aenmotor, apwml, apwmr, apwma1, apwma2, astatus))
   	db.commit()



#This only runs once to set-up the row associated with this robot!!! (robotName = topicfilter)

addLineDB()	

while True:
	
	try:
		string = socketS.recv(flags=zmq.NOBLOCK) #receive client No. topicfilter data
		atopic,aname,cdate,ctime,aenmotor,apwml,apwmr,apwma1,apwma2,astatus = string.split()
		print atopic,aname,cdate,ctime,astatus
		
		updateDB()

	except:
		sleep(0.1)
	