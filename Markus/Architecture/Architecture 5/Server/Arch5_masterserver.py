#!/usr/bin/env python
#title           :Arch5_masterserver.py
#description     :Watch status db for login information from robots then runs robot specific serverclient.py processes.
#author          :Marc-Andre Couturier
#date            :Summer 2016
#version         :4
#usage           :sudo python Arch5_masterserver.py 
#notes           :See architecture 4 diagram for complimentary files and structure.
#licence		 :Personal use and academic use only. Contact if unsure. 
#owner			 :UNB Electrical and Computer Engineering under Troy Lavigne.
#python_version  :2.7  

import sys
import MySQLdb
import MySQLdb.cursors
import time
from time import *
import subprocess
import os





#*********************************************
#
#get robot IP address (wait for it to send the log-in signal)
#
#


print "Waiting for 1..16 robots to send log-in information."

varib = 0

#
#This will read the IP of this robot from the status database. If empty it will close the cursor and retry.
#
#This will also remove any lines that are considered obsolete(were in place before this script started, from a previous game)
#The while loop also keeps the database connection opened once it exits with a valid robot login information.


loggedinrobots= []
n = 1 #count how many robots have signed in


while True:
	
		db = MySQLdb.connect("localhost", "robot1", "therobot1", "Controller")
		curs=db.cursor()

		#log in information is tagged with report=25. regular rows are tagged with report=1

		curs.execute("""SELECT name,report,IP from status WHERE report = "25" """)
		data = curs.fetchone()
		sleep(0.5)

		try: #if no data fetched, will go to except (throw error at robotname = data[0])
			robotname = data[0]
			report = data[1]
			robotIP = data[2]
			curs.execute("DELETE FROM status WHERE report != '25' ")
			db.commit()
			print robotname,report,robotIP

			#run appropriate serverclient script for the robot that just signed in
			subprocess.Popen([sys.executable,"./Arch5_serverclient.py",robotname,robotIP])
			
			#remove the report field 
			curs.execute("""UPDATE status SET report = '2'WHERE name = %s""",(robotname))
			db.commit()

			#add new robot in logged in pool
			loggedinrobots[n] = robotname
			n = n + 1
			print "List of logged in robots: " ,loggedinrobots
			curs.close()
			db.close()
			continue
		except:
			curs.close()
			db.close()
			sleep(0.5)
			continue
			
		
		


	






