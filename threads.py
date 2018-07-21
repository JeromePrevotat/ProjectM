import time

import tkinter as tk
from threading import Thread

import timeformat as tFormat

class Threads():
	def __init__(self, client):
		self.client = client

	def createThread(self, *args):
		if args is not None:
			threadName = args[0]
			if len(list(args)) > 1:
				threadArgs = list(args[1:])
		if threadName == 'manageServer' or threadName == 'connect':
			self.newThread = Thread(target= lambda : self.manageThread(threadArgs[0]), daemon=True)
			self.newThread.start()
		if threadName == 'updateMenu':
			self.newThread = Thread(target= lambda : self.updateMenu(threadArgs[0]), daemon=True)
			self.newThread.start()
		if threadName == 'listenServer':
			self.newThread = Thread(target= self.listenServer, daemon=True)
			self.newThread.start()
		if threadName == 'userList':
			self.newThread = Thread(target= self.userListThread, daemon=True)
			self.newThread.start()

	def updateMenu(self, ui):
		while ui.root.winfo_exists():
			#CONNECT COMMAND
			if (ui.client.server.name is None and
			ui.client.server.address is None and
			ui.client.server.port is None and
			ui.serverMenu.entrycget(0, 'state') == 'disabled'):
				ui.serverMenu.entryconfigure(0, state='normal')
			elif(ui.client.server.name is not None and
			ui.client.server.address is not None and
			ui.client.server.port is not None and
			ui.serverMenu.entrycget(0, 'state') == 'normal'):
				ui.serverMenu.entryconfigure(0, state='disabled')
			#SERVER INFOS COMMAND
			if (ui.client.server.name is None and
			ui.client.server.address is None and
			ui.client.server.port is None and
			ui.serverMenu.entrycget(1, 'state') == 'normal'):
				ui.serverMenu.entryconfigure(1, state='disabled')
			elif(ui.client.server.name is not None and
			ui.client.server.address is not None and
			ui.client.server.port is not None and
			ui.serverMenu.entrycget(1, 'state') == 'disabled'):
				ui.serverMenu.entryconfigure(1, state='normal')
			time.sleep(0.2)

	def manageThread(self, dialbox):
		while dialbox.winfo_exists() and dialbox.serverListbox.winfo_exists():
			if len(dialbox.serverListbox.curselection()) > 0:
				if type(dialbox.serverListbox.curselection()[0]) is int:
					index = dialbox.serverListbox.curselection()[0]
					self.updateServerEntries(dialbox, index)
				if type(dialbox.serverListbox.curselection()[0]) is str:
					self.updateServerEntries(dialbox,index)
			time.sleep(0.2)

	def updateServerEntries(self, dialbox, index):
		dialbox.serverNameEntry.config(state='normal')
		dialbox.serverName.set(self.client.serverList[index].name)
		dialbox.serverNameEntry.config(state='disabled')
		dialbox.addressEntry.config(state='normal')
		dialbox.server_address.set(self.client.serverList[index].address)
		dialbox.addressEntry.config(state='disabled')
		dialbox.portEntry.config(state='normal')
		dialbox.port.set(self.client.serverList[index].port)
		dialbox.portEntry.config(state='disabled')

	def listenServer(self):
		while True:
			msg = self.client.socket.recv(1024)
			if msg.decode()[:9] == '?REQUEST\n':
				self.client.gui.userList.config(state='normal')
				self.client.gui.userList.delete(1.0, tk.END)
				self.client.gui.userList.insert(tk.INSERT, msg.decode()[9:])
				self.client.gui.userList.config(state='disabled')
			elif msg.decode() != '' and msg.decode()[:9] != '?REQUEST\n':
				self.client.gui.msgOutput.config(state='normal')
				self.client.gui.msgOutput.insert(tk.INSERT, msg.decode() + '\nAt ' + tFormat.get_time_format(self.client.gui) + '\n')
				self.client.gui.msgOutput.config(state='disabled')

	def userListThread(self):
		while self.client.server.connected:
			self.client.socket.send('?REQUEST\n'.encode())
			time.sleep(0.5)
