# UNB-ECE-Robotics-Competition-Plaform

# Architecture 1 Notes:

This test does not incluse proper context termination which can result in getting this error :
	"Address already in use"

Reboot your unix machine to fix the problem.

# Architecture 1 Test Results

1. Message exchange is stable at reasonable data exchange speed.
2. Message exchange is stable at extremely high data exchange speed.
3. At extremely high speed, there is no data "dropped"
4. The robot drives normally at reasonable data exchange speed.
5. The robot drives normally at extremely high data exchange speed.
6. This itteration is 100% non blocking.

This test is a success.

![Architecture 1 diagram](https://github.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/blob/master/Markus/Architecture/Architecture%201/Architecture1_Test_1_Diagram.pdf)

# Architecture 2 Test 1 Notes:

1. The ability to exchange information as per the architecture 2 diagaram has been verified.
2. The ability to retain a non blocking approach on every level of the architecture has been achieved and verified.

# Architecture 2 Test 2 Notes:

This code has implemented and tested basic functionalities (start/stop/faster/slower) to control the robots.
There are also : 
	7/26/2016 -> setup of additional communication channels
			setup of 1 additional database called "masterControl" which defines the game parameters
			test current code and db usage.
		     The implementation of the database insertions has been done within the server-client file. This
			seems to provide adequate speeds for status updates. Under stress (10-20 messgaes per second), 
			the system buffers the messages automatically and queues them for database insertion. Once
			the message flow slows, the server-client writes the remaining messages from the buffer to the
			database. There are less than 1 status update per second expected to take place per server-client 
			process. Therefore the speed of operation is adequate. (class 4 sdcard, full os)
	
	7/27/2016 -> Test with two robots is a success. data transfert as per test 2 diagram is working great at 
			about 2 messages per second with little to no delay to database updates.
		    ***WARNING***
			Raspberry pi 2's show studder and the inability to receive zmq messages. The same setup for robot2
			on a raspberry pi 3 works great!
		    Test 2 is set-up exactly as described in the test 2 architecture diagram. The only thing not 
			complete is that the controller process generates it's own data to send to the robots.


- I think using a topicfilter works great to direct messages to the right place using zmq.

- I will also use a second port with an ID number topicfilter (from masterController DB) which will target robot ID=1 to robot ID=last(up to 16).
	this way we can either send data to all robots or only one which will reduce risk of impact on performace
	during high robot count or high message exchange. (TO BE IMPLEMENTED IN ARCHITECTURE 3)


# Architecture 3

#Test 1

- Implement basic masterControl functions like start/stop/slow/fast/disable any motor.(message passing is implemented but not the commands themselves)
- Implement basic controller controls to send coded commands to robots depending on robot ID (if one robot) or
	broadcast to all (if start/stop)
- Add a request field that allows to request a status update from all or just one robot.(controller side done, not robot side)

-masterControl database and control script only sends commands if there is a change in the database fields.
-Can select to send to all robots (ID field = 60) or to specific robots (ID field = 1 to 16)

- Control commands can be listed in the masterControl table in advance. the report field acts as a select signal
	to select which command (row) is active as the current robot control command. This can enable two special
	function (like rfid speed up etc). It can desable auxilary motors from one or all robots. It can stop/start
	one or all robots. It can also request a status update from one or all robots. (for request. keep all fields
	except report as NULL (empty) and set the request field to "1". (communication basis is implemented on db/controller
	but not on robot side.


#Test 2


- Just get basic communication channels working first : like changing masterControl database to start/stop all 
	robots. (now working 7/28/16) with no stutter !!
-- Implement PS3 client functions to decode commands and execute them. (go/stop)

- Implement robot side for all of test 1 controller implementations. 

** This will be done at a later time.
- Implement a scoreboard script to  be run from the server. This reads and writes to masterController AND status.


#Test 3

- Same as arch 3 test 1&2. Adds more functionality and stability fixes (such as sleep time in server scripts)



#Architecture 4 Notes:

- This version is to improve/stabilise current code. Code cleanup also done here.
- The completed architecture 4 will serve as a base system to support future robotics competitions.
- 8/3/2016 - Commit has WIP files for Architecture 4. 





# Robotics platform in depth details

Architecture 3, Test 2/3:
-	This design uses the databases (masterControl and status) as the primary data exchange medium on the server side. I think if possible, the use of zMQ from the human interface to the controller may reduce/eliminate lag. Since I have made the decision to hard code play modes (masterControl commands), the need for a database to archive all commands and used to ‘’select’’ the active command would not be necessary. 
-	The start/stop commands are working.
-	Is there a need for user controlled commands (other than game mode). Such as : robot 1 slow down. Or is it okay to let the server controller micro-manage specific actions (caused by hall effect switches and rfid tags – through the “special1” and “special2” fields).
-	Only basic functionality has been implemented to demonstrate the viability of this architecture. So far tests have been positive. Delays are minimal (even with heavy db use on server side).

Data format from server to robot:

ID	drive	aux	Special1	Special2	report	request
	
-	ID: This needs to be larger than “0” (zero) for the controller scrip to read the masterControl database. By default, use “1”.
-	Drive: If drive is “1” and request is “4”, the robot is enabled to drive normally.
      o	If drive is “0” and request is “4”, the robot is stopped.
-	Aux: This selects if the auxiliary motors are enables (“1”) or disabled (“0”). Not implemented.
-	Special1, special2: special commands where RFID tag/hall effect switch responses can be sent back to the robot. Depending on the play mode selected by the control user, these can mean different things. The controller has to implement special1&special2 capabilities in the future.
-	Report: Refers to the robot number (1..16). Use “60” for all robots.
      o	This selects either a specific robot to which this command applies or selects to send the command to all robots.
-	Request: Details what type of request the command line has.
      o	Request = “1” : return command values to null (default driving mode)
      o	Request = “2”:  Send robot status to the server.
      o	Request = “3”: special 1 is used to be a number between “0” and “1”.  This will be multiplied with the drive speed limit to slow a robot by a proportional factor of that value.
      o	Request = “4”: will either enable the robot to drive normally (drive = “1”) or stop the robot (drive = “0”)
      o	FUTURE DEVELOPMENT EXPECTED.

Data format from robot to server.

name	cdate	ctime	enmotors	pwml	pwmr	pwma1	pwma2	report

-	name: Name of the robot such as (“robot1”, “robot2”,…, “robot16”). No spaces!!!
-	cdate: The date
-	ctime: The time at which the data was sent from the robot.
-	enmotors: If “1”, motors are enabled. If “0” motors are disables.
-	pwml: Pulse width modulation left. Shows values from 0 to 100 for pwm of left motor.
-	pwmr: Pulse width modulation right. Shows values from 0 to 100 for pwm of right motor. 
-	pwma1: Pulse width modulation auxiliary 1. Shows values from 0 to 100 for pwm of aux 1 motor.
-	pwma2: Pulse width modulation auxiliary 2. Shows values from 0 to 100 for pwm of aux 2 motor.
-	report: no specific function at the moment.

CAUTION: Programmers should take note that: the robot script MUST have the sleep delays in the main loop. This is to reduce CPU load and decrease heat on the RPI. Removing the delays may cause overheating and/or catastrophic failure.

CAUTION: All values used are text based. They are surrounded by quotes ie: “1”. To use as a variable of type int, float etc you need to convert from string to int,float,etc.

#GUI notes and how to:  (coded using Tkinter for python)

The graphical user interface (starting arch3_test3) has real time robot status shown in the tables. To the left, you can enter the number of the robot (1..16) for which you want to commit changes(use “60” or leave blank for all robots). To the right, you can enter a number (float) between 0 and 1. This is a factor of speed which can be committed to slow down a robot (or all). Stop, Start can be used with robot selection. Slow down can use robot selection and factor of speed.

-Future improvements: - Have a stop/start button instead of using RadioButtons with a commit button.
			 - Sorted list (the list shows in order of who was last updated right now).
How to: To open the GUI, open a command window, navigate to the directory where the GUI .py file is located then open it using the command: sudo python filenameGUI.py



#how to get started:
1.	To run the architecture, the server has to have mysql and zmq installed.

2.	The server must have a database called “Controller” and two tables. One called “status” and the other called “masterControl”. Names are case sensitive. See what column names to use above. Be careful, they are case sensitive.

3.	The server must run the 2 control scripts (controller and GUI) as well as all of the server_client scripts (one per robot). There is space for up to 16 robots, this can be altered if more are needed (resource permitting). System tested with 2 robot at the moment (8/3/2016). Remember than increasing sleep time within the server files may increase available resources to help add more robots.

4.	You need the IP address of each robot as well as the IP address of the server.

5.	Update the IP address of the server (current: 131.202.14.109) to your own in the python scripts. It is present in the PS3_client files (one per robot). Each file has reference to a robot number (topicfilter/generaltopicfilter/targettopicfilter/aname). Use “robot1” to “robot16”. Each robot has to have distinct names. Make sure you rename the robots accordingly when creating the robot files. Update robot names in the corresponding server_client_robotX.py files.

6.	In each server_client_robotX.py files, you need to insert the IP address of the robot. EX: if server_client_robot1.py, then the IP address replacing the current IP (131.202.14.140) will the be IP of your robot 1. Do this for all robots.

7.	NOTE A: in server_client : this port number needs to be different for each robot used. Update here and on the PS3_client file on the targeted robot. I suggest using 5551(robot1),5552(robot2)…5516(robot16).

8.	There is no specific order to open the files. Just make sure all of them are opened before starting to send commands.


TIP: To make yourself comfortable with the system. Set up 2 robots and observe how it works. There are two rpi with the complete install on them for the robots and there is a server also ready. Files are found in the “Markus” folder. Just connect the RPI, get their IP’s. Change the IP’s in the files of the Architecture 4 Test 1 and try the whole system. Open each file in a command window through putty. Open the GUI by connecting the server to a monitor and open the GUI file from a command window there.


TIP2: Look at the diagrams of Architecture 3 Test 2. That is how the current design works. This shows from and to for all messages and how all the files fit together. This is the best way to understand the system





