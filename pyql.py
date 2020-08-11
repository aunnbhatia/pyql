import prettytable 
import mysql.connector
from tkinter import *
from pandas import DataFrame as pdf
import time

def linebreak():
	res.insert(END,"\n\t\t------------------xxx------------------\n")
def dbtable(n):
	return prettytable.from_db_cursor(n)

def connectServer():
	global host, user, passwd, myconn, cur
	hostname = host_ent.get()
	username = user_ent.get()
	password = pass_ent.get()
	try:
		myconn = mysql.connector.connect(host = hostname, user = username, passwd = password)
		msg = f"Connected to {hostname} as {username}."
		disconn_btn = Button(m, text="Disconnect", width=12, command=disconnectServer)
		clear_btn = Button(m, text="Clear Screen", width=12, command=clearscr)
		disconn_btn.place(x=510,y=25)
		clear_btn.place(x=610,y=25)

	except:
		msg = "Unable to Connect to Server."
	res.insert(END,msg)
	linebreak()


def selectQuery():
	res.insert(END, "\n")
	query = str(slct_ent.get())
	try:
		cur = myconn.cursor()
		cur.execute(query)
		res.insert(END, dbtable(cur))
	except mysql.connector.errors.ProgrammingError:
		res.insert(END, "You have an error in your SQL syntax\n")
	except:
		res.insert(END,"Unable to search your Query. Try logging in again!\n")


def execute():
	res.insert(END, "\n")
	query = str(dl_ent.get())
	cur = myconn.cursor()
	cur.execute(query)
	res.insert(END, 'Status: Done')

def showDatabases():
	clearpnl()
	try:
		cur = myconn.cursor()
		cur.execute("show databases;")
		dt.insert(END,dbtable(cur))
	except:
		dt.insert(END,"Not Logged in Yet.\n")


def showTables():
	clearpnl()
	try:
		cur = myconn.cursor()
		cur.execute("show tables;")
		dt.insert(END,dbtable(cur))
	except:
		dt.insert(END,"Please Select a Database first.\n")


def disconnectServer():
	myconn.disconnect()
	res.insert(END,'\nDisconnected from Server. Thanks For Using PyQL\n')
	linebreak()


def clearscr():
	res.delete('1.0',END)

def clearpnl():
	dt.delete('1.0',END)

#GUI
m = Tk()
m.title('PyQL | Python Based MySQL Client')
m.minsize(height=600, width=1000)
m.tk.call('wm', 'iconphoto', m._w, PhotoImage(file='icon.png'))
host_lbl = Label(m, text="Host")
host_ent = Entry(m, highlightcolor="steelblue", highlightthickness=1)
user_lbl = Label(m, text="Username")
user_ent = Entry(m, highlightcolor="steelblue", highlightthickness=1)
pass_lbl = Label(m, text="Password")
pass_ent = Entry(m, highlightcolor="steelblue", highlightthickness=1)
db_lbl = Label(m, text="Database")
db_ent = Entry(m, highlightcolor="steelblue", highlightthickness=1)
conn_btn = Button(m, text="Connect!", width=12, command=connectServer)

host_lbl.place(x=20, y=10)
host_ent.place(x=20, y=30)
user_lbl.place(x=150, y=10)
user_ent.place(x=150, y=30)
pass_lbl.place(x=280, y=10)
pass_ent.place(x=280, y=30)
conn_btn.place(x=410, y=25)

resfrm = LabelFrame(m, text="Query Results", width=400, height=600)
resfrm.place(x=20, y=60)
res = Text(resfrm, highlightcolor="steelblue", highlightthickness=1,
	selectbackground="royalblue")
res.pack(side="left", padx=4,pady=4)
scr=Scrollbar(resfrm, orient=VERTICAL, command=res.yview)
scr.pack(side="left", fill=Y, padx = 10)

inpfrm1 = LabelFrame(m, text="Select Query", width=800, height=60)
inpfrm1.place(x=20, y=480)
slct_ent = Entry(inpfrm1, width=95, font=("",12,""), highlightcolor="steelblue", highlightthickness=1)
slct_ent.pack(side="left", pady=4, padx=4)
slct_btn = Button(inpfrm1, text="Select", width=12, command=selectQuery)
slct_btn.pack(side="left", pady=4, padx=4)


inpfrm2 = LabelFrame(m, text="Insert, Update, Alter and Drop Query", width=800, height=60)
inpfrm2.place(x=20, y=540)
dl_ent = Entry(inpfrm2, width=95, font=("",12,""), highlightcolor="steelblue", highlightthickness=1)
dl_ent.pack(side="left", pady=4, padx=4)
dl_btn = Button(inpfrm2, text="Execute", width=12, command=execute)
dl_btn.pack(side="left", pady=4, padx=4)

dosfrm = LabelFrame(m, text="Databases and Tables", width=200, height=410)
dosfrm.place(x=680, y=60)
dt = Text(dosfrm, width=35, height=22, highlightcolor="steelblue", highlightthickness=1,
	selectbackground="royalblue")
dt.pack(padx=8, pady=4)
dos1 = Frame(dosfrm)
dos1.pack(fill=X)

dos_btn1 = Button(dos1, text="Show Databases", command=showDatabases)
dos_btn2 = Button(dos1, text="Show Tables", command=showTables)
dos_btn3 = Button(dos1, text="Clear Panel", command=clearpnl)
dos_btn1.pack(side="left", padx=4, pady=4)
dos_btn2.pack(side="left", padx=4, pady=4)
dos_btn3.pack(side="left", padx=4, pady=4)

m.mainloop()