
#
# Written by Troy T. Lavigne
#
# Updated May 4, 2016 (Star Wars day!)
# 
#
# Modified by Marc-Andre Couturier (Summer 2016)
# (created architecture + message passing using zmq and mysql + GUI for masterControl)
#
#
#
# Adding ZMQ Publisher
#
# Oct 2, 2014
# Raspberry Pi demo robot
#
# Updated May 4, 2015 (Star Wars Day!) to port to 
# Raspberry Pi B+ and the Pi Interface Board
#
# Using PWM with RPi.GPIO pt 2 - requires RPi.GPIO 0.5.2a or higher
#
# Blue Motor  - right motor view behind robot, caster at rear.
# Green Motor - left motor view behind robot, caster at rear.
#
# Controls
# --------
# Left analog stick controls the left motor
# Right analog stick controls the right motor
# Aux1 with L1/R1
# Aux2 with L2/R2
#
# Known issues
# ------------
# 1) Holding L1/R1 and then pressing opposite L1/R1 will reverse direction
#


import random
from random import randrange
import zmq
import sys
import pygame
import os
import stat
import time
import subprocess
import RPi.GPIO as GPIO
from time import sleep

#
#Initialize some robot variables
#
#
#

aname= "robot2"

aenmotor = 1
astatus= 1

commandtopic=""
IDe=""
drive=""
aux=""
special1=""
special2=""
commandreport=""
request=""

override="0"


generaltopicfilter = "controller"
targettopicfilter = "robot2"

#mode = 0666|stat.S_IRUSR





#
# System Variables
#
pwmfreq=200	# in Hertz
Auxpwmlimit=50 # Set PWM value for Aux motors.
Drivepwmlimit=1 # Set MAX value for drive motors
sleeptime=0.02 # delay (in seconds) between PS3 controller readings
#sleeptime=0.001 # delay (in seconds) between PS3 controller readings
reversedrive=0 # use Triangle button to reverse drive motors
reverseaux=0   # use X button to reverse aux motors

loopcount=1 # test for client/server
loopindex=1

#
# Counters and Flags for button presses
#######################################
count_tri=0
count_tri_flag=0
count_x=0
count_x_flag=0
count_square=0
count_square_flag=0
count_circle=0
count_circle_flag=0
count_start=0
count_start_flag=0
flag_sw2=0


#
# Output pin definitions
######################################
MotorLeftpin=38
MotorLeftdir=35
MotorRightpin=40
MotorRightdir=37

MotorAux1pin=32
MotorAux1dir=31
MotorAux2pin=33
MotorAux2dir=29

Brake1234=22
#CS1234=38

UserLED=36

SysEnablepin=7
#######################################

motorLeftpwm=0
motorRightpwm=0
motorAux1pwm=0
motorAux2pwm=0

#
# To reduce CPU usage, only change PWM outputs when the joystick input changes.
# Keep track of value; save prev value and compare. If they differ, change output.
#
prevmotorLeftpwm=0
prevmotorRightpwm=0
prevmotorAux1pwm=0
prevmotorAux2pwm=0


#
# PS3 Controller button definition
# DO NOT ALTER, cause there's no need to.
#
PS3_L1=10
PS3_L2=8
PS3_L3=1

PS3_R1=11
PS3_R2=9
PS3_R3=2

PS3_triangle=12
PS3_circle=13
PS3_x=14
PS3_square=15
PS3_PS=16

PS3_select=0
PS3_start=3
PS3_up=4
PS3_right=5
PS3_down=6
PS3_left=7


#note: each robot needs to have their own port number to publish to their respective server client process.
#	They will subscribe to the same port (5559 and 6001) to listen for messages.
#
# zMQ Publisher Setup (socketP)
#

topic = "robot2"
port = "5552"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socketP = context.socket(zmq.PUB)
socketP.bind("tcp://*:%s" % port)




#
#ZMQ Subscriber Setup (socketS) receives general commands
#

