#GUI File
import tkinter as tk

from tkinter import ttk, scrolledtext, Menu
from tkinter import messagebox as mBox

import callbacks as callb
from resources import Resources

BASE_SIZE = (800,600)

class Gui():
	def __init__(self, client):
		self.client = client
		self.root = tk.Tk()
		self.res = Resources('en')
		self.callbacks = callb.Callbacks(self)
		self.init_gui()

	def init_gui(self):
		self.root.title(self.res.title)
		#Forces the root window to be foreground
		self.root.lift()
		self.root.attributes('-topmost', True)
		self.root.after_idle(self.root.attributes, '-topmost', False)
		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)

		#MAIN FRAME
		self.mainFrame = tk.Frame(self.root, name='mainFrame')
		self.mainFrame.grid(row=0, column=0, sticky='NSWE')
		if not self.client.user.logged :
			self.buildLogInUI()

	def buildLogInUI(self):
		#FRAMES
		self.mainFrame.columnconfigure(0, weight=1)
		self.mainFrame.rowconfigure(0, weight=1)
		self.logInFrame = tk.Frame(self.mainFrame, width=200, height=300, name="logInFrame")
		self.logInFrame.grid(row=0, column=0, sticky='NSEW')
		self.logInFrame.grid_propagate(False)
		self.logInFrame.columnconfigure(0, weight=1)
		self.logInFrame.rowconfigure((0,1,2), weight=1)
		self.infosFrame = tk.Frame(self.logInFrame, width=200, height=200)
		self.infosFrame.columnconfigure(0, weight=1)
		self.infosFrame.grid(row=0, column=0, sticky='NSEW')
		self.infosFrame.grid_propagate(False)
		self.errorFrame = tk.Frame(self.logInFrame)
		self.errorFrame.grid(row=1,column=0)
		self.buttonFrame = tk.Frame(self.logInFrame, width=200, height=100)
		self.buttonFrame.columnconfigure((0,1), weight=1)
		self.buttonFrame.grid(row=2, column=0, sticky='NSEW')
		self.buttonFrame.grid_propagate(False)
		#USERNAME
		self.username = tk.StringVar()
		self.usernameLabel = tk.Label(self.infosFrame, text=self.res.username, pady=5)
		self.usernameEntry = tk.Entry(self.infosFrame, textvariable=self.username)
		self.usernameLabel.grid(row=0, column=0)
		self.usernameEntry.grid(row=1, column=0)
		#PASSWORD
		self.password = tk.StringVar()
		self.passwordLabel = tk.Label(self.infosFrame, text=self.res.password, pady=5)
		self.passwordEntry = tk.Entry(self.infosFrame, textvariable=self.password, show='*')
		self.passwordLabel.grid(row=2, column=0)
		self.passwordEntry.grid(row=3, column=0)
		#ERROR
		self.errorLabel = tk.Label(self.errorFrame, wraplength=190, fg='red')
		self.errorLabel.grid(row=4, column=0, padx=5)
		#BUTTONS
		self.logInButton = tk.Button(self.buttonFrame, text=self.res.logIn, width=8,
		name="logInButton", command=self.callbacks.logIn)
		self.exitButton = tk.Button(self.buttonFrame, text=self.res.exit, width=8,
		name="exitButton", command=self.callbacks._quit)
		self.registerButton = tk.Button(self.buttonFrame, text=self.res.register, width=8,
		name="registerButton", command=self.buildRegister)
		self.logInButton.grid(row=1, column=0)
		self.exitButton.grid(row=1, column=1)
		self.registerButton.grid(row=0, column=0, columnspan=2, padx=5)

		#NEW
		self.logInButton.focus_set()
		self.mainFrame.bind_all("<Return>", self.callbacks.keyPress_Return)

	def buildRegister(self):
		self.mail = tk.StringVar()
		self.usernameEntry.delete(0, tk.END)
		self.passwordEntry.delete(0, tk.END)
		self.mailLabel = tk.Label(self.infosFrame, text=self.res.mail, pady=5)
		self.mailEntry = tk.Entry(self.infosFrame, textvariable=self.mail)
		self.mailLabel.grid(row=4 ,column=0)
		self.mailEntry.grid(row=5, column=0)
		self.registerButton.grid_remove()
		self.logInButton.config(text=self.res.done,
		command=self.callbacks.newUser)
		self.exitButton.config(text=self.res.cancel,
		command = self.buildLogInUI)

	def buildMainUI(self):
		self.mainFrame.rowconfigure(0, weight=1)
		self.mainFrame.rowconfigure(1, weight=2)
		self.mainFrame.columnconfigure(0, weight=1)
		self.mainFrame.columnconfigure(1, weight=3)
		#USER FRAME
		self.userFrame = tk.LabelFrame(self.mainFrame, text=self.res.userListLabel,
		width=BASE_SIZE[0]/4, height=BASE_SIZE[1])
		self.userFrame.rowconfigure(0, weight=1)
		self.userFrame.columnconfigure(0, weight=1)
		self.userFrame.grid(row=0, column=0, rowspan=2, sticky='NSWE')
		#READ FRAME
		self.outputFrame = tk.LabelFrame(self.mainFrame, text=self.res.outputLabel,
		width=BASE_SIZE[0]*0.75, height=(BASE_SIZE[1]/3)*2)
		self.outputFrame.rowconfigure(0, weight=1)
		self.outputFrame.columnconfigure(0, weight=1)
		self.outputFrame.grid(row=0, column=1, sticky='NSWE')
		#WRITE FRAME
		self.inputFrame = tk.LabelFrame(self.mainFrame, text=self.res.inputLabel,
		width=BASE_SIZE[0]*0.75, height=BASE_SIZE[1]/3)
		self.inputFrame.rowconfigure(0, weight=1)
		self.inputFrame.columnconfigure(0, weight=1)
		self.inputFrame.grid(row=1, column=1, sticky='NSWE')

		#USER SCROLLEDTEXT
		self.userList = tk.scrolledtext.ScrolledText(self.userFrame, wrap=tk.WORD,
		width=25, state='disabled')
		self.userList.grid(row=0, column=0, sticky='NSWE', pady=2, padx=1)
		#READ SCROLLEDTEXT
		self.msgOutput = tk.scrolledtext.ScrolledText(self.outputFrame, wrap=tk.WORD,
		state='disabled')
		self.msgOutput.grid(row=0, column=0, sticky='NSWE', padx=1, pady=2)
		#WRITE SCROLLEDTEXT
		self.msgInput = tk.scrolledtext.ScrolledText(self.inputFrame, wrap=tk.WORD,
		height=11)
		self.msgInput.grid(row=0, column=0, sticky='NSWE', padx=1, pady=2)

		#SEND BUTTON
		self.sendButton = ttk.Button(self.inputFrame, text=self.res.send)
		self.sendButton.grid(row=1, column=0)

		#MENUS
		#MAIN BAR
		self.menuBar = Menu(self.root)
		self.root.config(menu=self.menuBar)
		#SERVER MENU
		self.serverMenu = Menu(self.menuBar, tearoff=0)
		self.serverMenu.add_command(label=self.res.serverConnect, state='disabled',
		command=self.callbacks.serverConnect)
		self.serverMenu.add_command(label=self.res.serverInfos, state='disabled',
		command=self.callbacks.serverInfos)
		self.serverMenu.add_command(label=self.res.manageServer,
		command=self.callbacks.manageServer)
		self.menuBar.add_cascade(label=self.res.serverMenu, menu=self.serverMenu)
		#PROFILE MENU
		self.profileMenu = Menu(self.menuBar, tearoff=0)
		self.profileMenu.add_command(label=self.res.personal,
		command=self.callbacks.profile)
		self.menuBar.add_cascade(label=self.res.profile, menu=self.profileMenu)
		#HELP MENU
		self.helpMenu = Menu(self.menuBar, tearoff=0)
		self.helpMenu.add_command(label=self.res.about)
		self.menuBar.add_cascade(label=self.res.helpMenu, menu=self.helpMenu)
		########################################################################
		#   THREAD UPDATE MENU												   #
		########################################################################
		self.client.threadList.createThread('updateMenu', self)