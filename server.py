#SERVER OBJECT FILE
import os
import sys
import time
import socket

import tkinter as tk
from pickle import Pickler, Unpickler

import encoding

class Server():
	def __init__(self, name=None, address=None, port=None):
		self.name = name
		self.address = address
		self.port = port
		self.connected = False

	def saveServer(self, absPath=None, saveDir=None, ext=None):
		if os.path.exists(saveDir) and not os.path.isfile(saveDir):
			os.chdir(saveDir)
		else:
			os.mkdir(saveDir)
			os.chdir(saveDir)
		with open(self.name + ext, 'wb') as newFile:
			pickler = Pickler(newFile)
			pickler.dump(self)
		os.chdir(absPath)

	def connectTo(self, serverName, serverInfos, client):
		client.server.name = serverName
		client.server.address = serverInfos[0]
		client.server.port = serverInfos[1]
		maxConnexionAttempts = 10
		success = False
		failed = 0
		#Client output
		client.gui.msgOutput.config(state='normal')
		client.gui.msgOutput.insert(tk.INSERT,
		'Trying to connect to ' + serverInfos[0] + ':' + str(serverInfos[1]) + '\n')
		client.gui.msgOutput.config(state='disabled')
		#Connection Loop
		while not self.connected and failed < maxConnexionAttempts:
			try:
				client.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client.socket.connect(serverInfos)
				self.connected = True
				client.gui.msgOutput.config(state='normal')
				client.gui.msgOutput.insert(tk.INSERT, 'Connexion Successful !\nWelcome <'
				+ client.username + '> !\n')
				client.gui.msgOutput.config(state='disabled')
			except:
				client.gui.msgOutput.config(state='normal')
				client.gui.msgOutput.insert(tk.INSERT, 'Connexion Failed...\n')
				client.gui.msgOutput.config(state='disabled')
				failed += 1
				time.sleep(1)
		if failed == maxConnexionAttempts:
			client.gui.msgOutput.config(state='normal')
			client.gui.msgOutput.insert(tk.INSERT, 'Connexion aborted : Too many failed attempts.\n')
			client.gui.msgOutput.config(state='disabled')
			return
		else:
			self.updateUsername(client.username, client.socket)
			client.gui.msgInput.bind('<KeyPress - Return>',
			lambda event : client.gui.callbacks.sendMsg(client.gui))
			client.gui.sendButton.configure(command= lambda : client.gui.callbacks.sendMsg(client.gui))
			client.threadList.createThread('listenServer')
			client.threadList.createThread('userList')

	def updateUsername(self, username, socket):
		update = "rename(" + username + ")"
		socket.send(encoding.encode_cmd(update))

def getServerList(client):
	serverList = []
	if os.path.exists(client.saveDir) and not os.path.isfile(client.saveDir):
		os.chdir(client.saveDir)
	else:
		os.mkdir(client.saveDir)
		os.chdir(client.saveDir)
	dirContent = os.listdir(os.getcwd())
	for srvFile in dirContent:
		if len(srvFile) >= 5 and srvFile[len(srvFile) - len(client.ext):] == client.ext:
			with open(srvFile, 'rb') as srv:
				depickler = Unpickler(srv)
				server = depickler.load()
			serverList.append(server)
	os.chdir(client.absPath)
	return serverList

