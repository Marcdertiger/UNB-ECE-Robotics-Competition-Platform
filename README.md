# UNB-ECE-Robotics-Competition-Plaform


#Progress and thoughts (up to architecture 3)

- The whole system would be much improved with an automated "login" process where the robot braudcasts it is on, then transmits a
	message with it's IP address by zmq (transmit to all (publish)over port 5551...5566 for robot 1..16). The corresponding server_client1..16 would then update an IP and port# field which will be used to set up the port and IP numbers of the connection for any zmq sub that requires an IP. I will try to implement this soon at it may greatly improve the usability of this system(8/3/2016).






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

Architecture 1 Diagram
![Architecture 1 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%201/Architecture1_Test_1_Diagram.jpg?token=ANNZ91LQHQdlTjavMzQDaMcSpjS0cLfzks5Xqy3ewA%3D%3D)
Note: The pub/sub between the server_client and the controller is not present in the architecture. The controller sends data 
	based on time intervals to the PS3_client instead.
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

Architecture 2 Test 1 Diagram
![Architecture 2 Test 1 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%202/Architecture2_Test_1_Diagram.jpg?token=ANNZ938JOn-FqIpnomGGWxehUX2LEk6sks5Xqy5QwA%3D%3D)
 
 
  
Architecture 2 Test 2 Diagram
![Architecture 2 Test 2 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%202/Architecture2_Test_2_Diagram.jpg?token=ANNZ99_knjz4rLg3V13Mir_Fnm6qoP5Tks5Xqy59wA%3D%3D)

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

Architecture 3 Test 1 Diagram
![Architecture 3 Test 1 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%203/Architecture3_Test_1_Diagram.jpg?token=ANNZ9w1Yp2OTe4tNKNH0oAueQU4-bYFXks5Xqy6YwA%3D%3D)


#Test 2


- Just get basic communication channels working first : like changing masterControl database to start/stop all 
	robots. (now working 7/28/16) with no stutter !!
-- Implement PS3 client functions to decode commands and execute them. (go/stop)

- Implement robot side for all of test 1 controller implementations. 

** This will be done at a later time.
- Implement a scoreboard script to  be run from the server. This reads and writes to masterController AND status.



Architecture 3 Test 2 Diagram
![Architecture 3 Test 2 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%203/Architecture3_Test_2_Diagram.jpg?token=ANNZ905r9dWC1KYMDSQC9Npz8N_Y3D7gks5Xqy67wA%3D%3D)



#Test 3

- Same as arch 3 test 1&2. Adds more functionality and stability fixes (such as sleep time in server scripts)



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


#Architecture 5 Notes : 

- Additional file called Arch5_masterserver.py logs in the robots into the system and opens a single process for 
	each of the robots connected.
- The process created by this new file will time-out after 20 seconds of inactivity(robot not sending status updates)
	This is to prevent multiple processes per robot. 
- In the event of any problems, the only thing needed is to power cycle the robot itself. The server won't require
	user intervension. We could also implement a key sequence that would send the log-in signal again as to 
	remove the need to reboot affected robot. The 20 second delay may be modified in lenght as well, however this
	delay must pass before the robot is logged back into the server or else there will be duplicate processe for
	that robot.
- This file takes no arguments to run.


![Architecture 5 Diagram](https://raw.githubusercontent.com/Marcdertiger/UNB-ECE-Robotics-Competition-Platform/master/Markus/Architecture/Architecture%203/Architecture3_Test_2_Diagram.jpg?token=ANNZ905r9dWC1KYMDSQC9Npz8N_Y3D7gks5Xqy67wA%3D%3D)
Architecture 5 Diagram



# Robotics platform in depth details (per architecture)

#Architecture 3, Test 2/3:
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


#Architecture 4

This architecture focusses on creating homogeneous files that do not require modification regardless of the name/IP of each robot. 
The IP address of the server still has to be known.

-Login

The new design implements basic login between the robots and the server.

1.	Robot will try and access the remote database. There is no bypass in the 8/4/2016 upload.
2.	The robot will write “25” into the report field of the status table. This indicates to the server that the robot wants to sign-in.
3.	After a successful insert into the database, the robot exits the log-in loop and looks for a PS3 controller. Then the main loop is executed. This is when the robot starts sending status updates to the server.
4.	The server, in the meanwhile, was waiting for a field in the same database with which the report field is “25” and deleted all other rows (with name field = robotName argument).
5.	Once the server has verified the information received it exits the log-in loop and proceeds with updating the robot status row with the information received from the robot.
6.	The server will override the report field value of the robot status as soon as it exits the log-in loop. This is to prevent the server(once an automated script opens the client processes) to open multiple processes for a single robot. This is there as a fail-safe. 
-	Positive from this approach is that with MySQL, we know the info from the robot has been written and do not need to wait for a response from the server scripts before going further

-Note: fail-safe protection may be redundant. It is meant to offer the highest reliability possible during play and set-up.
Running scripts is now slightly different.
-	The PS3_client file does not need to be modified: all robots will use the same exact file.
-	The server_client file does not need to be modified: all processe required to communicate with the active robots will use the same exact file.
This is achieved using system arguments as such:
PS3_client (write in command line):
~/sudo python Arch4_PS3client.py robot2 131.202.14.109
Server_client (write in command line):
~/Sudo python Arch4_serverclient.py robot2
Notice that robot2 is the first system argument and that the PS3client requires the IP address of the server! This can be automated through a boot loader and using a local server to fetch the required information. This will be done at a later time.



