import socket
import threading
import ConfigParser
import os

Online_Users   = []
Client_Objects = []


#==================================================================================================
class Server():                                 #
#===============================================#
	def __init__(self, port):
		self._PORT = port
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#================================================
	def start(self):
		self._socket.bind(('', self._PORT))
		self._socket.listen(3)
		while True:
			self._client, self._address = self._socket.accept()
			self._handler = Client_Handler(self._client, self._address)
			self._handler.start()
#==================================================================================================


#==================================================================================================
class Sender(threading.Thread):                 #
#===============================================#
	def __init__(self, port):
		threading.Thread.__init__(self)
		self._port = port
		global Client_Objects
#================================================
	def all(self, string):
		self._message = string
		for self._client in Client_Objects:
			print self._client
			try:
				self._client.send(self._message)
			except:
				print "ERR: No Clients connected!"
#================================================
	def private(self, user, string):
		self._message = string
		self._clientobj = Get_Obj(user)
		self._clientobj.send(self._message)
#==================================================================================================


#==================================================================================================
class Client_Handler(threading.Thread):         #
#===============================================#
	def __init__(self, client, address):
		threading.Thread.__init__(self)
		self._clientobj = client
		print self._clientobj
		self._address = address
		global Online_Users
		global Client_Objects
#================================================
	def run(self):
		self._username = self._clientobj.recv(1024)
		if Allow_duplicate_usernames == False:
			while Check_Availability(self._username) == False:
				self._clientobj.send("1")
				self._username = self._clientobj.recv(1024)
		sender.all(self._username + " joined the channel.")
		Online_Users.append(self._username)
		Client_Objects.append(self._clientobj)
		self._clientobj.send("0")
		self._clientobj.send(Welcome_message)
		while True:
			self._message = self._clientobj.recv(1024)
			Evaluate(self._username, self._message, self._clientobj)
#==================================================================================================


#================================================
def Evaluate(username, message, clientobj):
	mList = message.split(".")
	if mList[0] == None:
		pass
	elif mList[0] == "PMSG":
		msg = "[PM]" + username + mList[2]
		sender.private(mList[2], msg)
	elif mList[0] == "QUIT":
		sender.all(username + " left the channel.")
	else:
		sender.all(username + ":" + message)
#================================================
def ParseConfig():
	config = ConfigParser.RawConfigParser()
	config.read("chatterd.conf")
	global PORT
	#global Operator_List
	global Allow_duplicate_usernames
	global Welcome_message
	PORT = config.getint("Server Settings", "port")
	#Operator_List = config.get("User Settings", "operators").split()
	Allow_duplicate_usernames = config.getboolean("User Settings", "Allow_duplicate_usernames")
	Welcome_message = config.get("Server Settings", "Welcome_message")
#================================================
def GenerateConfig():
	header = "# This config file was automatically generated with the default settings. Feel free to change any at all, but\n# keep the same types. In [User Settings] 'Operators' can be more than one username seperated by a space.\n\n"
	config = ConfigParser.RawConfigParser()
	config.add_section("Server Settings")
	config.set("Server Settings", "port", "1337")
	config.set("Server Settings", "Welcome_message", "Welcome to Chatter v0.2!")
	config.add_section("User Settings")
	#config.set("User Settings", "operators", "Administrator")
	config.set("User Settings", "Allow_duplicate_usernames", "False")
	with open("chatterd.conf", 'a') as confFile:
		confFile.write(header)
		config.write(confFile)
#================================================
def Check_Availability(username):
	if username in Online_Users:
		return False
	else:
		return True
#================================================
def Get_Obj(username):
	index = Online_Users.index(username)
	return Client_Objects[index]
#================================================

if not os.path.exists("chatterd.conf"):
	GenerateConfig()
ParseConfig()
server = Server(PORT)
sender = Sender(PORT)
server.start()