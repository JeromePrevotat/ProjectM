#DIALOG BOX FILE
import os
import tkinter as tk
from tkinter import ttk, messagebox as mBox
from server import getServerList

class Dialog(tk.Toplevel):
	def __init__(self, ui, bodyType, title=None):
		self.ui = ui
		self.bodyType = bodyType
		tk.Toplevel.__init__(self, self.ui.root)
		#Associate with a parent window
		self.transient(self.ui.root)
		self.resizable(False, False)
		if title:
			self.title(title)
		self.parent = self.ui.root
		self.returnValue = None
		self.masterFrame = tk.Frame(self)
		self.initial_focus = self.bodyBuild()
		self.masterFrame.grid(row=0, column=0, padx=5, pady=5)
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" %	(self.ui.root.winfo_rootx() + 50,
									 self.ui.root.winfo_rooty() + 50))
		self.initial_focus.focus_get()
		########################################################################
		# THREAD UPDATE ENTRIES ON LISTBOX SELECTION                           #
		########################################################################
		if self.bodyType == 'manageServer' or self.bodyType == 'connect':
			self.ui.client.threadList.createThread(self.bodyType, self)
		#Wait for the dialogbox to be validated or closed
		self.wait_window(self)

	def bodyBuild(self):
		"""Method to create the Body of the DialogBox."""
		if self.bodyType == 'connect':
			self.body = self.buildConnect()
		if self.bodyType == 'manageServer':
			self.body = self.buildManageServer()
		if self.bodyType == 'add_server':
			self.body = self.buildAddServer()
		if self.bodyType == 'changePseudo':
			self.body = self.buildChangePseudo()
		if self.bodyType == 'changePassword':
			self.body = self.buildChangePassword()
		if self.bodyType == 'serverInfos':
			self.body = self.buildServerInfos()

	def buildManageServer(self):
		import manageServer
		manageServer.buildFrames(self)
		manageServer.fillServerListFrame(self)
		manageServer.fillServerInfosFrame(self)
		manageServer.fillButtonFrame(self)

	def buildConnect(self):
		import manageServer
		manageServer.buildFrames(self)
		manageServer.fillServerListFrame(self)
		manageServer.fillServerInfosFrame(self)
		#BUTTONS
		self.buttonDone = tk.Button(self.buttonFrame, text=self.ui.res.serverConnect, width=8,
		command= lambda : self.ui.callbacks.done(self))
		self.buttonDone.grid(row=1, column=1)
		self.buttonCancel = tk.Button(self.buttonFrame, text=self.ui.res.cancel, width=8,
		command= lambda : self.ui.callbacks.cancel(self))
		self.buttonCancel.grid(row=1, column=0)

	def buildChangePseudo(self):
		import changeUsername
		changeUsername.setVar(self)
		changeUsername.buildFrames(self)
		changeUsername.buildLabels(self)
		changeUsername.buildEntry(self)
		changeUsername.fillButtonFrame(self)

	def buildChangePassword(self):
		import changePass
		changePass.setVar(self)
		changePass.buildFrames(self)
		changePass.buildLabels(self)
		changePass.buildEntry(self)
		changePass.fillButtonFrame(self)

	def buildServerInfos(self):
		#SERVER NAME
		self.serverNameLabel = tk.Label(self.masterFrame, text=self.ui.res.serverNameLabel)
		self.serverNameLabel.grid(row=0, column=0, sticky='W')
		self.serverName = tk.StringVar()
		self.serverNameEntry = tk.Entry(self.masterFrame, textvariable=self.serverName,
		width=25, state='disabled')
		self.serverNameEntry.grid(row=0, column=1)
		#ADRESS
		self.adressLabel = tk.Label(self.masterFrame, text = self.ui.res.adressLabel)
		self.adressLabel.grid(row=1, column=0, sticky='W')
		self.server_adress = tk.StringVar()
		self.adressEntry = tk.Entry(self.masterFrame, textvariable = self.server_adress,
		width=25, state='disabled')
		self.adressEntry.grid(row=1, column=1)
		#PORT
		self.portLabel = tk.Label(self.masterFrame, text=self.ui.res.portLabel)
		self.portLabel.grid(row=2, column=0, sticky='W')
		self.port = tk.StringVar()
		self.portEntry = tk.Entry(self.masterFrame, textvariable=self.port,
		width=25, state='disabled')
		self.portEntry.grid(row=2, column=1)

	def cancel(self, event=None):
		self.parent.focus_set()
		self.destroy()