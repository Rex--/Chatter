import socket
import threading
from Tkinter import *

Username = None


#==================================================================================================
 # gui class -- class that handles the gui and such
class gui():
#================================================
 # __init__ function -- accepts the root of a tkinter something I dont even know what I'm saying
	def __init__(self, root):
		self._master = root
		grid = Grid()

		# So when the [x] is pressed I can close my shit too
		self._master.protocol("WM_DELETE_WINDOW", self._quit)

		# Textbox with scroll bar
		self._scrollBar = Scrollbar(self._master)
		self._scrollBar.grid(row=1, column=4, sticky=N+S)
		self._textbox = Text(self._master, height=20, width=50, state=DISABLED, yscrollcommand=self._scrollBar.set)
		self._textbox.grid(row=1, column=1, columnspan=3, sticky=N+E+S+W)
		self._scrollBar.config(command=self._textbox.yview)

		# Send Button
		self._sendButton = Button(self._master, text='Send', fg='blue', command=self._Send_Message)
		self._sendButton.grid(row=2, column=1, sticky=N+E+S+W)

		#Entry to get the message
		self._message = StringVar() #Defining as a tkinter object variable
		self._messageEntry = Entry(self._master, textvariable=self._message, width=35)
		self._messageEntry.grid(row=2, column=2, columnspan=2, sticky=N+E+S+W)
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
		self._messageEntry.delete(0, END)
#================================================
	def Get_username(self):
		print "Not done yet but close"
 # _quit function -- takes no arguments, is called when the [x] is clicked on the gui. Makes sure everything stops gracefully
	def _quit(self):
		print "Stopping listener..."
		print "Stopping Sender..."
		self._master.destroy()
#==================================================================================================

#==================================================================================================
 # Network class -- Class that handles all network and server communication
class Network(threading.Thread):
#================================================
 # __init__ function -- takes a socket object as a argument and sets everything up 
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self._socket = socket
#================================================
 # connect function -- takes a port and ip and connects to it and works out the username situation
	def connect(self, port, ip):
		self._socket.connect((ip, port))
		if Username == None:
			Username = GUI.Get_username()
		self._socket.send(Username)
		wmsg = self._socket.recv(1024)
		GUI.display(wmsg)
#================================================
 # loop function -- the main listening loop. Listens for messages and then displays it 
	def loop(self):
		while True:
			msg = self._socket.recv(1024)
			GUI.display(msg)
#================================================
 # send function -- takes a string as argument and sends it off to the server
	def send(self, string):
		self._socket.send(string)
#==================================================================================================


root = Tk()
root.title("Chatter v0.02")
GUI = gui(root)
root.mainloop()