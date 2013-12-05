import socket
import threading




#######################
### Config Messages ###
Welcome_Message = "Welcome to v0.2 of Chatter-- a client-server relationship."
Username_Taken  = "That username is already in use! Please try another."
Unknown_Command = "Unknown Command"
Not_OP          = "You don't have permsission for that."
Goodbye         = "Goodbye!"




# Name will be in the same place as the object [Hopefully]
Online_Users   = []
Client_Objects = []

OP_List = ["Administrator"]

#==================================================================================================
 # Check_Availability function -- checks if username is already in use, if it is not available returns false, if it is returns true
def Check_Availability(username):
	if username in Online_Users:
		return False
	else:
		return True
#==================================================================================================

#==================================================================================================
 # Evaluate function -- takes a username, string, and socket object as arguments and evals the string and does what it needs to
def Evaluate(user, string, sockobj):
	mList = string.split()
	if mList[0] == "MSG":
		#Normal global message
		sender.all(string)
		print string
	elif mList[0] == "PMSG":
		#Private message
		sender.private(mList[1], "PMSG" + mList[2])
	elif mList[0] == "BAN":
		# Ban a user forever(Or until they get smart ;)
		sender.private(mList[1], "BAN" + mList[2])
	elif mList[0] == "KICK":
		# Kick a user. They can reconnect immediatly
		sender.private(mList[1], "KICK" + mList[2])
	elif mList[0] == "OP":
		# Promotes a user to operator status
		if CheckOP(user):
			OP_List.append(mList[1])
		else:
			sender.private(user, Not_OP)
	elif mList[0] == "QUIT":
		# Message recieved when they close out of chatter
		sender.private(user, Goodbye)
		print "%s closed the client!" %user
		sockobj.close()
		Online_Users.remove(user)
		Client_Objects.remove(sockobj)

	else:
		# unknown command
		sender.private(user, Unknown_Command + mList[0])
#==================================================================================================

#==================================================================================================
 # CheckOP function -- checks to see if user is an op. If so returns true, if not returns false
def CheckOP(user):
	if user in OP_List:
		return True
	else:
		return False
#==================================================================================================

#==================================================================================================
 # GetObj function -- accepts a username for input, returns the socket_obj for that username. Returns False if username does not exist
def GetObj(user):
	index = Online_Users.index(user)
	return Client_Objects[index]
#==================================================================================================

#==================================================================================================
# Server class -- Listens for connections and when there is one it passes the client obj and address to the client handler to handle messages
class Server():
#================================================
	# Defining stuff
	def __init__(self, port):
		self._PORT = port
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#================================================
	# main loop
	def start(self):
		self._socket.bind(('', self._PORT))
		self._socket.listen(3)
		while True:
			self._client, self._address = self._socket.accept()
			self._handler = Client_Handler(self._client, self._address)
			self._handler.start()
#==================================================================================================

#==================================================================================================
 # Client_Handler class -- gets passed the client obj and address and then listens for messages
class Client_Handler(threading.Thread):	
#================================================
 # Just defining some variables
	def __init__(self, client, address):
		threading.Thread.__init__(self)
		self._clientOBJ = client
		self._address = address
#================================================
	# main func
	def run(self):
		self._username = self._clientOBJ.recv(1024)
		while Check_Availability(self._username) == False:
			self._clientOBJ.send(Username_Taken)
			self._username = self._clientOBJ.recv(1024)
		Online_Users.append(self._username)
		Client_Objects.append(self._clientOBJ)
		self._clientOBJ.send(Welcome_Message)
		# Main loooop!
		while True:
			self._message = self._clientOBJ.recv(1024)
			Evaluate(self._username, self._message, self._clientOBJ)
#==================================================================================================

#==================================================================================================
# Sender class -- Handles all sending whether it be a private message or just a normal message
class Sender(threading.Thread):
#================================================
	# defining start variables
	def __init__(self, port):
		threading.Thread.__init__(self)
		self._PORT = port
#================================================
	# Function to send a message to all current online users
	def all(self, message):
		self._message = message
		for self._obj in Client_Objects:
			self._obj.send(message)
#================================================
	# Function to send a message to a specific user
	def private(self, user, message):
		self._user = user
		self._message = message
		self._obj = GetObj(self._user)
		self._obj.send(self._message)
#==================================================================================================
server = Server(1337)
sender = Sender(1337)
server.start()