port = "5559"
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
socketS.connect ("tcp://131.202.14.109:%s" % port) #server IP

if len(sys.argv) > 2:
    socketS.connect ("tcp://131.202.14.109:%s" % port1)


socketS.setsockopt(zmq.SUBSCRIBE, generaltopicfilter)

#
#ZMQ Subscriber Setup (targcom) receives targetted commands
#

port = "6001"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
targcom = context.socket(zmq.SUB)

print "Collecting updates from weather server..."
targcom.connect ("tcp://131.202.14.109:%s" % port) #server IP

if len(sys.argv) > 2:
    targcom.connect ("tcp://131.202.14.109:%s" % port1)

targcom.setsockopt(zmq.SUBSCRIBE, targettopicfilter)


avalue = 0


GPIO.setmode(GPIO.BOARD)

#
# Setup the various GPIO values, using the BCM numbers.
#########################
GPIO.setup(MotorLeftpin, GPIO.OUT) # set MotorLeftpin as output for motorLeft
GPIO.setup(MotorRightpin, GPIO.OUT)# set MotorRightpin as output for motorRight
GPIO.setup(MotorAux1pin, GPIO.OUT) # set MotorAux1pin as output for motorAux1
GPIO.setup(MotorAux2pin, GPIO.OUT) # set MotorAux2pin as output for motorAux2
GPIO.setup(Brake1234, GPIO.OUT)    # Global Brake pin
GPIO.setup(UserLED, GPIO.OUT)	   # User (Bluetooth) LED
GPIO.setup(SysEnablepin, GPIO.IN)  # Enable pin

#if GPIO.input(SysEnablepin) == 0:
#  print ("SysEnablepin is tied to GND. Exiting Program")
#  GPIO.cleanup()
#  sys.exit()

GPIO.setup(MotorLeftdir, GPIO.OUT)  # Left Motor dir
GPIO.output(MotorLeftdir, GPIO.LOW)

GPIO.setup(MotorRightdir, GPIO.OUT) # Right Motor dir
GPIO.output(MotorRightdir, GPIO.LOW)

GPIO.setup(MotorAux1dir, GPIO.OUT) # Aux1 Motor dir
GPIO.output(MotorAux1dir, GPIO.LOW)

GPIO.setup(MotorAux2dir, GPIO.OUT) # Aux2 Motor dir
GPIO.output(MotorAux2dir, GPIO.LOW)

#
# Disable Global Brake. You might have a use for it eventually
########################
GPIO.setup(Brake1234, GPIO.OUT)    # Disable Global Brake.
GPIO.output(Brake1234, GPIO.LOW)

#
# Create PWM objects
########################
motorLeft = GPIO.PWM(MotorLeftpin, pwmfreq)    # create object motorLeft for PWM
motorRight = GPIO.PWM(MotorRightpin, pwmfreq)  # create object motorRight for PWM
motorAux1 = GPIO.PWM(MotorAux1pin, pwmfreq)    # create object motorAux1 for PWM
motorAux2 = GPIO.PWM(MotorAux2pin, pwmfreq)    # create object motorAux2 for PWM


motorLeft.start(motorLeftpwm)              # start motors at 0 percent duty cycle (off)
motorRight.start(motorRightpwm)             
motorAux1.start(motorAux1pwm)
motorAux2.start(motorAux2pwm)

LeftTrack = 0
RightTrack = 0
Aux1Track = False
Aux2Track = False


#
# If SW2 is pressed, attempt to pair PS3 via USB
# The PS3 Controller must be connected to the Rpi via USB to pair.
################################################
if GPIO.input(SysEnablepin)== 0 and flag_sw2 == 0:
  print ("Attempting to pair PS3 controller via USB...")
  flag_sw2=1
  os.system("sudo hciconfig hci0 up") # Ensure Bluetooth interface is UP
  os.system("sudo hciconfig")
  os.system("sudo ./sixpair")
  os.system("sudo shutdown -r now")

