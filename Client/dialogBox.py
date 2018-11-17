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
		#MANAGE FRAME
		self.manageFrame = tk.Frame(self.masterFrame)
		self.manageFrame.grid(row=0, column=0)
		#SERVER LIST FRAME
		self.serverListFrame = tk.Frame(self.manageFrame)
		self.serverListFrame.grid(row=0, column=0)
		#LISTBOX
		self.serverListbox = tk.Listbox(self.serverListFrame, selectmode ='single',
		height=20)
		#ADD ALL SERVER SAVED TO LISTBOX
		for srv in self.ui.client.serverList:
			self.serverListbox.insert(tk.END, srv.name)
		self.serverListbox.grid(row=0, column=0, rowspan=6)
		#SERVER INFOS FRAME
		self.serverInfosFrame = tk.Frame(self.manageFrame)
		self.serverInfosFrame.grid(row=0, column=1, sticky='N')
		#SERVER NAME
		self.serverNameLabel = tk.Label(self.serverInfosFrame, text=self.ui.res.serverNameLabel)
		self.serverNameLabel.grid(row=0, column=1, sticky='W', padx=5)
		self.serverName = tk.StringVar()
		self.serverNameEntry = tk.Entry(self.serverInfosFrame, textvariable=self.serverName,
		width=25, state='disabled')
		self.serverNameEntry.grid(row=1, column=1, padx=5)
		#ADDRESS
		self.adressLabel = tk.Label(self.serverInfosFrame, text = self.ui.res.adressLabel)
		self.adressLabel.grid(row=2, column=1, sticky='W', padx=5)
		self.server_address = tk.StringVar()
		self.addressEntry = tk.Entry(self.serverInfosFrame, textvariable = self.server_address,
		width=25, state='disabled')
		self.addressEntry.grid(row=3, column=1, padx=5)
		#PORT
		self.portLabel = tk.Label(self.serverInfosFrame, text=self.ui.res.portLabel)
		self.portLabel.grid(row=4, column=1, sticky='W', padx=5)
		self.port = tk.StringVar()
		self.portEntry = tk.Entry(self.serverInfosFrame, textvariable=self.port,
		width=25, state='disabled')
		self.portEntry.grid(row=5, column=1, padx=5)
		#BUTTON FRAME
		self.buttonFrame = tk.Frame(self.manageFrame)
		self.buttonFrame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
		self.addButton = tk.Button(self.buttonFrame, text=self.ui.res.addserver,
		width=10, command=lambda : self.ui.callbacks.add(self))
		self.addButton.grid(row=0, column=0)
		self.delButton = tk.Button(self.buttonFrame, text=self.ui.res.delete,
		width=10)
		self.delButton.grid(row=0, column=1)
		self.editButton = tk.Button(self.buttonFrame, text=self.ui.res.edit,
		width=10, command=lambda : self.ui.callbacks.edit(self))
		self.editButton.grid(row=0, column=2)
		self.doneButton = tk.Button(self.buttonFrame, text=self.ui.res.done,
		width=10, command=lambda : self.ui.callbacks.done(self))
		self.doneButton.grid(row=0, column=3)
		self.cancelButton = tk.Button(self.buttonFrame, text=self.ui.res.cancel,
		width=10, command= lambda : self.ui.callbacks.cancel(self))
		self.cancelButton.grid(row=0, column=4)

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

	def buildChangePseudo(self):
		self.pseudoStr = tk.StringVar()
		if len(self.ui.client.username) >= 5:
			self.pseudoStr.set(self.ui.client.username)
		self.pseudoLabel = tk.Label(self.masterFrame, text=self.ui.res.changePseudoLabel)
		self.pseudoEntry = tk.Entry(self.masterFrame, textvariable=self.pseudoStr,
		width=20)
		self.pseudoLabel.grid(row=0, column=0)
		self.pseudoEntry.grid(row=0, column=1)
		self.buttonFrame = tk.Frame(self.masterFrame)
		self.buttonFrame.grid(row=1, column=1)
		self.buttonDone = tk.Button(self.buttonFrame, text='Done', width=8,
		command= lambda : self.ui.callbacks.done(self))
		self.buttonDone.grid(row=1, column=1)
		self.buttonCancel = tk.Button(self.buttonFrame, text='Cancel', width=8,
		command= lambda : self.ui.callbacks.cancel(self))
		self.buttonCancel.grid(row=1, column=0)

	def buildChangePassword(self):
		#StringVar
		self.oldPasswordStr = tk.StringVar()
		self.newPasswordStr1 = tk.StringVar()
		self.newPasswordStr2 = tk.StringVar()
		#Labels & Entry
		self.oldPasswordLabel = tk.Label(self.masterFrame, text=self.ui.res.oldPasswordLabel)
		self.oldPasswordEntry = tk.Entry(self.masterFrame, textvariable=self.oldPasswordStr,
		width=20, show='*')
		self.newPasswordLabel1 = tk.Label(self.masterFrame, text=self.ui.res.newPasswordLabel)
		self.newPasswordEntry1 = tk.Entry(self.masterFrame, textvariable=self.newPasswordStr1,
		width=20, show='*')
		self.newPasswordLabel2 = tk.Label(self.masterFrame, text=self.ui.res.newPasswordLabel)
		self.newPasswordEntry2 = tk.Entry(self.masterFrame, textvariable=self.newPasswordStr2,
		width=20, show='*')
		self.oldPasswordLabel.grid(row=0, column=0)
		self.oldPasswordEntry.grid(row=0, column=1)
		self.newPasswordLabel1.grid(row=1, column=0)
		self.newPasswordEntry1.grid(row=1, column=1)
		self.newPasswordLabel2.grid(row=2, column=0)
		self.newPasswordEntry2.grid(row=2, column=1)
		#Buttons
		self.buttonFrame = tk.Frame(self.masterFrame)
		self.buttonFrame.grid(row=3, column=1)
		self.buttonDone = tk.Button(self.buttonFrame, text='Done', width=8,
		command= lambda : self.ui.callbacks.done(self))
		self.buttonDone.grid(row=0, column=1)
		self.buttonCancel = tk.Button(self.buttonFrame, text='Cancel', width=8,
		command= lambda : self.ui.callbacks.cancel(self))
		self.buttonCancel.grid(row=0, column=0)
		#Output Frame
		self.outputFrame = tk.Frame(self.masterFrame)
		self.outputFrame.grid(row=4, column=0, columnspan=2)
		self.outputLabel = tk.Label(self.outputFrame, wraplength=190)
		self.outputLabel.grid(row=0, column=0)

	def buildConnect(self):
		self.serverListFrame = tk.Frame(self.masterFrame)
		self.serverListFrame.grid(row=0, column=0)
		self.serverInfosFrame = tk.Frame(self.masterFrame)
		self.serverInfosFrame.grid(row=0, column=1, sticky='N')
		self.buttonFrame = tk.Frame(self.masterFrame)
		self.buttonFrame.grid(row=1, column=0, columnspan=2)
		#SERVER CHOICE
		#LISTBOX
		self.serverListbox = tk.Listbox(self.serverListFrame, selectmode ='single',
		height=20)
		#ADD ALL SERVER SAVED TO LISTBOX
		for srv in self.ui.client.serverList:
			self.serverListbox.insert(tk.END, srv.name)
		self.serverListbox.grid(row=0, column=0, rowspan=6)
		#SERVER NAME
		self.serverNameLabel = tk.Label(self.serverInfosFrame, text=self.ui.res.serverNameLabel)
		self.serverNameLabel.grid(row=0, column=1, sticky='W', padx=5)
		self.serverName = tk.StringVar()
		self.serverNameEntry = tk.Entry(self.serverInfosFrame, textvariable=self.serverName,
		width=25, state='disabled')
		self.serverNameEntry.grid(row=1, column=1, padx=5)
		#ADDRESS
		self.adressLabel = tk.Label(self.serverInfosFrame, text = self.ui.res.adressLabel)
		self.adressLabel.grid(row=2, column=1, sticky='W', padx=5)
		self.server_address = tk.StringVar()
		self.addressEntry = tk.Entry(self.serverInfosFrame, textvariable = self.server_address,
		width=25, state='disabled')
		self.addressEntry.grid(row=3, column=1, padx=5)
		#PORT
		self.portLabel = tk.Label(self.serverInfosFrame, text=self.ui.res.portLabel)
		self.portLabel.grid(row=4, column=1, sticky='W', padx=5)
		self.port = tk.StringVar()
		self.portEntry = tk.Entry(self.serverInfosFrame, textvariable=self.port,
		width=25, state='disabled')
		self.portEntry.grid(row=5, column=1, padx=5)
		#BUTTONS
		self.buttonDone = tk.Button(self.buttonFrame, text=self.ui.res.serverConnect, width=8,
		command= lambda : self.ui.callbacks.done(self))
		self.buttonDone.grid(row=1, column=1)
		self.buttonCancel = tk.Button(self.buttonFrame, text=self.ui.res.cancel, width=8,
		command= lambda : self.ui.callbacks.cancel(self))
		self.buttonCancel.grid(row=1, column=0)

################################################################################
# TO REWRITE                                                                   #
################################################################################

	#NOT USED
	def buttonbox(self):
		"""Method to create Confirm and Cancel Buttons of the DialogBox."""
		box = tk.Frame(self)
		w = tk.Button(box, text='OK', width=10, command=self.ok, default=tk.ACTIVE)
		w.grid(row=0, column=0, padx=5, pady=5)
		w = tk.Button(box, text='Cancel', width=10, command=self.cancel)
		w.grid(row=0, column=1, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.grid(row=1, column=0)

	def ok(self, event=None):
		if not self.validate():
			self.initial_focus.focus_set()
			return
		self.withdraw()
		self.update_idletasks()
		self.apply()
		self.cancel()

	def cancel(self, event=None):
		self.parent.focus_set()
		self.destroy()

	def apply(self):
		"""Method to apply changes if needed."""
		if self.bodyType == 'personal_informations':
			print(self.pseudoStr.get())
		if self.bodyType == 'connect':
			if self.connectTo.get() == 'local':
				from socket import socket, AF_INET, SOCK_STREAM
				self.ui.client.socket = socket(AF_INET, SOCK_STREAM)
				self.ui.client.socket.connect(('localhost', 4242))