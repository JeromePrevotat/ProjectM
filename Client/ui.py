"""Gui Module."""

import tkinter as tk

from tkinter import ttk, Menu, scrolledtext

import callbacks as callb
from resources import Resources

BASE_SIZE = (800, 600)

class Gui():
    """Gui Class."""
    def __init__(self, client):
        self.client = client
        self.root = tk.Tk()
        self.res = Resources('en')
        self.callbacks = callb.Callbacks(self)
        self.init_gui()

    def init_gui(self):
        """Initialize the bases of the gui."""
        self.root.title(self.res.title)
        #Forces the root window to be foreground
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        #MAIN FRAME
        self.main_frame = tk.Frame(self.root, name='main_frame')
        self.main_frame.grid(row=0, column=0, sticky='NSWE')
        if not self.client.user.logged:
            self.build_log_in_ui()

    def build_log_in_ui(self):
        """Build the Log In gui."""
        #FRAMES
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.log_in_frame = tk.Frame(self.main_frame, width=300, height=450, \
        name="log_in_frame")
        self.log_in_frame.grid(row=0, column=0, sticky='NSEW')
        self.log_in_frame.grid_propagate(False)
        self.log_in_frame.columnconfigure(0, weight=1)
        self.log_in_frame.rowconfigure((0, 1, 2), weight=1)
        self.infos_frame = tk.Frame(self.log_in_frame, width=200, height=200)
        self.infos_frame.columnconfigure(0, weight=1)
        self.infos_frame.grid(row=0, column=0, sticky='NSEW')
        self.infos_frame.grid_propagate(False)
        self.error_frame = tk.Frame(self.log_in_frame)
        self.error_frame.grid(row=1, column=0)
        self.button_frame = tk.Frame(self.log_in_frame, width=200, height=50)
        self.button_frame.columnconfigure((0, 1), weight=1)
        self.button_frame.grid(row=2, column=0, sticky='NSEW')
        self.button_frame.grid_propagate(False)
        #USERNAME
        self.username = tk.StringVar()
        self.username_label = tk.Label(self.infos_frame, \
        text=self.res.username, pady=5)
        self.username_entry = tk.Entry(self.infos_frame, \
        textvariable=self.username)
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=1, column=0)
        #PASSWORD
        self.password = tk.StringVar()
        self.password_label = tk.Label(self.infos_frame, \
        text=self.res.password, pady=5)
        self.password_entry = tk.Entry(self.infos_frame, \
        textvariable=self.password, show='*')
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=3, column=0)
        #ERROR
        self.error_label = tk.Label(self.error_frame, wraplength=190, fg='red')
        self.error_label.grid(row=4, column=0, padx=5)
        #BUTTONS
        self.log_in_button = tk.Button(self.button_frame, text=self.res.log_in, \
        width=8, name="log_in_button", command=self.callbacks.log_in)
        self.exit_button = tk.Button(self.button_frame, text=self.res.exit, \
        width=8, name="exit_button", command=self.callbacks._quit)
        self.register_button = tk.Button(self.button_frame,         \
        text=self.res.register, width=8, name="register_button",    \
        command=self.build_register)
        self.log_in_button.grid(row=1, column=0)
        self.exit_button.grid(row=1, column=1)
        self.register_button.grid(row=0, column=0, columnspan=2, padx=5)
        #Set Keypress Return default behaviour to Done
        self.log_in_button.focus_set()
        self.main_frame.bind_all("<Return>", self.callbacks.key_press_return)

    def build_register(self):
        """Build the Register Window gui."""
        self.mail = tk.StringVar()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.mail_label = tk.Label(self.infos_frame, text=self.res.mail, pady=5)
        self.mail_entry = tk.Entry(self.infos_frame, textvariable=self.mail)
        self.mail_label.grid(row=4, column=0)
        self.mail_entry.grid(row=5, column=0)
        #Number Field
        self.number_str = tk.StringVar()
        self.number_label = tk.Label(self.infos_frame, text=self.res.number, pady=5)
        self.number_entry = tk.Entry(self.infos_frame, textvariable=self.number_str)
        self.number_label.grid(row=6, column=0)
        self.number_entry.grid(row=7, column=0)
        #End number Field
        self.register_button.grid_remove()
        #REGISTER MODE
        #Create the new user in the DB
        #Ask for the confirmation sent via sms
        self.log_in_button.config(text=self.res.done, \
        command=self.callbacks.check_entry)
        #Do not ask for the confirmation via sms
        #self.log_in_button.config(text=self.res.done,
        #command=self.callbacks.newUser)
        #Exit Button
        self.exit_button.config(text=self.res.cancel, \
        command=self.build_log_in_ui)

    def build_main_ui(self):
        """Build the Main gui"""
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=2)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        #USER FRAME
        self.user_frame = tk.LabelFrame(self.main_frame, \
        text=self.res.user_list_label, width=BASE_SIZE[0]/4, height=BASE_SIZE[1])
        self.user_frame.rowconfigure(0, weight=1)
        self.user_frame.columnconfigure(0, weight=1)
        self.user_frame.grid(row=0, column=0, rowspan=2, sticky='NSWE')
        #READ FRAME
        self.output_frame = tk.LabelFrame(self.main_frame, \
        text=self.res.output_label, width=BASE_SIZE[0]*0.75, height=(BASE_SIZE[1]/3)*2)
        self.output_frame.rowconfigure(0, weight=1)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.grid(row=0, column=1, sticky='NSWE')
        #WRITE FRAME
        self.input_frame = tk.LabelFrame(self.main_frame, \
        text=self.res.input_label, width=BASE_SIZE[0]*0.75, height=BASE_SIZE[1]/3)
        self.input_frame.rowconfigure(0, weight=1)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.grid(row=1, column=1, sticky='NSWE')

        #USER SCROLLEDTEXT
        self.user_list = tk.scrolledtext.ScrolledText(self.user_frame, \
        wrap=tk.WORD, width=25, state='disabled')
        self.user_list.grid(row=0, column=0, sticky='NSWE', pady=2, padx=1)
        #READ SCROLLEDTEXT
        self.msg_output = tk.scrolledtext.ScrolledText(self.output_frame, \
        wrap=tk.WORD, state='disabled')
        self.msg_output.grid(row=0, column=0, sticky='NSWE', padx=1, pady=2)
        #WRITE SCROLLEDTEXT
        self.msg_input = tk.scrolledtext.ScrolledText(self.input_frame, \
        wrap=tk.WORD, height=11)
        self.msg_input.grid(row=0, column=0, sticky='NSWE', padx=1, pady=2)

        #SEND BUTTON
        self.send_button = ttk.Button(self.input_frame, text=self.res.send)
        self.send_button.grid(row=1, column=0)

        #MENUS
        #MAIN BAR
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        #SERVER MENU
        self.server_menu = Menu(self.menu_bar, tearoff=0)
        self.server_menu.add_command(label=self.res.server_connect, \
        state='disabled', command=self.callbacks.server_connect)
        self.server_menu.add_command(label=self.res.server_infos, \
        state='disabled', command=self.callbacks.server_infos)
        self.server_menu.add_command(label=self.res.manage_server, \
        command=self.callbacks.manage_server)
        self.menu_bar.add_cascade(label=self.res.server_menu, menu=self.server_menu)
        #PROFILE MENU
        self.profile_menu = Menu(self.menu_bar, tearoff=0)
        #Change Pseudo
        self.profile_menu.add_command(label=self.res.change_pseudo, \
        command=self.callbacks.change_pseudo)
        #Change password
        self.profile_menu.add_command(label=self.res.change_password, \
        command=self.callbacks.change_password)
        #Change mail
        self.menu_bar.add_cascade(label=self.res.profile, menu=self.profile_menu)
        #HELP MENU
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label=self.res.about)
        self.menu_bar.add_cascade(label=self.res.help_menu, menu=self.help_menu)
        ########################################################################
        #   THREAD UPDATE MENU                                                   #
        ########################################################################
        self.client.thread_list.create_thread('update_menu', self)