#
# Initialise the pygame library
################################
pygame.init()

#
# Loop until a joystick is found.
################################
joysticks = pygame.joystick.get_count()
print str(joysticks) + " joystick(s) detected "

while (joysticks < 1):
   GPIO.output(UserLED, True)
   sleep(1) # sleep for 1 second
   GPIO.output(UserLED, False)
   sleep(1) # sleep for 1 second
   pygame.quit()
   pygame.init()
   joysticks = pygame.joystick.get_count()
   print str(joysticks) + " joystick(s) detected "

#
# Connect to the first joystick
################################
j = pygame.joystick.Joystick(0)
j.init()

#
# Setup PS3 Controller
#########################
print ('Initialized Joystick : %s' % j.get_name())

#
# Write data to Server
#
# If the locksend_s file exists, the publisher is reading data, so don't send data yet
# Otherwise, create locksend_d to lock senddata.txt file
# if senddata.txt exists for some reason, remove it.
# Fill senddata.txt with the command
# Removing locksend_d (free up PUB process to use data)
#################################################################
def senddata():
		
		now = time.localtime(time.time())
		ctime = time.strftime("%H:%M:%S", now)
		cdate = time.strftime("%y/%m/%d", now)
		
		print "%s %d" % (topic, avalue)
		#print ctime,cdate
		print "PS3client-send-to-serverclient"
		socketP.send("%s %s %s %s %d %d %d %d %d %d" % (topic,aname,cdate,ctime, aenmotor,motorLeftpwm,motorRightpwm,motorAux1pwm,motorAux2pwm,astatus))

		return

def receivedata(drive,aux,special1,special2,commandreport,request):

	
 	#receive from 2nd socket here (targetted commands)
		
	try:
		string = targcom.recv(flags=zmq.NOBLOCK)
   		commandtopic,IDe,drive,aux,special1,special2,commandreport,request = string.split()
		print "PS3client-receive-from-target-controller"
		print (IDe,drive,aux,special1,special2,commandreport,request)

	except:
		pass


	#receive general commands here (to all robots)

	try:


		stringa = socketS.recv(flags=zmq.NOBLOCK)
   		commandtopic,IDe,drive,aux,special1,special2,commandreport,request = stringa.split()
		print "PS3client-receive-from-general-controller"
		print (IDe,drive,aux,special1,special2,commandreport,request)

	except:
		pass

	return (drive,aux,special1,special2,commandreport,request)

#
#
# mainControl() will decode the command codes received from the Controller process
# This method will look at both general command (topicfilter = controller ) as well
# as commands directed to the robot itself (topicfilter = robotID)
#
# This code assumes it will only be sent data ONLY IF it's current state needs to change.
# That is dealt with by the controller script on the server.
#
#


def mainControl(drive,aux,special1,special2,commandreport,request,override):

	
	global Drivepwmlimit

# ID # 1 is the default driving mode, reset command values then return.
	print drive,aux,special1,special2,commandreport,request

	if request == "1":
		commandtopic=""
		IDe=""
		drive=""
		aux=""
		special1=""
		special2=""
		request=""
		commandreport=""
		return


	# ID # 4 means that we will control main motor function. Either start or stop the motors.
	if request == "4":
		if drive == "0":
			print "stop"
			#motorLeftpwm = 0
   			#motorRightpwm = 0
			motorLeft.ChangeDutyCycle(0)
			motorRight.ChangeDutyCycle(0)
			override="1"
			
		if drive == "1":
			print "GO"
			motorLeft.ChangeDutyCycle(motorLeftpwm*Drivepwmlimit)
			motorRight.ChangeDutyCycle(motorRightpwm*Drivepwmlimit)
			override = "0"
		
	if request == "5":
		print "slow"
		Drivepwmlimit= float(special1)
		override="0"

	return override
            
