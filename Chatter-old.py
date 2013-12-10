import socket
import threading
from Tkinter import *
#############################################
# You may and should change these variables #
Username = "Rex"
ip = "localhost"
port = 1337
#############################################

#==================================================================================================
 # Evaluate function -- 
def Evaluate(message):
	mList = message.split()
	if mList[0] == "MSG":
		# normal message
		GUI.display(mList[1] + ": " + mList[2])
	elif mList[0] == "PMSG":
		# Private message
		GUI.display("PM: " + mList[1] +  ": " + mList[2])
	else:
		# This should never be used but in dev
		GUI.display("ERROR: Unknown command: " + mList[0])
#==================================================================================================

#==================================================================================================
 # gui class -- class that handles the gui and such
class gui():
#================================================
 # __init__ function -- accepts the root of a tkinter something I dont even know what I'm saying
	def __init__(self, root):
		self._master = root
		grid = Grid()

		global Username
		global port
		global ip

		# So when the [x] is pressed I can close my shit too
		self._master.protocol("WM_DELETE_WINDOW", self._quit)

		# Entry to get the server ip
		self._ip = StringVar()
		self._ipEntry = Entry(self._master, textvariable=self._ip)
		self._ipEntry.grid(row=1, column=2)
		# Labeling the entry
		self._ipLabel = Label(self._master, text="IP: ")
		self._ipLabel.grid(row=1, column=1)

		# Button to connect to the server
		self._connectButton = Button(self._master, text="Connect", fg="blue", command=self._connect)
		self._connectButton.grid(row=1, column=3)

		# Textbox with scroll bar
		self._scrollBar = Scrollbar(self._master)
		self._scrollBar.grid(row=2, column=4, sticky=N+S)
		self._textbox = Text(self._master, height=20, width=50, state=DISABLED, yscrollcommand=self._scrollBar.set)
		self._textbox.grid(row=2, column=1, columnspan=3, sticky=N+E+S+W)
		self._scrollBar.config(command=self._textbox.yview)

		# Send Button
		self._sendButton = Button(self._master, text='Send', fg='blue', command=self._Send_Message)
		self._sendButton.grid(row=3, column=1, sticky=N+E+S+W)

		#Entry to get the message
		self._message = StringVar() #Defining as a tkinter object variable
		self._messageEntry = Entry(self._master, textvariable=self._message, width=35)
		self._messageEntry.grid(row=3, column=2, columnspan=2, sticky=N+E+S+W)
#================================================
 # display function -- accepts a string as argument and writes the passed string and a newline to the main textbox
	def display(self, string):
		self._textbox.config(state=NORMAL)
		self._textbox.insert(END, string + "\n")
		self._textbox.config(state=DISABLED)
#================================================
 # _Send_Message function -- takes no arguments, gets the string from the tkinter str obj and sends it to the Sender.send() function
	def _Send_Message(self):
		print "Message: " + self._message.get()
		network.send("MSG " + Username + " " + self._message.get())
		self._messageEntry.delete(0, END)
#================================================
 # Get_username function -- takes no arguments, opens a toplevel widget to get a username from the user
	def Get_username(self):
		print "Get_username function"
		self._GUbox = Toplevel()
		self._username = StringVar()
		self._userEntry = Entry(self._GUbox, textvariable=self._username)
		self._userEntry.grid(row=1, column=1)
		self._okButton = Button(self._GUbox, text='Ok', command=self._closeGU)
		self._okButton.grid(row=1, column=2)
		return self._username.get()
#================================================
 # _closeGU function -- takes no arguments, is called when the Ok button is clicked. Just destroys the toplevel widget
	def _closeGU(self):
		self._GUbox.destroy()
#================================================
 # _connect function -- takes no arguments, is called when the Connect button is clicked. Connects to the server
	def _connect(self):
		print "Connecting to %s on port %i with username %s" %(ip, port, Username)
		network.connect(port, ip, Username)
		network.start()
#================================================
 # _quit function -- takes no arguments, is called when the [x] is clicked on the gui. Makes sure everything stops gracefully
	def _quit(self):
		try:
			network.send("QUIT")
			network.stop()
		except:
			pass
		self._master.destroy()
#==================================================================================================

#==================================================================================================
 # Network class -- Class that handles all network and server communication
class Network(threading.Thread):
#================================================
 # __init__ function -- takes a TCP! socket object as a argument and sets everything up 
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self._socket = socket
		self._loop = True
#================================================
 # connect function -- takes a port and ip and connects to it and works out the username situation
	def connect(self, port, ip, username):
		print "connect function"
		self._socket.connect((ip, port))
		if username == None:
			username = GUI.Get_username()
		self._socket.send(username)
		wmsg = self._socket.recv(1024)
		GUI.display(wmsg)
#================================================
 # run function -- the main listening loop. Listens for messages and then displays it 
	def run(self):
		print "run function in class Network"
		while self._loop == True:
			msg = self._socket.recv(1024)
			Evaluate(msg)
#================================================
 # send function -- takes a string as argument and sends it off to the server
	def send(self, string):
		self._socket.send(string)
#================================================
 # stop function -- takes no arguments, when called it sets loop to false making the loop quit on the next ?loop?
	def stop(self):
		self._loop = False
		self._socket.close()
#==================================================================================================

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
network = Network(socket)
root = Tk()
GUI = gui(root)
root.title("Chatter v0.02")
print "Starting gui.."
root.mainloop()