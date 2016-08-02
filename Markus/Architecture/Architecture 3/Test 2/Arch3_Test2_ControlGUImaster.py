#written by : Marc-Andre Couturier
#Summer of 2016

#!/usr/bin/python

import Tkinter
from Tkinter import *
import sys
import MySQLdb
import MySQLdb.cursors
import time
from time import sleep



dbc = MySQLdb.connect(host ="localhost", user = "root", passwd = "energySHOULDERreally03", db = "Controller")
masterDB=dbc.cursor()

#Init global variables
IDe = ""
drivee = ""
auxe = ""
special1e = ""
special2e = ""
reporte = ""
requeste = ""

#Init GUI

window=Tkinter.Tk()
var = IntVar()

label=Label(window)
label.pack()

# This reads the database, removes old entries and inserts new entries.
def readStatusDB():
    dbs = MySQLdb.connect(host ="localhost", user = "root", passwd = "energySHOULDERreally03", db = "Controller")
    statusDB=dbs.cursor()
    statusDB.execute("SELECT * from status")
    count = 1

    namebox.delete(0,END)
    datebox.delete(0,END)
    ctimebox.delete(0,END)
    enmotorsbox.delete(0,END)
    pwmlbox.delete(0,END)
    pwmrbox.delete(0,END)
    pwma1box.delete(0,END)
    pwma2box.delete(0,END)
    reportbox.delete(0,END)
    
    for i in range(statusDB.rowcount):
              
                data = statusDB.fetchone()
                
                namebox.insert(count,data[0])
                datebox.insert(count,data[1])
                ctimebox.insert(count,data[2])
                enmotorsbox.insert(count,data[3])
                pwmlbox.insert(count,data[4])
                pwmrbox.insert(count,data[5])
                pwma1box.insert(count,data[6])
                pwma2box.insert(count,data[7])
                reportbox.insert(count,data[8])

                count = count + 1

#This will modify the command line that should be active (adds a "1" into the request field of the new command)
def writeCommandDB():

   masterDB.execute("DELETE FROM masterControl")
   masterDB.execute ("""INSERT INTO masterControl(ID,drive,aux,special1,special2,report,request) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(IDe,drivee,auxe,special1e,special2e,reporte,requeste))
   dbc.commit() 
 
def commit():
    writeCommandDB()
    return

def selectRB():
    global IDe
    global drivee
    global auxe
    global special1e
    global special2e
    global reporte
    global requeste

    selection = str(var.get())
    label.config(text = selection)

    if selection == "1":
        IDe = "1"
        drivee = "1"
        auxe = " "
        special1e = " "
        special2e = " "
        reporte = "60"
        requeste = "4"
   
    else:
        IDe = "0"
        drivee = "0"
        auxe = "0"
        special1e = "0"
        special2e = "0"
        reporte = "0"
        requeste = "0"
    
    return 



playMode1=Radiobutton(window,text="Start All Robots",variable=var,value= 1,command = selectRB).pack()
playMode2=Radiobutton(window,text="Stop All Robots",variable=var,value= 2,command = selectRB).pack()
playMode3=Radiobutton(window,text="Play Game 1",variable=var,value= 3,command = selectRB).pack()
playMode4=Radiobutton(window,text="Play Game 2",value= 4,variable=var,command = selectRB).pack()
playMode5=Radiobutton(window,text="Play Game 3",value= 5,variable=var,command = selectRB).pack()
playMode6=Radiobutton(window,text="RESET",value= 6,variable=var,command = selectRB).pack()

                
namebox = Listbox(window,selectmode=SINGLE,width=10,height=16)
datebox = Listbox(window,selectmode=SINGLE,width=10,height=16)
ctimebox = Listbox(window,selectmode=SINGLE,width=10,height=16)
enmotorsbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwmlbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwmrbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwma1box = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwma2box = Listbox(window,selectmode=SINGLE,width=4,height=16)
reportbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
                   

commitB = Tkinter.Button(window,bg='green',text="Commit",command = commit,cursor="circle")
commitB.pack()


namebox.pack(side=LEFT)
datebox.pack(side=LEFT)
ctimebox.pack(side=LEFT)
enmotorsbox.pack(side=LEFT)
pwmlbox.pack(side=LEFT)
pwmrbox.pack(side=LEFT)
pwma1box.pack(side=LEFT)
pwma2box.pack(side=LEFT)
reportbox.pack(side=LEFT)


#This is the main loop!

while True:

    readStatusDB()
   
    window.update()

window.mainloop()