#motorAux1.start(motorAux1pwm)
#motorAux2.start(motorAux2pwm)


#
# Configure the motors to match the current settings.
#########################
def setmotors():
	#print "X"

	if prevmotorLeftpwm != motorLeftpwm:
	  motorLeft.ChangeDutyCycle(motorLeftpwm*Drivepwmlimit)
	  #prevmotorLeftpwm = motorLeftpwm

        if prevmotorRightpwm != motorRightpwm:
          motorRight.ChangeDutyCycle(motorRightpwm*Drivepwmlimit)
          #prevmotorRightpwm = motorRightpwm

        if prevmotorAux1pwm != motorAux1pwm:
          motorAux1.ChangeDutyCycle(motorAux1pwm)
          #prevmotorAux1pwm = motorAux1pwm

        if prevmotorAux2pwm != motorAux2pwm:
          motorAux2.ChangeDutyCycle(motorAux2pwm)
          #prevmotorAux2pwm = motorAux2pwm

        #prevmotorLeftpwm = motorLeftpwm
        #prevmotorRightpwm = motorRightpwm
        #prevmotorAux1pwm = motorAux1pwm
        #prevmotorAux2pwm = motorAux2pwm

        if LeftTrack < 0:
	 if reversedrive == 0:
	  GPIO.output(MotorLeftdir,True)
	 else:
	  GPIO.output(MotorLeftdir,False)

        else: # LeftTrack = 1
         if reversedrive == 0:
          GPIO.output(MotorLeftdir,False)
         else:
          GPIO.output(MotorLeftdir,True)


        if RightTrack < 0:
         if reversedrive == 0:
          GPIO.output(MotorRightdir,False)
         else:
          GPIO.output(MotorRightdir,True)

        else: # RightTrack = 1
         if reversedrive == 0:
          GPIO.output(MotorRightdir,True)
         else:
          GPIO.output(MotorRightdir,False)


	GPIO.output(MotorAux1dir,Aux1Track^reverseaux)
        GPIO.output(MotorAux2dir,Aux2Track^reverseaux)



# Try and run the main code, and in case of failure we can stop the motors
try:
    # Turn on the motors
    #GPIO.output(MotorAE, True)
    #GPIO.output(MotorBE, True)

    #
    # This is the main loop
    ##########################

    while True:
	if loopcount == 40: # Publish data ~ every 0.5s
		loopcount = 1
		senddata()
		avalue += 1
                loopindex = loopindex+1
        loopcount = loopcount + 1;
	


	drive,aux,special1,special2,commandreport,request = receivedata(drive,aux,special1,special2,commandreport,request)

	override = mainControl(drive,aux,special1,special2,commandreport,request,override)
	
	if override == "1":
		drive,aux,special1,special2,commandreport,request = receivedata(drive,aux,special1,special2,commandreport,request)
		sleep(sleeptime*5) # Test, sleeping 20ms between samples to reduce CPU load
		continue

	sleep(sleeptime*2) # Test, sleeping 20ms between samples to reduce CPU load

	#
	# Time how long the Triangle, X, and Start buttons are pressed
	# Use this information to change default motor direction and shutdown robot
	###########################################################################
        if count_tri_flag > 0:
	  count_tri = count_tri + 1;
	else:
	  count_tri = 0;

        if count_x_flag > 0:
          count_x = count_x + 1;
        else:
          count_x = 0;

        if count_start_flag > 0:
          count_start = count_start + 1;
        else:
          count_start = 0;


        # Check for any queued events and then process each one
        events = pygame.event.get()
        for event in events:
          UpdateMotors = 0

          #
          # Check if one of the joysticks has moved
          ############################################
          if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1:
              LeftTrack = event.value
              #print "LeftTrack %f " % (LeftTrack)
              UpdateMotors = 1
            elif event.axis == 3:
              RightTrack = event.value
	      #print "RightTrack %f " % (RightTrack)
              UpdateMotors = 1

            #
            # Check if we need to update what the motors are doing
            ######################################################
            if UpdateMotors:
	      if LeftTrack < 0:
	      	motorLeftpwm=round(abs(LeftTrack*100))
	      else:
                motorLeftpwm=round(LeftTrack*100)
             
              if RightTrack < 0:
                motorRightpwm=round(abs(RightTrack*100))
              else:
                motorRightpwm=round(RightTrack*100)
             
	      #print "motorLeftpwm %f " % (motorLeftpwm)
              #print "motorRightpwm %f " % (motorRightpwm)

