import tkinter as tk
from time import sleep
from threading import Thread
from pytz import all_timezones, timezone
from datetime import datetime

class Callbacks():
	def __init__(self, oop):
		self.oop = oop

	def defaultFileEntries(self, fDir, netDir):
		self.oop.tab2Content.fileEntry.delete(0, tk.END)
		self.oop.tab2Content.fileEntry.insert(0, fDir)
		if len(fDir) > self.oop.tab2Content.entryLen:
			self.oop.tab2Content.fileEntry.config(width=len(fDir) + 3)
			self.oop.tab2Content.fileEntry.config(state='readonly')
		self.oop.tab2Content.netwEntry.delete(0, tk.END)
		self.oop.tab2Content.netwEntry.insert(0, netDir)
		if len(netDir) > self.oop.tab2Content.entryLen:
			self.oop.tab2Content.netwEntry.config(width=len(netDir) + 3)

	def _combo(self, val=0):
		value = self.oop.tab2Content.numberChosen.get()
		self.oop.scr.insert(tk.INSERT, value + '\n')

	def insertQuote(self):
		title = self.oop.insert_title_entry.get()
		page = self.oop.insert_page_entry.get()
		quote = self.oop.scr.get(1.0, tk.END)
		self.oop.mySQL.insertBooks(title, page, quote)

	def getQuote(self):
		allBooks = self.oop.mySQL.showBooks()
		self.oop.scr.insert(tk.INSERT, allBooks)

	def click_me(self):
		self.oop.tab2Content.button1.configure(text="Hello " + self.name.get() + ' ' + self.number.get())
		#self.button1.configure(state='disabled')
		#self.createThread(int(self.spin.get()))
		self.oop.tab2Content.scr.delete(1.0, tk.END)
		bq.writeToScroll(self)
		htmlData = url.getHTML()
		self.oop.tab2Content.scr.insert(tk.INSERT, htmlData)

	def _quit(self):
		self.win.quit()
		self.win.destroy()
		exit()

	def _msgBox(self):
		answer = mBox.askyesno('Python Message Dual Choice Box', 'Are you sure you really want to do this ?')
		print(answer)