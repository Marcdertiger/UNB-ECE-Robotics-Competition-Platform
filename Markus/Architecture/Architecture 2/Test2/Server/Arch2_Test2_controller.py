import sys
import zmq
import random
import time
from time import sleep
import socket
from random import randrange
import MySQLdb
import MySQLdb.cursors


selectID = 1; #this is where you can select the database ID which changes the game mode(row number in the DB)

#
#Init database connection
#

db = MySQLdb.connect("localhost", "root", "energySHOULDERreally03", "Controller")
masterDB=db.cursor()

#
#Keep track of previous values
#

prevIDe = ""
prevdrive= ""
prevaux= ""
prevspecial1= ""
prevspecial2= ""
prevreport= ""

topic = "controller"


#
#Init ZMQ publisher
#
#This is meant to publish data to the robot identified  by the topic variable
#


topic = "controller"

avalue = 0
data = ""

port = "5559"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socketP = context.socket(zmq.PUB)
socketP.bind("tcp://*:%s" % port)

masterDB.execute("INSERT into masterControl(ID,drive,aux,special1,special2,report) Values('0','1','2','3','4','5')")

#
#Your controller code here
#
#


while True:
	
	#read masterControl database for control settings (start/stop motors, enable special1 &| special 2, enable/desable aux motors.
	
	masterDB.execute("SELECT ID,drive,aux,special1,special2,report from masterControl")
	data = masterDB.fetchone()
	
	IDe = data[0]
	drive= data[1]
	aux= data[2]
	special1=data[3]
	special2=data[4]
	report=data[5]


	print IDe,drive,aux,special1,special2,report

	if IDe == selectID:
		if drive != prevdrive: 
			if aux != prevaux:
				if special1 != prevspecial1:
					if special2 != prevspecial2:
						if report != prevreport:
							socketP.send(" %s, %s, %s, %s, %s " % ( IDe, drive, aux, special1, special2, report))
							print "sent"
	socketP.send("%s %s %s %s %s %s %s " % (topic, IDe, drive, aux, special1, special2, report))

	sleep(5) #do nothing for 5 seconds