#
# Look for Aux motor button presses.
#################################################
	  elif event.type == pygame.JOYBUTTONDOWN:

            #print "joy button down"

            if event.button == PS3_L1:
	      motorAux1pwm = Auxpwmlimit
	      Aux1Track = True
	    elif event.button == PS3_R1:
              motorAux1pwm = Auxpwmlimit
              Aux1Track = False
	    elif event.button == PS3_L2:
              motorAux2pwm = Auxpwmlimit
              Aux2Track = True
            elif event.button == PS3_R2:
              motorAux2pwm = Auxpwmlimit
              Aux2Track = False

            elif event.button == PS3_triangle:
	      count_tri_flag = 1
	      print "Triangle button down"
            elif event.button == PS3_x:
              count_x_flag = 1
              print "X button down"
            elif event.button == PS3_square:
              pass
            elif event.button == PS3_circle:
              pass		
            elif event.button == PS3_start: # Shutdown robot!
              count_start_flag = 1
              print "Start button pressed."


            elif event.button == PS3_L2 or event.button == PS3_R2:
              motorAux2pwm=0

	    #print "joy button down"
	    #print "event.axis %d" % (event.button)

#
# Look for Aux motor button releases.
#################################################
          elif event.type == pygame.JOYBUTTONUP:
            #print "joy button up"

	    if event.button == PS3_L1 or event.button == PS3_R1:
	      motorAux1pwm=0

	    elif event.button == PS3_L2 or event.button == PS3_R2:
              motorAux2pwm=0


            elif event.button == PS3_triangle:
              count_tri_flag=0
	      #print "Count is %d" % (count_tri)

              if count_tri > 250: # about 5 seconds
                #print "Reverse Drive motors."
		if reversedrive == 0:
		  reversedrive = 1
	        else:
		  reversedrive = 0
              count_tri=0

            elif event.button == PS3_x:
              count_x_flag=0
              #print "Count is %d" % (count_x)

              if count_x > 250: # about 5 seconds
                #print "Reverse Aux motors."
                if reverseaux == 0:
                  reverseaux = 1
                else:
                  reverseaux = 0
              count_x=0

            elif event.button == PS3_start:
              count_start_flag=0
              #print "Count Start is %d" % (count_start)

              if count_start > 250: # about 5 seconds
		print "Shutting down robot now..."
                os.system("sudo shutdown -h now")
		while True:	
                  motorRight.ChangeDutyCycle(0)
                  motorLeft.ChangeDutyCycle(0)
                  motorAux1.ChangeDutyCycle(0)
                  motorAux2.ChangeDutyCycle(0)

              count_start=0

	       
	     #print "Let go of L1"
            #elif event.axis == 8:
              #print "Pressed L2"

          setmotors()
          prevmotorLeftpwm = motorLeftpwm
          prevmotorRightpwm = motorRightpwm
          prevmotorAux1pwm = motorAux1pwm
          prevmotorAux2pwm = motorAux2pwm



except KeyboardInterrupt:
    # Turn off the motors
    motorRight.stop()
    motorLeft.stop()
    j.quit()#!/usr/bin/env python
    #subprocess.Popen(['rm','/var/tmp/senddata.txt'])
    #subprocess.Popen(['rm','/var/tmp/locksend_d'])

    

GPIO.cleanup()
socketP.close()
socketS.close()

