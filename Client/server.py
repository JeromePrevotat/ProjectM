"""Module containing the Server Class."""

import os
import time
import socket

import tkinter as tk
from pickle import Pickler, Unpickler

import encoding

class Server():
    """Class Server."""
    def __init__(self, name=None, address=None, port=None):
        self.name = name
        self.address = address
        self.port = port
        self.connected = False

    def save_server(self, abs_path=None, save_dir=None, ext=None):
        """Save a new Server."""
        if os.path.exists(save_dir) and not os.path.isfile(save_dir):
            os.chdir(save_dir)
        else:
            os.mkdir(save_dir)
            os.chdir(save_dir)
        with open(self.name + ext, 'wb') as new_file:
            pickler = Pickler(new_file)
            pickler.dump(self)
        os.chdir(abs_path)

    def connect_to(self, server_name, server_infos, client):
        """Connect to a Server."""
        client.server.name = server_name
        client.server.address = server_infos[0]
        client.server.port = server_infos[1]
        max_connexion_attempts = 10
        failed = 0
        #Client output
        client.gui.msg_output.config(state='normal')
        client.gui.msg_output.insert(tk.INSERT, 'Trying to connect to ' + \
        server_infos[0] + ':' + str(server_infos[1]) + '\n')
        client.gui.msg_output.config(state='disabled')
        #Connection Loop
        while not self.connected and failed < max_connexion_attempts:
            try:
                client.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.socket.connect(server_infos)
                self.connected = True
                client.gui.msg_output.config(state='normal')
                client.gui.msg_output.insert(tk.INSERT, \
                'Connexion Successful !\nWelcome <' + client.username + '> !\n')
                client.gui.msg_output.config(state='disabled')
            except:
                client.gui.msg_output.config(state='normal')
                client.gui.msg_output.insert(tk.INSERT, 'Connexion Failed...\n')
                client.gui.msg_output.config(state='disabled')
                failed += 1
                time.sleep(1)
        if failed == max_connexion_attempts:
            client.gui.msg_output.config(state='normal')
            client.gui.msg_output.insert(tk.INSERT, \
            'Connexion aborted : Too many failed attempts.\n')
            client.gui.msg_output.config(state='disabled')
        else:
            self.update_username(client.username, client.socket)
            client.gui.msg_input.bind('<KeyPress - Return>', \
            lambda event: client.gui.callbacks.send_msg(client.gui))
            client.gui.send_button.configure( \
            command=lambda: client.gui.callbacks.send_msg(client.gui))
            client.thread_list.create_thread('listen_server')
            client.thread_list.create_thread('user_list')

    def update_username(self, username, sock):
        """Update the Username."""
        update = "rename(" + username + ")"
        sock.send(encoding.encode_cmd(update))

def get_server_list(client):
    """Return a List of all saved Servers."""
    server_list = []
    if os.path.exists(client.save_dir) and not os.path.isfile(client.save_dir):
        os.chdir(client.save_dir)
    else:
        os.mkdir(client.save_dir)
        os.chdir(client.save_dir)
    dir_content = os.listdir(os.getcwd())
    for srv_file in dir_content:
        if len(srv_file) >= 5 and srv_file[len(srv_file) - len(client.ext):] == client.ext:
            with open(srv_file, 'rb') as srv:
                depickler = Unpickler(srv)
                server = depickler.load()
            server_list.append(server)
    os.chdir(client.abs_path)
    return server_list
