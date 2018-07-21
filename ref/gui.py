import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from tkinter import messagebox as mBox, filedialog as fd

from os import path, makedirs

from threading import Thread
from queue import Queue, Empty
import time
import pytz

import tooltip as tips
import queues as bq
import tcp_server as srv
import URL as url
import mysql_test
import Callbacks as callb
from Resources import I18N

import tab2

fDir = path.dirname(__file__)
netDir = fDir + 'Backup'
if not path.exists(netDir):
	makedirs(netDir, exist_ok=True)

class OOP():
	def __init__(self):
		srvT = Thread(target=srv.startServer, daemon=True)
		srvT.start()
		self.win = tk.Tk()
		self.i18n = I18N('en')
		self.callbacks = callb.Callbacks(self)
		self.init_gui()
		self.guiQueue = Queue()
		self.callbacks.defaultFileEntries(fDir, netDir)

	def allTimeZones(self):
		for tz in pytz.all_timezones:
			self.scr.insert(tk.INSERT, tz + '\n')

	def localTimeZone(self):
		from tzlocal import get_localzone
		self.scr.insert(tk.INSERT, get_localzone())

	def getDateTime(self):
		from datetime import datetime
		fmtStrZone = "\"%Y-%m-%d %H:%M:%S\""
		self.tab2Content.lbl2.set(datetime.now().strftime(fmtStrZone))

	def useQueue(self):
		while True:
			try:
				data = self.guiQueue.get(False)
			except Empty:
				data = None
			if data is not None:
				print(data)
				self.scr.insert(tk.INSERT, data + '\n')

	def methodInAThread(self, numberOfLoops=10):
		for idx in range(numberOfLoops):
			time.sleep(1)
			self.scr.insert(tk.INSERT, str(idx) + '\n')
		time.sleep(1)
		print('methodInAThread():', self.runT.isAlive())

	def createThread(self, num):
		writeT = Thread(target=self.useQueue, daemon=True)
		writeT.start()

	def init_gui(self):
		self.win.title(self.i18n.title)
		self.win.lift()
		#Forces the win window to be on Foreground
		self.win.attributes('-topmost', True)
		#Allows the win window to pass Backgroud after idle
		self.win.after_idle(self.win.attributes, '-topmost', False)

		#TAB PANNELS
		self.tabControl = ttk.Notebook(self.win)
		self.tabControl.pack(expand=1, fill="both")

		self.tab1 = ttk.Frame(self.tabControl)
		self.tabControl.add(self.tab1, text='MySQL')
		self.tab2 = ttk.Frame(self.tabControl)
		self.tabControl.add(self.tab2, text=self.i18n.WIDGET_LABEL)

		#MySQL TAB
		#MAIN FRAMES
		self.pydb = ttk.LabelFrame(self.tab1, text='Python Database')
		self.pydb.rowconfigure(0, weight=1)
		self.pydb.columnconfigure(0, weight=1)
		self.pydb.grid(row=0, column=0, padx=8, pady=4)

		self.book_quote = ttk.LabelFrame(self.tab1, text='Book Quotations')
		self.book_quote.rowconfigure(1, weight=1)
		self.book_quote.columnconfigure(0, weight=1)
		self.book_quote.grid(row=1, column=0, padx=8, pady=4, sticky='WE')

		#LABELS
		ttk.Label(self.pydb, text='Book Title :').grid(row=0, column=0,sticky='W')
		ttk.Label(self.pydb, text='Page :').grid(row=0, column=	1, sticky='W')

		#BUTTONS
		self.insert_button = ttk.Button(self.pydb, text='Insert Quote',
		command=self.callbacks.insertQuote, width=15)
		self.insert_button.grid(row=1, column=2, sticky='NSWE')
		self.get_button = ttk.Button(self.pydb, text='Get Quote',
		command=self.callbacks.getQuote, width=15)
		self.get_button.grid(row=2, column=2, sticky='NSWE')
		self.modify_button = ttk.Button(self.pydb, text='Modify Quote',
		command=self.callbacks.click_me, width=15)
		self.modify_button.grid(row=3, column=2, sticky='NSWE')

		#ENTRY
		#TITLE ENTRY
		self.insert_title = tk.StringVar()
		self.insert_title_entry = ttk.Entry(self.pydb, width=35,
		textvariable=self.insert_title)
		self.insert_title_entry.grid(row=1, column=0, sticky='W')
		self.insert_title_entry.delete(0, tk.END)
		self.insert_title_entry.insert(0, '< Enter a Title >')

		self.get_title = tk.StringVar()
		self.get_title_entry = ttk.Entry(self.pydb, width=35,
		textvariable=self.get_title)
		self.get_title_entry.grid(row=2, column=0, sticky='W')
		self.get_title_entry.delete(0, tk.END)
		self.get_title_entry.insert(0, '< Enter a Title >')

		self.modify_title = tk.StringVar()
		self.modify_title_entry = ttk.Entry(self.pydb, width=35,
		textvariable=self.modify_title)
		self.modify_title_entry.grid(row=3, column=0, sticky='W')
		self.modify_title_entry.delete(0, tk.END)
		self.modify_title_entry.insert(0, '< Enter a Title >')

		#PAGE ENTRY
		self.insert_page = tk.StringVar()
		self.insert_page_entry = ttk.Entry(self.pydb, width=10,
		textvariable=self.insert_page)
		self.insert_page_entry.grid(row=1, column=1, sticky='W')
		self.insert_page_entry.delete(0, tk.END)
		self.insert_page_entry.insert(0, '< N° Page >')

		self.get_page = tk.StringVar()
		self.get_page_entry = ttk.Entry(self.pydb, width=10,
		textvariable=self.get_page)
		self.get_page_entry.grid(row=2, column=1, sticky='W')
		self.get_page_entry.delete(0, tk.END)
		self.get_page_entry.insert(0, '< N° Page >')

		self.modify_page = tk.StringVar()
		self.modify_page_entry = ttk.Entry(self.pydb, width=10,
		textvariable=self.modify_page)
		self.modify_page_entry.grid(row=3, column=1, sticky='W')
		self.modify_page_entry.delete(0, tk.END)
		self.modify_page_entry.insert(0, '< N° Page >')

		#SCROLLEDTEXT
		scrolW = 40
		scrolH = 10
		self.scr = scrolledtext.ScrolledText(self.book_quote, width=scrolW, height=scrolH, wrap=tk.WORD)
		for child in self.book_quote.winfo_children():
			child.grid_configure(sticky='W')
		self.scr.grid(row=5, column=0, columnspan=3, sticky='WE')

		#DIVERS
		#MENUBAR
		self.menuBar = Menu(self.win)
		self.win.config(menu=self.menuBar)
		self.fileMenu = Menu(self.menuBar, tearoff=0)
		self.fileMenu.add_command(label=self.i18n.new)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label=self.i18n.exit, command=self.callbacks._quit)
		self.menuBar.add_cascade(label=self.i18n.file, menu=self.fileMenu)
		self.helpMenu=Menu(self.menuBar, tearoff=0)
		self.helpMenu.add_command(label=self.i18n.about, command=self.callbacks._msgBox)
		self.menuBar.add_cascade(label=self.i18n.help, menu=self.helpMenu)

		#TOOLTIPS
		tips.createToolTip(self.book_quote, 'This is a Spin control.')
		#tips.createToolTip(self.scr, 'This is a ScrolledText Widget.')
		tips.createToolTip(self.insert_title_entry, 'This is a Entry control.')
		tips.createToolTip(self.insert_button, 'This is a Button control.')
		tips.createToolTip(self.get_button, 'This is a Button control.')
		tips.createToolTip(self.modify_button, 'This is a Button control.')

		self.tab2Content = tab2.Tab2(self)
		self.mySQL = mysql_test.MySQL()
		#self.mySQL.showData()



oop = OOP()
oop.win.mainloop()