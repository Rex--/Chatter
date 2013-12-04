import socket
from Tkinter import *


#class gui():
#==================================================================================================
# Setting up the gui
#	def __init__(self, master):
#
#		grid = Grid()
#
#		# Textbox with scroll bar
#		self._scrollBar = Scrollbar(master)
#       self._scrollBar.grid(row=1, column=4, sticky=N+S)
#        self._textbox = Text(master, height=20, width=50, state=DISABLED, yscrollcommand=self._scrollBar.set)
#        self._textbox.grid(row = 1, column=1, columnspan=3, sticky=N+E+S+W)
#       self._scrollBar.config(command=self._textbox.yview)
#
 #       # Send Button
  #      self._sendButton = Button(master, text='Send', fg='blue', command=self._Send_Message) #Command sends the message
 #       self._sendButton.grid(row=2, column=1, sticky=N+E+S+W)
#
  #      #Entry to get the message
   #     self._message = StringVar() #Defining as a tkinter object variable
   #     self._messageEntry = Entry(master, textvariable=self._message, width=35)
  #      self._messageEntry.grid(row=2, column=2, columnspan=2, sticky=N+E+S+W)
#
#        # Quit button
#        self._quitButton = Button(master, text="Quit", fg='red', command=self._quit)
  #      self._quitButton.grid(row=3, column=3, sticky=E+N+S)
#==================================================================================================

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 1337))
s.send("Rex")
print s.recv(1024)

while True:
	s.send(raw_input("> "))
	print s.recv(1024)