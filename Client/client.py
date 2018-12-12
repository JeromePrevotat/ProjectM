"""Client Module."""

import os
import sys
import socket

from user import User
from queue import Queue
from ui import Gui
from server import Server, get_server_list
from threads import Threads
from db_com import DBCom

class Client():
    """Client Client."""

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = Server()
        self.thread_list = Threads(self)
        self.gui_queue = Queue()
        self.user = User('', '', None, '')
        self.gui = Gui(self)
        self.dbcom = DBCom(self)
        if getattr(sys, 'frozen', False):
            # frozen
            self.abs_path = os.path.dirname(sys.executable)
        else:
            # unfrozen
            self.abs_path = os.path.dirname(os.path.realpath(__file__))
        self.save_dir = './savedServers'
        self.ext = '.srv'
        os.chdir(self.abs_path)
        self.server_list = get_server_list(self)
        self.username = None

if __name__ == "__main__":
    CLIENT = Client()
    CLIENT.gui.root.mainloop()
