#CALLBACKS COMMANDS FILE

import tkinter as tk
import timeformat as tFormat

from tkinter import ttk, messagebox as mBox

import dialogBox
from server import Server, getServerList

class Callbacks():
	def __init__(self, ui):
		self.ui = ui

	def sendMsg(self, ui):
		msg = ui.msgInput.get(1.0, tk.END)
		if msg != '':
			ui.client.socket.send(msg.encode())
			ui.msgInput.delete(1.0, tk.END)
			self.ui.msgOutput.config(state='normal')
			self.ui.msgOutput.insert(tk.INSERT,'You at ' + tFormat.get_time_format(self.ui) + ' :\n\t' + msg + '\n')
			self.ui.msgOutput.config(state='disabled')
		return 'break'

	def profile(self):
		self.dialBox = dialogBox.Dialog(self.ui, 'personal_informations')

	def serverInfos(self):
		self.dialBox = dialogBox.Dialog(self.ui, 'serverInfos')

	def manageServer(self):
		self.dialBox = dialogBox.Dialog(self.ui, 'manageServer')

	def add(self, dialbox):
		dialbox.serverNameEntry.config(state='normal')
		dialbox.addressEntry.config(state='normal')
		dialbox.portEntry.config(state='normal')

	def edit(self, dialbox):
		dialbox.serverNameEntry.config(state='normal')
		dialbox.addressEntry.config(state='normal')
		dialbox.portEntry.config(state='normal')

	def cancel(self, dialbox):
		dialbox.parent.focus_set()
		dialbox.destroy()

	def done(self, dialbox):
		#SERVERS MANAGEMENT
		if dialbox.bodyType == 'manageServer':
			serverName = dialbox.serverNameEntry.get()
			serverAddress = dialbox.addressEntry.get()
			serverPort = dialbox.portEntry.get()
			if serverName and serverAddress and serverPort:
				for server in self.ui.client.serverList:
					if server.name == serverName or server.address == serverAddress:
						print('DUPLICATE')
						return
				newServer = Server(serverName, serverAddress, serverPort)
				Server.saveServer(newServer, self.ui.client.absPath,
				self.ui.client.saveDir, self.ui.client.ext)
				#ADD NEW SERVER TO SERVERLIST
				self.ui.client.serverList.append(newServer)
				#ADD NEW SERVER TO LISTBOX
				dialbox.serverListbox.insert(tk.END, serverName)
			dialbox.serverNameEntry.delete(0, tk.END)
			dialbox.addressEntry.delete(0, tk.END)
			dialbox.portEntry.delete(0, tk.END)
			dialbox.serverNameEntry.config(state='disabled')
			dialbox.addressEntry.config(state='disabled')
			dialbox.portEntry.config(state='disabled')
		#PERSONNAL INFORMATIONS
		if dialbox.bodyType == 'personal_informations':
			if len(dialbox.pseudoStr.get()) >= 5:
				self.ui.client.username = dialbox.pseudoStr.get()
			else:
				mBox.showwarning(self.ui.res.pseudoWarningTitle, self.ui.res.pseudoWarningMsg)
		#CONNECT TO SERVER
		if dialbox.bodyType == 'connect':
			serverName = dialbox.serverNameEntry.get()
			serverAddress = dialbox.addressEntry.get()
			serverPort = dialbox.portEntry.get()
			if (serverName is not None and
			serverAddress is not None and
			serverPort is not None and
			self.ui.client.username is not None and
			self.ui.client.username != ''):
				self.ui.client.server.connectTo(serverName, (serverAddress, int(serverPort)), self.ui.client)
		dialbox.cancel(dialbox)

	def serverConnect(self):
		self.dialBox = dialogBox.Dialog(self.ui, 'connect')

	def newUser(self):
		username = self.ui.usernameEntry.get()
		password = self.ui.passwordEntry.get()
		email = self.ui.mailEntry.get()
		if self.ui.client.dbcom.checkUsername(username) and self.ui.client.dbcom.checkMail(email):
			self.ui.client.dbcom.add_user(username, password, email)
			self.ui.buildLogInUI()

	def logIn(self):
		username = self.ui.usernameEntry.get()
		password = self.ui.passwordEntry.get()
		if self.ui.client.dbcom.identify(username, password):
			self.ui.client.username = username
			self.ui.buildMainUI()
		else:
			self.ui.errorLabel.config(text=self.ui.res.badNamePassCombo)