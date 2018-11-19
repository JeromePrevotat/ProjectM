import tkinter as tk

def buildFrames(dialbox):
	#Buttons Frame
	dialbox.buttonFrame = tk.Frame(dialbox.masterFrame)
	dialbox.buttonFrame.grid(row=3, column=1)
	#Output Frame
	dialbox.outputFrame = tk.Frame(dialbox.masterFrame)
	dialbox.outputFrame.grid(row=4, column=0, columnspan=2)

def buildLabels(dialbox):
	#Input Fields
	dialbox.oldPseudoLabel = tk.Label(dialbox.masterFrame, text=dialbox.ui.res.oldPseudoLabel)
	dialbox.newPseudoLabel = tk.Label(dialbox.masterFrame, text=dialbox.ui.res.newPseudoLabel)
	dialbox.passwordLabel = tk.Label(dialbox.masterFrame, text=dialbox.ui.res.passwordLabel)
	dialbox.oldPseudoLabel.grid(row=0, column=0)
	dialbox.newPseudoLabel.grid(row=1, column=0)
	dialbox.passwordLabel.grid(row=2, column=0)
	#Output Label
	dialbox.outputLabel = tk.Label(dialbox.outputFrame, wraplength=190)
	dialbox.outputLabel.grid(row=0, column=0)

def buildEntry(dialbox):
	dialbox.oldPseudoEntry = tk.Entry(dialbox.masterFrame, textvariable=dialbox.oldPseudoStr,
	width=20)
	dialbox.newPseudoEntry = tk.Entry(dialbox.masterFrame, textvariable=dialbox.newPseudoStr,
	width=20)
	dialbox.passwordEntry = tk.Entry(dialbox.masterFrame, textvariable=dialbox.passwordStr,
	width=20, show='*')
	dialbox.oldPseudoEntry.grid(row=0, column=1)
	dialbox.newPseudoEntry.grid(row=1, column=1)
	dialbox.passwordEntry.grid(row=2, column=1)

def fillButtonFrame(dialbox):
	dialbox.buttonDone = tk.Button(dialbox.buttonFrame, text='Done', width=8,
	command= lambda : dialbox.ui.callbacks.done(dialbox))
	dialbox.buttonDone.grid(row=1, column=1)
	dialbox.buttonCancel = tk.Button(dialbox.buttonFrame, text='Cancel', width=8,
	command= lambda : dialbox.ui.callbacks.cancel(dialbox))
	dialbox.buttonCancel.grid(row=1, column=0)

def setVar(dialbox):
	dialbox.oldPseudoStr = tk.StringVar()
	dialbox.newPseudoStr = tk.StringVar()
	dialbox.passwordStr = tk.StringVar()
	if len(dialbox.ui.client.username) >= 5:
		dialbox.oldPseudoStr.set(dialbox.ui.client.username)

