#Client File

import os
import sys
import socket
from os import path

from user import User
from queue import Queue, Empty
from ui import Gui
from server import Server, getServerList
from threads import Threads
from db_com import DBCom

import encoding

class Client():
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = Server()
		self.threadList = Threads(self)
		self.guiQueue = Queue()
		self.user = User('', '', None, '')
		self.gui = Gui(self)
		self.dbcom = DBCom(self)
		if getattr(sys, 'frozen', False):
			# frozen
			self.absPath = os.path.dirname(sys.executable)
		else:
			# unfrozen
			self.absPath = os.path.dirname(os.path.realpath(__file__))
		self.saveDir = './savedServers'
		self.ext = '.srv'
		os.chdir(self.absPath)
		self.serverList = getServerList(self)
		self.username = None

if __name__ == "__main__":
	client = Client()
	client.gui.root.mainloop()