
#title           :Arch4_serverclient.py
#description     :Receive robot data, update robot status table in Controller database.
#author          :Marc-Andre Couturier
#date            :Summer 2016
#version         :4
#usage           :sudo python Arch4_serverclient.py argument1=robotname
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
robotIP = ""



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



#define query statements for db access

insertquery = ("""INSERT INTO status(name,cdate,ctime,enmotors,pwml,pwmr,pwma1,pwma2,report,IP) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

#additional protection againt duplicated login rows / and to remove old lines if table not reset before game

deletequery = ("DELETE FROM status WHERE name =%s")

#*********************************************
#
#get robot IP address (wait for it to send the log-in signal)
#
#


print "Waiting for %s to send log-in information." % topicfilter

varib = 0

#
#This will read the IP of this robot from the status database. If empty it will close the cursor and retry.
#
#This will also remove any lines that are considered obsolete(were in place before this script started, from a previous game)
#The while loop also keeps the database connection opened once it exits with a valid robot login information.

while varib == 0:
	
		db = MySQLdb.connect("localhost", "robot1", "therobot1", "Controller")
		curs=db.cursor()

		curs.execute("""SELECT report,IP from status WHERE name = %s""",(topicfilter))
		data = curs.fetchone()
		sleep(0.5)

		try:
			report = data[0]
			robotIP = data[1]
			

			if report != "25": #log in information is tagged with report=25. regular rows are tagged with report=1
				curs.execute("DELETE FROM status WHERE report != '25' ")
				db.commit()
				curs.close()
				db.close()
				continue
		except:
			curs.close()
			db.close()
			continue
			
		varib = 1 #report had value "25" for this robot, exit the login loop
		

#remove the report field 
curs.execute("""UPDATE status SET report = '2'WHERE name = %s""",(topicfilter))
db.commit()

print "%s logged in completed." % topicfilter



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
	curs.execute(deletequery,topicfilter)
	addLineDB()

def addLineDB():
	curs.execute(insertquery,(aname, cdate, ctime, aenmotor, apwml, apwmr, apwma1, apwma2, astatus, robotIP))
   	db.commit()



#This only runs once to set-up the row associated with this robot!!! (robotName = topicfilter)

addLineDB()

while True:
	
	try:
		string = socketS.recv(flags=zmq.NOBLOCK) 
		atopic,aname,cdate,ctime,aenmotor,apwml,apwmr,apwma1,apwma2,astatus,robotIP = string.split()
		print atopic,aname,cdate,ctime,astatus,robotIP
		
		updateDB()

	except:
		sleep(0.2)
	