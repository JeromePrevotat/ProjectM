import tkinter as tk

def buildFrames(dialbox):
	#Window Frame
	dialbox.manageFrame = tk.Frame(dialbox.masterFrame)
	dialbox.manageFrame.grid(row=0, column=0)
	#SERVER LIST FRAME
	dialbox.serverListFrame = tk.Frame(dialbox.manageFrame)
	dialbox.serverListFrame.grid(row=0, column=0)
	#SERVER INFOS FRAME
	dialbox.serverInfosFrame = tk.Frame(dialbox.manageFrame)
	dialbox.serverInfosFrame.grid(row=0, column=1, sticky='N')
	#BUTTON FRAME
	dialbox.buttonFrame = tk.Frame(dialbox.manageFrame)
	dialbox.buttonFrame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def fillServerListFrame(dialbox):
	#LISTBOX
	dialbox.serverListbox = tk.Listbox(dialbox.serverListFrame, selectmode ='single',
	height=20)
	#ADD ALL SERVER SAVED TO LISTBOX
	for srv in dialbox.ui.client.serverList:
		dialbox.serverListbox.insert(tk.END, srv.name)
	dialbox.serverListbox.grid(row=0, column=0, rowspan=6)

def fillServerInfosFrame(dialbox):
	#SERVER NAME
	dialbox.serverNameLabel = tk.Label(dialbox.serverInfosFrame, text=dialbox.ui.res.serverNameLabel)
	dialbox.serverNameLabel.grid(row=0, column=1, sticky='W', padx=5)
	dialbox.serverName = tk.StringVar()
	dialbox.serverNameEntry = tk.Entry(dialbox.serverInfosFrame, textvariable=dialbox.serverName,
	width=25, state='disabled')
	dialbox.serverNameEntry.grid(row=1, column=1, padx=5)
	#ADDRESS
	dialbox.adressLabel = tk.Label(dialbox.serverInfosFrame, text = dialbox.ui.res.adressLabel)
	dialbox.adressLabel.grid(row=2, column=1, sticky='W', padx=5)
	dialbox.server_address = tk.StringVar()
	dialbox.addressEntry = tk.Entry(dialbox.serverInfosFrame, textvariable = dialbox.server_address,
	width=25, state='disabled')
	dialbox.addressEntry.grid(row=3, column=1, padx=5)
	#PORT
	dialbox.portLabel = tk.Label(dialbox.serverInfosFrame, text=dialbox.ui.res.portLabel)
	dialbox.portLabel.grid(row=4, column=1, sticky='W', padx=5)
	dialbox.port = tk.StringVar()
	dialbox.portEntry = tk.Entry(dialbox.serverInfosFrame, textvariable=dialbox.port,
	width=25, state='disabled')
	dialbox.portEntry.grid(row=5, column=1, padx=5)

def fillButtonFrame(dialbox):
	#ADD BUTTON
	dialbox.addButton = tk.Button(dialbox.buttonFrame, text=dialbox.ui.res.addserver,
	width=10, command=lambda : dialbox.ui.callbacks.add(dialbox))
	dialbox.addButton.grid(row=0, column=0)
	#DELETE BUTTON
	dialbox.delButton = tk.Button(dialbox.buttonFrame, text=dialbox.ui.res.delete,
	width=10)
	dialbox.delButton.grid(row=0, column=1)
	#EDIT BUTTON
	dialbox.editButton = tk.Button(dialbox.buttonFrame, text=dialbox.ui.res.edit,
	width=10, command=lambda : dialbox.ui.callbacks.edit(dialbox))
	dialbox.editButton.grid(row=0, column=2)
	#DONE BUTTON
	dialbox.doneButton = tk.Button(dialbox.buttonFrame, text=dialbox.ui.res.done,
	width=10, command=lambda : dialbox.ui.callbacks.done(dialbox))
	dialbox.doneButton.grid(row=0, column=3)
	#CANCEL BUTTON
	dialbox.cancelButton = tk.Button(dialbox.buttonFrame, text=dialbox.ui.res.cancel,
	width=10, command= lambda : dialbox.ui.callbacks.cancel(dialbox))
	dialbox.cancelButton.grid(row=0, column=4)