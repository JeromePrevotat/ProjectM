import tkinter as tk

from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from tkinter import filedialog as fd

from os import path
from os import makedirs

from threading import Thread
from queue import Queue, Empty
import time

from Resources import I18N

colors = ['Blue', 'Gold', 'Red']

class Tab2():
	def __init__(self, gui):
		self.gui = gui
		#MAIN FRAMES
		self.yolo = ttk.LabelFrame(gui.tab2, text=' The Snake ')
		self.yolo.grid(row=0, column=0, padx=8, pady=4)

		#SPINBOX
		self.spin = tk.Spinbox(self.yolo, width=5, bd=8, command=self._spin)
		self.spin['values'] = (1, 4, 42, 100)
		self.spin.grid(row=0, column=0, sticky='W')
		self.spin2 = tk.Spinbox(self.yolo, values=(0, 50, 100), width=5, bd=8,
		command=self._spin, relief=tk.RIDGE)
		self.spin2.grid(row=0, column=2, sticky='W')

		#COMBOBOX
		self.number = tk.StringVar()
		self.numberChosen = ttk.Combobox(self.yolo, width=14, textvariable=self.number,
		state='readonly')
		self.numberChosen['values'] = (1, 2, 4, 42, 100)
		self.numberChosen.grid(row=1, column=1)
		self.numberChosen.current(0)

		#CHECKBUTTONS
		self.chVarDis = tk.IntVar()
		self.check1 = tk.Checkbutton(self.yolo, text=gui.i18n.disabled,
		variable=self.chVarDis, state='disabled')
		self.check1.select()
		self.check1.grid(row=2, column=0, sticky=tk.W)
		self.chVarUn = tk.IntVar()
		self.check2 = tk.Checkbutton(self.yolo, text=gui.i18n.unchecked,
		variable=self.chVarUn)
		self.check2.deselect()
		self.check2.grid(row=2, column=1)
		self.chVarEn = tk.IntVar()
		self.check3 = tk.Checkbutton(self.yolo, text=gui.i18n.toggle,
		variable=self.chVarEn)
		self.check3.select()
		self.check3.grid(row=2, column=2, sticky = tk.W)

		#RADIONBUTTONS
		self.radVar = tk.IntVar()
		self.radVar.set(99)
		for col in range(3):
			curRad = 'rad' + str(col)
			curRad = tk.Radiobutton(self.yolo, text=colors[col], variable=self.radVar,
			value=col, command=self.radCall)
			curRad.grid(row=3, column=col)

		#TIMEZONES BUTTON
		self.allTZs = ttk.Button(self.yolo, text=self.gui.i18n.timezones,
		command=self.gui.allTimeZones)
		self.allTZs.grid(row=4, column=1,sticky='WE')
		self.localTZ = ttk.Button(self.yolo, text=self.gui.i18n.localtz,
		command=self.gui.localTimeZone)
		self.localTZ.grid(row=4, column=0,sticky='WE')
		self.getTime = ttk.Button(self.yolo, text=self.gui.i18n.getTime,
		command=self.gui.getDateTime)
		self.getTime.grid(row=4, column=2,sticky='WE')

		#LABELS
		self.labelsFrame = ttk.LabelFrame(self.yolo, text=gui.i18n.labelsFrame)
		self.labelsFrame.grid(column=1, pady=40)
		self.label1 = ttk.Label(self.labelsFrame, text=gui.i18n.label1).grid(row=0, column=0)
		self.lbl2 = tk.StringVar()
		self.lbl2.set(self.gui.i18n.label2)
		self.label2 = ttk.Label(self.labelsFrame, textvariable=self.lbl2).grid(row=1, column=0)
		self.label3 = ttk.Label(self.labelsFrame, text=gui.i18n.label3).grid(row=2, column=0)
		for child in self.labelsFrame.winfo_children():
			child.grid_configure(padx=8, pady=4)

		#MANAGE FILE FRAME
		self.mngFilesFrame = ttk.LabelFrame(gui.tab2, text=gui.i18n.mgrFiles)
		self.mngFilesFrame.grid(row=1, column=0, sticky='WE', padx=10, pady=5)

		#BUTTONS
		self.lb = ttk.Button(self.mngFilesFrame, text=gui.i18n.browseTo, command=self.getFileName)
		self.lb.grid(row=0, column=0, sticky='W')

		scrolW = 40
		scrolH = 10
		self.file = tk.StringVar()
		self.entryLen = scrolW
		self.fileEntry = ttk.Entry(self.mngFilesFrame, width=self.entryLen, textvariable=self.file)
		self.fileEntry.grid(row=0, column=1, sticky='W')

		self.logDir = tk.StringVar()
		self.netwEntry = ttk.Entry(self.mngFilesFrame, width=self.entryLen, textvariable=self.logDir)
		self.netwEntry.grid(row=1 , column=1, sticky='W')

		self.cb = ttk.Button(self.mngFilesFrame, text=gui.i18n.copyTo, command=self.copyFile)
		self.cb.grid(row=1, column=0, sticky='E')
		for child in self.mngFilesFrame.winfo_children():
			child.grid_configure(padx=6, pady=6)

	def radCall(self):
		radSel = self.radVar.get()
		#if radSel == 0: self.yolo.configure(text=colors[0])
		#elif radSel == 1: self.yolo.configure(text=colors[1])
		#elif radSel == 2: self.yolo.configure(text=colors[2])

		if radSel == 0: self.yolo.configure(text=self.gui.i18n.WIDGET_LABEL + self.gui.i18n.colorsIn[0])
		elif radSel == 1: self.yolo.configure(text=self.gui.i18n.WIDGET_LABEL + self.gui.i18n.colorsIn[1])
		elif radSel == 2: self.yolo.configure(text=self.gui.i18n.WIDGET_LABEL + self.gui.i18n.colorsIn[2])

	def _spin(self):
		value = self.spin.get()
		print(value)
		self.scr.insert(tk.INSERT, value + '\n')

	def getFileName(self):
		print('Hello from getFilename !')
		fDir = path.dirname(__file__)
		fName = fd.askopenfilename(parent=self.gui.win, initialdir=fDir)
		self.fileEntry.delete(0, tk.END)
		self.fileEntry.insert(0, fName)

	def copyFile(self):
		import shutil
		src = self.fileEntry.get()
		file = src.split('/')[-1]
		dst = self.netwEntry.get() + '/' + file
		try:
			shutil.copy(src, dst)
			mBox.showinfo('Copy File to Network...', 'Sucess File Copied !')
		except FileNotFoundError as err:
			mBox.showerror('Copy File to Network...',
			'*** Failed to Copy File ! ***\n\n' + str(err))
		except Exception as ex:
			mBox.showerror('Copy File to Network...',
			'*** Failed to Copy File ! ***\n\n' + str(ex))