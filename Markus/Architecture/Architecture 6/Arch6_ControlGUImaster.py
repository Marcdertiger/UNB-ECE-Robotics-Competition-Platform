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
#if robot has timed out, make it's name field red with white text.
                if data[8] == "100":
                    namebox.itemconfig(i,bg='red',fg='white')
                else:
                    namebox.itemconfig(i,bg='white',fg='black')

                count = count + 1


#This will modify the command line that should be active (adds a "1" into the request field of the new command)
def writeCommandDB():
    dbc = MySQLdb.connect(host ="localhost", user = "root", passwd = "energySHOULDERreally03", db = "Controller")
    masterDB=dbc.cursor()
    masterDB.execute("DELETE FROM masterControl")
    masterDB.execute ("""INSERT INTO masterControl(ID,drive,aux,special1,special2,report,request) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(IDe,drivee,auxe,special1e,special2e,reporte,requeste))
    dbc.commit()
    masterDB.close()
    dbc.close()
 
def commit():
    global reporte
    global special1e
    global requeste
    
    vari = robotnumber.get()
    spc1 = spec1.get()
    
    if vari != "":
        reporte=vari
    elif vari == "":
        reporte = "60"
        
    if requeste == "5":
        if spc1 != "":
            special1e = spc1
    
    
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
    
#DO NOT LEAVE ANY FIELD EMPTY OR WITH A SPACE!!!!!!
    #USE REPORT = 100 FOR RESET FUNCTION, REPORT CANNOT BE ZERO!!!
    
    if selection == "1":
        IDe = "1"
        drivee = "1"
        auxe = "0"
        special1e = "0"
        special2e = "0"
        
        requeste = "4"
   
    if selection == "2":
        IDe = "1"
        drivee = "0"
        auxe = "0"
        special1e = "0"
        special2e = "0"
        
        requeste = "4"
        
    if selection == "3":
        IDe = "1"
        drivee = "1"
        auxe = "0"
        special1e = "0"
        special2e = "0"
        
        requeste = "5"
    
    
    return 


#DO NOT LEAVE A SPACE BETWEEN = AND 1. DO THIS : "VALUE=1" NOT THIsleS :"VALUE= 1"
playMode1=Radiobutton(window,text="Start Robot/s",variable=var,value=1,command = selectRB).pack()
playMode2=Radiobutton(window,text="Stop Robot/s",variable=var,value=2,command = selectRB).pack()
playMode3=Radiobutton(window,text="Slow Down",variable=var,value=3,command = selectRB).pack()
playMode4=Radiobutton(window,text="Play Game 1",value=4,variable=var,command = selectRB).pack()
playMode5=Radiobutton(window,text="Play Game 2",value=5,variable=var,command = selectRB).pack()
playMode6=Radiobutton(window,text="RESET",value=6,variable=var,command = selectRB).pack()

robno =Label(window, text = "Robot number (1..16), empty for all.") #better would be use "60" for all and disable default empty (reduce human error)
robno.pack(side = LEFT)
robotnumber = Entry(window)
robotnumber.pack(side = LEFT)

labspc1 =Label(window, text = "Special value 1.")
labspc1.pack(side = RIGHT)
spec1 = Entry(window)
spec1.pack(side = RIGHT)

commitB = Tkinter.Button(window,bg='green',text="Commit",command = commit,cursor="circle")
commitB.pack()


label2 = Label(window,anchor = CENTER, text = "Name   Date   Time   ENmotors   PWM L   PWM R   AUX PWM 1   AUX PWM 2   Report")
label2.pack()
                
namebox = Listbox(window,selectmode=SINGLE,width=10,height=16)
datebox = Listbox(window,selectmode=SINGLE,width=10,height=16)
ctimebox = Listbox(window,selectmode=SINGLE,width=10,height=16)
enmotorsbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwmlbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwmrbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwma1box = Listbox(window,selectmode=SINGLE,width=4,height=16)
pwma2box = Listbox(window,selectmode=SINGLE,width=4,height=16)
reportbox = Listbox(window,selectmode=SINGLE,width=4,height=16)
                   



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




