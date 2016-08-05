
#title           :Arch4_controller.py
#description     :Read masterControl database, process information then send information to robots.
#author          :Marc-Andre Couturier
#date            :Summer 2016
#version         :4
#usage           :sudo python Arch4_Test1_controller.py
#notes           :See architecture 4 diagram for complimentary files and structure.
#licence		 :Personal use and academic use only. Contact if unsure. 
#owner			 :UNB Electrical and Computer Engineering under Troy Lavigne.
#python_version  :2.6.6  

import sys
import zmq
import random
import time
from time import sleep
import socket
from random import randrange
import MySQLdb
import MySQLdb.cursors



#***************************CAUTION
#
#Note that all fields in the database are TEXT, therefore all variables need to be 
#dealt with as strings (double quotes "")
#




#
# Init variables
#


generaltopic = "controller"

avalue = 0
data = ""
targetdata = ""

targettopic = "" #this one needs to be dynamic ( change depending on what robot is targetted by the instruction



#
#Init database connection
#

#db = MySQLdb.connect("localhost", "root", "energySHOULDERreally03", "Controller", cursorclass = MySQLdb.cursors.SSCursor)
#masterDB=db.cursor()

#
#Keep track of previous values
#

prevIDe = ""
prevdrive= ""
prevaux= ""
prevspecial1= ""
prevspecial2= ""
prevreport= ""
prevrequest=""

dataflag = 0


#
#Init ZMQ publisher (socketP) sends data to all robots
#
#This is meant to publish data to the robot identified  by the topic variable
#



port = "6000"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socketP = context.socket(zmq.PUB)
socketP.bind("tcp://*:%s" % port)


#
#Init ZMQ publisher (targcom) sends data to a target robot
#
#This is meant to publish data to the robot identified  by the topic variable
#



port = "6001"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
targcom = context.socket(zmq.PUB)
targcom.bind("tcp://*:%s" % port)



#
#Your controller code here
#
#




#def globalSend()
	


#def targetSend()





while True:
	


	#Open new connection with database. 
	#
	#this seems to be required for every loop as the data output from this script would not reflect database changes.
	#opening and closing the connection to the database seems to fix that.
	
	db = MySQLdb.connect("localhost", "root", "energySHOULDERreally03", "Controller", cursorclass = MySQLdb.cursors.SSCursor)
	masterDB=db.cursor()

	#read masterControl database for control settings (start/stop motors, enable special1 &| special 2, enable/desable aux motors.
	
	try:
	
		masterDB.execute("""SELECT ID,drive,aux,special1,special2,report,request from masterControl
			WHERE ID>%s""",(0))
	
		data = masterDB.fetchone()

		IDe = data[0]
		drive= data[1]
		aux= data[2]
		special1=data[3]
		special2=data[4]
		report=data[5]
		request=data[6]

		#just for testing

		if IDe != prevIDe :
			prevIDe = IDe
			dataflag = 1
		if drive != prevdrive:
 			prevdrive= drive
			dataflag = 1
		if aux != prevaux:
			prevaux= aux
			dataflag = 1
		if special1 != prevspecial1:
			prevspecial1= special1
			dataflag = 1
		if special2 != prevspecial2:
			prevspecial2= special2
			dataflag = 1
		if report != prevreport:
			prevreport= report
			dataflag = 1
		if request != prevrequest:
			prevrequest=request
			dataflag= 1

		#route messages to proper robot/s. report = 0 means no transmission

		if dataflag:	

			if report == "60":
				topic="controller"
				socketP.send("%s %s %s %s %s %s %s %s" % (topic, IDe, drive, aux, special1, special2, report, request))	
				print IDe,drive,aux,special1,special2,report,request
			if report == "1":
				targettopic = "robot1"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
				print IDe,drive,aux,special1,special2,report,request
			if report == "2":
				targettopic = "robot2"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "3":
				targettopic = "robot3"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "4":
				targettopic = "robot4"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "5":	
				targettopic = "robot5"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "6":
				targettopic = "robot6"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "7":
				targettopic = "robot7"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "8":
				targettopic = "robot8"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "9":
				targettopic = "robot9"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "10":
				targettopic = "robot10"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "11":
				targettopic = "robot11"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "12":
				targettopic = "robot12"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "13":
				targettopic = "robot13"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "14":
				targettopic = "robot14"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "15":
				targettopic = "robot15"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))
			if report == "16":
				targettopic = "robot16"
				targcom.send("%s %s %s %s %s %s %s %s" % (targettopic, IDe, drive, aux, special1, special2, report,request))


	except:
		pass
	
	dataflag=0
	masterDB.close()
	db.close()
	sleep(0.05) #do nothing for 1 seconds
	