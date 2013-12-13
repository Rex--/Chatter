import socket
import threading
from Tkinter import *

#==================================================================================================
class GUI():                                    #
#===============================================#
	def __init__(self, root):
		self._master = root
		grid = Grid()
		self._master.protocol("WM_DELETE_WINDOW", self._quit)
		self._scrollBar = Scrollbar(self._master)
		self._scrollBar.grid(row=2, column=4, sticky=N+S)
		self._textbox = Text(self._master, height=20, width=50, state=DISABLED, yscrollcommand=self._scrollBar.set)
		self._textbox.grid(row=2, column=1, columnspan=3, sticky=N+E+S+W)
		self._scrollBar.config(command=self._textbox.yview)
		self._sendButton = Button(self._master, text='Send', fg='blue', command=self._Send_Message)
		self._sendButton.grid(row=3, column=1, sticky=N+E+S+W)
		self._message = StringVar()
		self._messageEntry = Entry(self._master, textvariable=self._message, width=35)
		self._messageEntry.grid(row=3, column=2, columnspan=2, sticky=N+E+S+W)
#================================================
	def display(self, string):
		self._textbox.config(state=NORMAL)
		self._textbox.insert(END, string + "\n")
		self._textbox.config(state=DISABLED)
#================================================
	def _Send_Message(self):
		print "Message: " + self._message.get()
		network.send(self._message.get())
		self._messageEntry.delete(0, END)
#================================================
	def _quit(self):
		network.send("QUIT")
		self._master.destroy()
#==================================================================================================


#==================================================================================================
class GetUsername():                            #
#===============================================#
	def __init__(self, root):
		self._master = root
		grid = Grid()
		self._ip = StringVar()
		self._ipEntry = Entry(self._master, textvariable=self._ip, width=16)
		self._ipEntry.grid(row=1, column=2)
		self._ipLabel = Label(self._master, text="IP: ")
		self._ipLabel.grid(row=1, column=1, sticky=E)
		self._port = IntVar()
		self._portEntry = Entry(self._master, textvariable=self._port, width=10)
		self._portEntry.grid(row=1, column=4)
		self._portLabel = Label(self._master, text="Port: ")
		self._portLabel.grid(row=1, column=3)
		self._username = StringVar()
		self._usernameEntry = Entry(self._master, textvariable=self._username, width=21)
		self._usernameEntry.grid(row=2, column=2, columnspan=2)
		self._usernameLabel = Label(self._master, text="Username: ")
		self._usernameLabel.grid(row=2, column=1)
		self._connectButton = Button(self._master, text="Connect", fg="blue", command = self._connect)
		self._connectButton.grid(row=2, column=4)
		self._status = Label(self._master, text="Status: Not Connected")
		self._status.grid(row=3, column=2, columnspan=2)
#================================================
	def _connect(self):
		print self._username.get() + "@" + self._ip.get() + ":" + str(self._port.get())
		network.connect(self._ip.get(), self._port.get(), self._username.get())
		network.start()
#================================================
	def set_status(self, status):
		self._stus = "Status: " + status
		self._status.config(text=self._stus)
#================================================
	def quit(self):
		self._master.destroy()
		mgroot = Tk()
		mainGUI = GUI(mgroot)
		mgroot.title("Chatter")
		mgroot.mainloop()
#==================================================================================================


#==================================================================================================
class Network(threading.Thread):                #
#===============================================#
	def __init__(self):
		threading.Thread.__init__(self)
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#================================================
	def connect(self, ip, port, username):
		self._ip = ip
		self._port = port
		self._username = username
		try:
			self._socket.connect((self._ip, self._port))
		except:
			print "Couldn't connect. Maybe this was meant to be?"
		self._socket.send(self._username)
		self._reply = self._socket.recv(1024)
		if self._reply == "0":
			getUsername.quit()
		else:
			getUsername.set_status("Username already taken")
#================================================
	def send(self, string):
		self._socket.send(string)
#================================================
	def run(self):
		while True:
			self._msg = self._socket.recv(1024)
			mgroot.display(self._msg)

#==================================================================================================


network = Network()
guroot = Tk()
getUsername = GetUsername(guroot)
guroot.title("Chatter")
guroot.mainloop()