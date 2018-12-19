"""Threads Management Module."""

import time

import tkinter as tk
from threading import Thread

import timeformat as tFormat

import encoding

class Threads():
    """Custom Thread Class."""
    def __init__(self, client):
        self.client = client
        self.new_thread = None

    def create_thread(self, *args):
        """Creates a new Thread."""
        if args is not None:
            thread_name = args[0]
            if len(list(args)) > 1:
                thread_args = list(args[1:])
        if thread_name in ['manage_server', 'connect']:
            self.new_thread = Thread( \
            target=lambda: self.manage_thread(thread_args[0]), daemon=True)
            self.new_thread.start()
        if thread_name == 'update_menu':
            self.new_thread = Thread( \
            target=lambda: self.update_menu(thread_args[0]), daemon=True)
            self.new_thread.start()
        if thread_name == 'listen_server':
            self.new_thread = Thread(target=self.listen_server, daemon=True)
            self.new_thread.start()
        if thread_name == 'user_list':
            self.new_thread = Thread(target=self.user_list_thread, daemon=True)
            self.new_thread.start()

    def update_menu(self, gui):
        """Thread disabling the Connect Menu if already connected to a Server."""
        while gui.root.winfo_exists():
            #CONNECT COMMAND
            if (gui.client.server.name is None and  \
            gui.client.server.address is None and   \
            gui.client.server.port is None and      \
            gui.server_menu.entrycget(0, 'state') == 'disabled'):
                gui.server_menu.entryconfigure(0, state='normal')
            elif(gui.client.server.name is not None and \
            gui.client.server.address is not None and   \
            gui.client.server.port is not None and      \
            gui.server_menu.entrycget(0, 'state') == 'normal'):
                gui.server_menu.entryconfigure(0, state='disabled')
            #SERVER INFOS COMMAND
            if (gui.client.server.name is None and  \
            gui.client.server.address is None and   \
            gui.client.server.port is None and      \
            gui.server_menu.entrycget(1, 'state') == 'normal'):
                gui.server_menu.entryconfigure(1, state='disabled')
            elif(gui.client.server.name is not None and \
            gui.client.server.address is not None and   \
            gui.client.server.port is not None and      \
            gui.server_menu.entrycget(1, 'state') == 'disabled'):
                gui.server_menu.entryconfigure(1, state='normal')
            time.sleep(0.2)

    def manage_thread(self, dialbox):
        """Thread Manage Window."""
        while dialbox.winfo_exists() and dialbox.server_listbox.winfo_exists():
            if len(dialbox.server_listbox.curselection()) > 0:
                if isinstance(dialbox.server_listbox.curselection()[0], int):
                    index = dialbox.server_listbox.curselection()[0]
                    try:
                        self.update_server_entries(dialbox, index)
                    except:
                        pass
                if isinstance(dialbox.server_listbox.curselection()[0], str):
                    self.update_server_entries(dialbox, index)
            time.sleep(0.2)

    def update_server_entries(self, dialbox, index):
        """Thread displaying Servers Infos."""
        if not dialbox.edit:
            dialbox.entries_unlock()
            dialbox.server_name.set(self.client.server_list[index].name)
            dialbox.server_address.set(self.client.server_list[index].address)
            dialbox.port.set(self.client.server_list[index].port)
            dialbox.entries_lock()

    def listen_server(self):
        """Thread listenning to the Server."""
        while True:
            received = self.client.socket.recv(1024).decode()
            while received != "":
                cmd, args, msg, length = encoding.parse_type_received(received)
                received = received[length:]
            if cmd:
                if cmd == "request":
                    self.client.gui.user_list.config(state='normal')
                    self.client.gui.user_list.delete(1.0, tk.END)
                    self.client.gui.user_list.insert(tk.INSERT, args)
                    self.client.gui.user_list.config(state='disabled')
            if msg:
                self.client.gui.msg_output.config(state='normal')
                self.client.gui.msg_output.insert(tk.INSERT, msg + '\nAt ' + \
                tFormat.get_time_format(self.client.gui) + '\n')
                self.client.gui.msg_output.config(state='disabled')

    def user_list_thread(self):
        """Thread displaying connected Users."""
        while self.client.server.connected:
            self.client.socket.send(encoding.encode_cmd("request()"))
            time.sleep(0.2)
