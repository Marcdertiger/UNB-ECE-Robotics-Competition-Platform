import MySQLdb
import zmq
import time

db = MySQLdb.connect("localhost", "robot1", "therobot1", "Controller")
curs=db.cursor()

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:1212")
subscriber.setsockopt(zmq.SUBSCRIBE, '')
 
query = ("""INSERT INTO status(name,cdate,ctime,enmotors,pwml,pwmr,pwma1,pwma2,report)""" "Values(%s,%s,%s,%d,%d,%d,%d,%d,%d)")

flag1=0
topic=""
messagedata=None

while True:
	try:	
		string = subscriber.recv(flags=zmq.NOBLOCK)
		aname,adate,atime,aenmotors,apwml,apwmr,apwma1,apwm2,areport = string.split()
   		flag1=1

	except:
		flag1=0

	if flag1 == 0:
		pass
	else:
		curs.execute (query,aname,adate,atime,aenmotors,apwml,apwmr,apwma1,apwm2,areport)
   		db.commit()
   		print topic