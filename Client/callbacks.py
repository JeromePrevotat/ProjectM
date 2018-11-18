#CALLBACKS COMMANDS FILE

import tkinter as tk
import timeformat as tFormat

from tkinter import ttk, messagebox as mBox

import dialogBox
import encoding
from server import Server, getServerList

import bcrypt

import smsCode

class Callbacks():
	def __init__(self, ui):
		self.ui = ui

	def _quit(self):
		self.ui.root.quit()
		self.ui.root.destroy()
		exit()

	def keyPress_Return(self, _event=None):
		if (type(self.ui.mainFrame.focus_get()) == tk.Button
		and self.ui.mainFrame.focus_get().config()['command'] != ''):
			self.ui.mainFrame.focus_get().invoke()
		else:
			self.ui.logInButton.invoke()

	def sendMsg(self, ui):
		msg = ui.msgInput.get(1.0, tk.END)
		if msg != '' and msg != '\n':
			encoded_msg = encoding.encode_msg(msg)
			ui.client.socket.send(encoded_msg)
			ui.msgInput.delete(1.0, tk.END)
			self.ui.msgOutput.config(state='normal')
			self.ui.msgOutput.insert(tk.INSERT,'You at ' + tFormat.get_time_format(self.ui) + ' :\n\t' + msg + '\n')
			self.ui.msgOutput.config(state='disabled')
		return 'break'

	def changePseudo(self):
		self.dialBox = dialogBox.Dialog(self.ui, 'changePseudo')

	def changePassword(self):
		self.dialBox = dialogBox.Dialog(self.ui, 'changePassword')

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
			dialbox.cancel(dialbox)
		#PERSONNAL INFORMATIONS
		#PSEUDO CHANGE
		if dialbox.bodyType == 'changePseudo':
			if self.ui.client.dbcom.identify(dialbox.oldPseudoStr.get(), dialbox.passwordStr.get()):
				if len(dialbox.newPseudoStr.get()) >= 4:
					if self.ui.client.dbcom.checkUsername(dialbox.newPseudoStr.get()):
						self.ui.client.dbcom.update_username(dialbox.oldPseudoStr.get(), dialbox.newPseudoStr.get())
						mBox.showinfo(self.ui.res.pseudoChanged, self.ui.res.pseudoChanged)
						dialbox.cancel(dialbox)
					else:
						dialbox.outputLabel.configure(text=self.ui.res.pseudoTaken, fg='red')
				else:
					dialbox.outputLabel.configure(text=self.ui.res.pseudoTooShort, fg='red')
			else:
				dialbox.outputLabel.configure(text=self.ui.res.badNamePassCombo, fg='red')
		#PASSWORD CHANGE
		if dialbox.bodyType == 'changePassword':
			if self.ui.client.dbcom.identify(dialbox.usernameStr.get(), dialbox.oldPasswordStr.get()):
				if dialbox.newPasswordStr1.get() == dialbox.newPasswordStr2.get():
					if len(dialbox.newPasswordStr1.get()) >= 4:
						new_salt = bcrypt.gensalt()
						while(not self.ui.client.dbcom.checkSalt(new_salt)):
							new_salt = bcrypt.gensalt()
						new_password = bcrypt.hashpw(dialbox.newPasswordStr1.get().encode(), new_salt)
						self.ui.client.dbcom.update_password(dialbox.usernameStr.get(), new_salt, new_password)
						mBox.showinfo(self.ui.res.passwordChanged, self.ui.res.passwordChanged)
						dialbox.cancel(dialbox)
					else:
						dialbox.outputLabel.configure(text=self.ui.res.passwordTooShort, fg='red')
				else:
					dialbox.outputLabel.configure(text=self.ui.res.passwordNonIdentical, fg='red')
			else:
				dialbox.outputLabel.configure(text=self.ui.res.badNamePassCombo, fg='red')

		#CONNECT TO SERVER
		if dialbox.bodyType == 'connect':
			serverName = dialbox.serverNameEntry.get()
			serverAddress = dialbox.addressEntry.get()
			serverPort = dialbox.portEntry.get()
			if (serverName != "" and
			serverAddress != "" and
			serverPort != "" and
			self.ui.client.username is not None and
			self.ui.client.username != ''):
				self.ui.client.server.connectTo(serverName, (serverAddress, int(serverPort)), self.ui.client)
				dialbox.cancel(dialbox)
			else:
				mBox.showwarning(self.ui.res.serverConnectEmptyTitle, self.ui.res.serverConnectEmptyMsg)

	def serverConnect(self):
		self.dialBox = dialogBox.Dialog(self.ui, 'connect')

	def askCode(self):
		"""Send then Ask the user for the Confirmation Code sent by SMS."""
		#Send the Confirmation Code
		correctCode = smsCode.sendCode(self.ui.numberStr.get())
		#Clean the UI
		self.ui.usernameLabel.grid_remove()
		self.ui.usernameEntry.grid_remove()
		self.ui.passwordLabel.grid_remove()
		self.ui.passwordEntry.grid_remove()
		self.ui.mailLabel.grid_remove()
		self.ui.mailEntry.grid_remove()
		self.ui.numberLabel.grid_remove()
		self.ui.numberEntry.grid_remove()
		#Confirmation Code Field
		self.ui.confirmationCodeStr = tk.StringVar()
		self.ui.confirmatioCodeLabel = tk.Label(self.ui.infosFrame, text=self.ui.res.confirmationCode, pady=5)
		self.ui.confirmationCodeEntry = tk.Entry(self.ui.infosFrame, textvariable=self.ui.confirmationCodeStr)
		self.ui.confirmatioCodeLabel.grid(row=0, column=0)
		self.ui.confirmationCodeEntry.grid(row=1, column=0)
		#Output Label
		self.ui.outputLabel = tk.Label(self.ui.infosFrame)
		self.ui.outputLabel.grid(row=2, column=0)
		#Confirm command
		self.ui.logInButton.config(text=self.ui.res.done,
		command= lambda : self.confirmCode(correctCode))

	def confirmCode(self, correctCode):
		if self.ui.confirmationCodeStr.get() == correctCode:
			self.newUser()
		else:
			self.ui.outputLabel.configure(text='Wrong Code',fg='red')

	def newUser(self):
		username = self.ui.usernameEntry.get()
		salt = bcrypt.gensalt()
		while(not self.ui.client.dbcom.checkSalt(salt)):
			salt = bcrypt.gensalt()
		password = bcrypt.hashpw(self.ui.passwordEntry.get().encode(), salt)
		email = self.ui.mailEntry.get()
		if self.ui.client.dbcom.checkUsername(username) and self.ui.client.dbcom.checkMail(email):
			self.ui.client.dbcom.add_user(username, salt, password, email)
			self.ui.buildLogInUI()

	def logIn(self):
		username = self.ui.usernameEntry.get()
		password = self.ui.passwordEntry.get()
		if self.ui.client.dbcom.identify(username, password):
			self.ui.client.username = username
			self.ui.buildMainUI()
		else:
			self.ui.errorLabel.config(text=self.ui.res.badNamePassCombo)