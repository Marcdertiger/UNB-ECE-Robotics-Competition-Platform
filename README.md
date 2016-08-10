# UNB-ECE-Robotics-Competition-Plaform




#How Login Process Works


1. The robot will connect to http://ece.unb.ca/robotics and fetch the two text files it needs to 
	acquire the address of the RPI server and it’s name.
	
2. The robot will insert it’s log-in info into the Controller database, status table. 
	It can access the database because it now knows the IP address of the RPI server. The log-in
	info is identified by a report field of value “25”.

3."masterserver.py" monitors the status table for entries with the report field with value “25”.

4. Once it sees the log-in info, it reads the IP and name and then opens a subprocess for the robot. 
	The subprocess takes care of receiving data from the robot and updating the status table accordingly.
	Once the log-in info is read, the masterserver.py will change the value to report = “2” to prevent 
	creating multiple processes per robot.











#Architecture 6

There are general improvements and fixes for most files.

New:
	-Robots now get their names from the http:// server (using hostname of the robot rpi)
	-Robots now get their names from the http:// server (using MAC address of the robot rpi) -hostname replaced by MAC
	
##8/9/2016
- Totally automated login process added. If no connection to http server or no database access to the gameserver, any robot will run
	with default PS3 controls. The robot gets it's name from the Robot_Name.txt file on the http server. The hostname of each robot is used to identify who it is. (current format : "robotone","robottwo",...,"robotsixteen".
	In the future, using the MAC address of each RPI instead of the hostname will make the robot image more portable(no need to
	change the hostname on each robot, only have to gather all mac addresses the first time we set-up the robot RPI's).
- General improvements and fixes.
- WARNING: Most variables used in all code is text based (not numbers). Check for quotes "". 
- WARNING: Text based variables (string/character...) are case sensitive!
	
	
	
Future improvements considered:
	-Instead of hostname, use MAC address. (to make it easier to setup each RPI)
	-If robot was successful connecting to web server + send it's login info but then the RPI server goes down, we
		need to make sure the robot will still drive in default mode (aname = "NOSERVER" and default drive variables).


#Architecture 5 Notes : 

commit1:8/5/16

- Additional file called Arch5_masterserver.py logs in the robots into the system and opens a single process for 
	each of the robots connected.
- The process created by this new file will time-out after 10 seconds of inactivity(robot not sending status updates)
	This is to prevent multiple processes per robot. 
- In the event of any problems, the only thing needed is to power cycle the robot itself. The server won't require
	user intervension. We could also implement a key sequence that would send the log-in signal again as to 
	remove the need to reboot affected robot. The 10 second delay may be modified in lenght as well, however this
	delay must pass before the robot is logged back into the server or else there will be duplicate processe for
	that robot.
- This file takes no arguments to run.

commit2:8/5/16
-Further improvements done to overall sign-in process and database accesses.

Soon:
-Implement method for the robots to obtain the server IP and their name automatically.
	Probably a simple wget on a webserver to get a .txt file of the server's IP and name
	This file will also contain the name the robot should use.

There are general improvements and fixes for all files.

New: 
	-masterserver file to open the processes needed to receive and archive data from the robot.
	-Inactive robots will time-out after 5-10 seconds(you can modify this in serverclient file).
	-The graphical interface now displays an inactive robot with it's name field in a red background and white text.
	-There is no specific order with which turn on the server or the robot.
		1. The robot waits until it is able to write it's login information on the server (ADD OVERRIDE FOR DEMOS)
		2. The server waits until a robot entry in the status table has a value of report="25" (login signal)
		So the order of which is turned on first is insignificant.

![Architecture 5 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%203/Architecture3_Test_2_Diagram.jpg?token=ANNZ905r9dWC1KYMDSQC9Npz8N_Y3D7gks5Xqy67wA%3D%3D)
Architecture 5 Diagram




#Architecture 4 Notes:

- This version is to improve/stabilise current code. Code cleanup also done here.
- The completed architecture 4 will serve as a base system to support future robotics competitions.
- 8/3/2016 - Commit has WIP files for Architecture 4. 

8/4/16:

- Steamline set-up process for users by creating log-in process between PS3client and server_client.
- Now only need to provide IP address of the server to the robot script by passing a system variable when
	executing the script.
- Layed out cautionary actions to prevent ducplicated rows in status database.
- Layed out cautionary actions to prevent duplicate processes for the same robot when the future server_client_creator script
	will be added.

server_client_creator: This script will open a single server_client script per robot to enable communication.
	This script should take ownership of the sign-in process on the server side.



# Architecture 3

##Test 1

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

Architecture 3 Test 1 Diagram
![Architecture 3 Test 1 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%203/Architecture3_Test_1_Diagram.jpg?token=ANNZ9w1Yp2OTe4tNKNH0oAueQU4-bYFXks5Xqy6YwA%3D%3D)


##Test 2


- Just get basic communication channels working first : like changing masterControl database to start/stop all 
	robots. (now working 7/28/16) with no stutter !!
-- Implement PS3 client functions to decode commands and execute them. (go/stop)

- Implement robot side for all of test 1 controller implementations. 

** This will be done at a later time.
- Implement a scoreboard script to  be run from the server. This reads and writes to masterController AND status.



Architecture 3 Test 2 Diagram
![Architecture 3 Test 2 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%203/Architecture3_Test_2_Diagram.jpg?token=ANNZ905r9dWC1KYMDSQC9Npz8N_Y3D7gks5Xqy67wA%3D%3D)



##Test 3

- Same as arch 3 test 1&2. Adds more functionality and stability fixes (such as sleep time in server scripts)




## Architecture 2 Test 2 Notes:

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

Architecture 2 Test 1 Diagram
![Architecture 2 Test 1 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%202/Architecture2_Test_1_Diagram.jpg?token=ANNZ938JOn-FqIpnomGGWxehUX2LEk6sks5Xqy5QwA%3D%3D)
 
 
  
Architecture 2 Test 2 Diagram
![Architecture 2 Test 2 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%202/Architecture2_Test_2_Diagram.jpg?token=ANNZ99_knjz4rLg3V13Mir_Fnm6qoP5Tks5Xqy59wA%3D%3D)





# Architecture 1 Notes:

This test does not incluse proper context termination which can result in getting this error :
	"Address already in use"

Reboot your unix machine to fix the problem.

## Architecture 1 Test Results

1. Message exchange is stable at reasonable data exchange speed.
2. Message exchange is stable at extremely high data exchange speed.
3. At extremely high speed, there is no data "dropped"
4. The robot drives normally at reasonable data exchange speed.
5. The robot drives normally at extremely high data exchange speed.
6. This itteration is 100% non blocking.

This test is a success.

Architecture 1 Diagram
![Architecture 1 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%201/Architecture1_Test_1_Diagram.jpg?token=ANNZ91LQHQdlTjavMzQDaMcSpjS0cLfzks5Xqy3ewA%3D%3D)
Note: The pub/sub between the server_client and the controller is not present in the architecture. The controller sends data 
	based on time intervals to the PS3_client instead.
# Architecture 2 Test 1 Notes:

1. The ability to exchange information as per the architecture 2 diagaram has been verified.
2. The ability to retain a non blocking approach on every level of the architecture has been achieved and verified.



#Data packaging and variable definitions


##Data format from server to robot:

ID	drive	aux	  Special1  	Special2 	report	request
	
-	ID: This needs to be larger than “0” (zero) for the controller scrip to read the masterControl database. By default, use “1”.
-	Drive: If drive is “1” and request is “4”, the robot is enabled to drive normally.
      o	If drive is “0” and request is “4”, the robot is stopped.
	  o Can be used in any configuration under different requests.
-	Aux: This selects if the auxiliary motors are enables (“1”) or disabled (“0”). Not implemented.
-	Special1, special2: special commands where RFID tag/hall effect switch responses can be sent back to the robot. 
		Depending on the play mode selected by the control user, these can mean different things. The controller has 
		to implement special1&special2 capabilities in the future.
-	Report: Refers to the robot number (1..16). Use “60” for all robots.
      o	This selects either a specific robot to which this command applies or selects to send the command to all robots.
-	Request: Details what type of request the command line has.
      o	Request = “1” : return command values to null (default driving mode)
      o	Request = “2”:  Send robot status to the server.
      o	Request = “3”: special 1 is used to be a number between “0” and “1”.  This will be multiplied with the drive speed limit to slow a robot by a proportional factor of that value.
      o	Request = “4”: will either enable the robot to drive normally (drive = “1”) or stop the robot (drive = “0”)
      o	Other request numbers can be used for new commands.
	  
- The special1&special2 values are mostly meant to be command variables(select speed, on/off, etc).
- The other fields are meant as command select values (select what to do).

-The actual selection of the values given to all the data fields above is done in the graphical interface(GUI) python file.
-The processing of the values in the fields is done on each PS3client python scripts in the mainControl() method.

##Data format from robot to server.

name	cdate	ctime	enmotors	pwml	pwmr	pwma1	pwma2	report

-	name: Name of the robot such as (“robot1”, “robot2”,…, “robot16”). No spaces in the name itself!!!
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





--------------------------------------------------------------------------------------------------------

