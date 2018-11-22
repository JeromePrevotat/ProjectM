import tkinter as tk

def setVar(dialbox):
	dialbox.usernameStr = tk.StringVar()
	dialbox.oldPasswordStr = tk.StringVar()
	dialbox.newPasswordStr1 = tk.StringVar()
	dialbox.newPasswordStr2 = tk.StringVar()

def buildFrames(dialbox):
	dialbox.buttonFrame = tk.Frame(dialbox.masterFrame)
	dialbox.buttonFrame.grid(row=4, column=1)
	dialbox.outputFrame = tk.Frame(dialbox.masterFrame)
	dialbox.outputFrame.grid(row=5, column=0, columnspan=2)

def buildLabels(dialbox):
	#Input Label
	dialbox.usernameLabel = tk.Label(dialbox.masterFrame, text=dialbox.ui.res.usernameLabel)
	dialbox.oldPasswordLabel = tk.Label(dialbox.masterFrame, text=dialbox.ui.res.oldPasswordLabel)
	dialbox.newPasswordLabel1 = tk.Label(dialbox.masterFrame, text=dialbox.ui.res.newPasswordLabel)
	dialbox.newPasswordLabel2 = tk.Label(dialbox.masterFrame, text=dialbox.ui.res.newPasswordLabel)
	dialbox.usernameLabel.grid(row=0, column=0)
	dialbox.oldPasswordLabel.grid(row=1, column=0)
	dialbox.newPasswordLabel1.grid(row=2, column=0)
	dialbox.newPasswordLabel2.grid(row=3, column=0)
	#Output Label
	dialbox.outputLabel = tk.Label(dialbox.outputFrame, wraplength=190)
	dialbox.outputLabel.grid(row=0, column=0)

def buildEntry(dialbox):
	dialbox.usernameEntry = tk.Entry(dialbox.masterFrame, textvariable=dialbox.usernameStr,
	width=20)
	dialbox.oldPasswordEntry = tk.Entry(dialbox.masterFrame, textvariable=dialbox.oldPasswordStr,
	width=20, show='*')
	dialbox.newPasswordEntry1 = tk.Entry(dialbox.masterFrame, textvariable=dialbox.newPasswordStr1,
	width=20, show='*')
	dialbox.newPasswordEntry2 = tk.Entry(dialbox.masterFrame, textvariable=dialbox.newPasswordStr2,
	width=20, show='*')
	dialbox.usernameEntry.grid(row=0, column=1)
	dialbox.oldPasswordEntry.grid(row=1, column=1)
	dialbox.newPasswordEntry1.grid(row=2, column=1)
	dialbox.newPasswordEntry2.grid(row=3, column=1)

def fillButtonFrame(dialbox):
	dialbox.buttonDone = tk.Button(dialbox.buttonFrame, text='Done', width=8,
	command= lambda : dialbox.ui.callbacks.done(dialbox))
	dialbox.buttonDone.grid(row=0, column=1)
	dialbox.buttonCancel = tk.Button(dialbox.buttonFrame, text='Cancel', width=8,
	command= lambda : dialbox.ui.callbacks.cancel(dialbox))
	dialbox.buttonCancel.grid(row=0, column=0)