"""Callbacks Buttons Commands"""

import tkinter as tk
from tkinter import messagebox as mBox

import bcrypt


from server import Server, get_server_list, remove_server

import timeformat as tFormat
import dialogbox
import encoding
import sms_code


class Callbacks():
    """"Callbacks Buttons Commands Class."""

    def __init__(self, ui):
        self.gui = ui
        self.dialbox = None

    def _quit(self):
        """Quit Command."""
        self.gui.root.quit()
        self.gui.root.destroy()
        exit()

    def key_press_return(self, _event=None):
        """Default behaviour of Keypress Return."""
        if (isinstance(self.gui.main_frame.focus_get(), tk.Button) and \
        self.gui.main_frame.focus_get().config()['command'] != ''):
            self.gui.main_frame.focus_get().invoke()
        else:
            self.gui.log_in_button.invoke()

    def send_msg(self, gui):
        """Send a Message."""
        msg = gui.msg_input.get(1.0, tk.END)
        if msg not in ['', '\n']:
            encoded_msg = encoding.encode_msg(msg)
            gui.client.socket.send(encoded_msg)
            gui.msg_input.delete(1.0, tk.END)
            self.gui.msg_output.config(state='normal')
            self.gui.msg_output.insert(tk.INSERT, 'You at ' + \
            tFormat.get_time_format(self.gui) + ' :\n\t' + msg + '\n')
            self.gui.msg_output.config(state='disabled')
        return 'break'

    def change_pseudo(self):
        """Creates a Dialbox allowing to change the use Username."""
        self.dialbox = dialogbox.Dialog(self.gui, 'change_pseudo')

    def change_password(self):
        """Creates a Dialbox allowing to change the user Password."""
        self.dialbox = dialogbox.Dialog(self.gui, 'change_password')

    def server_infos(self):
        """Creates a Dialbox displaying Server Informations."""
        self.dialbox = dialogbox.Dialog(self.gui, 'server_infos')

    def manage_server(self):
        """Creates a Dialbox allowing Servers Management."""
        self.dialbox = dialogbox.Dialog(self.gui, 'manage_server')

    def add(self, dialbox):
        """Allows creation of a new Server."""
        dialbox.edit = True
        dialbox.server_name_entry.config(state='normal')
        dialbox.address_entry.config(state='normal')
        dialbox.port_entry.config(state='normal')
        dialbox.server_name_entry.delete(0, tk.END)
        dialbox.address_entry.delete(0, tk.END)
        dialbox.port_entry.delete(0, tk.END)

    def edit(self, dialbox):
        """Allows Edition of Server Fields."""
        dialbox.edit = True
        dialbox.server_name_entry.config(state='normal')
        dialbox.address_entry.config(state='normal')
        dialbox.port_entry.config(state='normal')

    def cancel(self, dialbox):
        """Cancel Command."""
        dialbox.parent.focus_set()
        dialbox.destroy()

    def remove(self, dialbox):
        """Removes a Server from the Server Listbox."""
        server_name = dialbox.server_name_entry.get()
        remove_server(server_name, self.gui.client.abs_path, \
        self.gui.client.save_dir, self.gui.client.ext)
        self.gui.client.server_list = get_server_list(self.gui.client)
        dialbox.cancel(dialbox)

    def done_manage(self, dialbox):
        """Done Callback for the Manage Servers Dialbox."""
        server_name = dialbox.server_name_entry.get()
        server_address = dialbox.address_entry.get()
        server_port = dialbox.port_entry.get()
        if server_name and server_address and server_port:
            new_server = Server(server_name, server_address, server_port)
            remove_server(server_name, self.gui.client.abs_path, \
            self.gui.client.save_dir, self.gui.client.ext)
            Server.save_server(new_server, self.gui.client.abs_path, \
            self.gui.client.save_dir, self.gui.client.ext)
            #ADD NEW SERVER TO server_list
            self.gui.client.server_list = get_server_list(self.gui.client)
            #ADD NEW SERVER TO LISTBOX
            dialbox.server_listbox.insert(tk.END, server_name)
        dialbox.server_name_entry.delete(0, tk.END)
        dialbox.address_entry.delete(0, tk.END)
        dialbox.port_entry.delete(0, tk.END)
        dialbox.server_name_entry.config(state='disabled')
        dialbox.address_entry.config(state='disabled')
        dialbox.port_entry.config(state='disabled')
        dialbox.cancel(dialbox)

    def done_change_pseudo(self, dialbox):
        """Done Callback for the Change Pseudo Dialbox."""
        if self.gui.client.dbcom.identify(dialbox.old_pseudo_str.get(), \
        dialbox.password_str.get()):
            if len(dialbox.new_pseudo_str.get()) >= 4:
                if self.gui.client.dbcom.check_username(dialbox.new_pseudo_str.get()):
                    self.gui.client.dbcom.update_username(dialbox.old_pseudo_str.get(), \
                    dialbox.new_pseudo_str.get())
                    mBox.showinfo(self.gui.res.pseudo_changed, \
                    self.gui.res.pseudo_changed)
                    dialbox.cancel(dialbox)
                else:
                    dialbox.output_label.configure(text=self.gui.res.pseudo_taken, fg='red')
            else:
                dialbox.output_label.configure(text=self.gui.res.pseudo_too_short, fg='red')
        else:
            dialbox.output_label.configure(text=self.gui.res.bad_name_pass_combo, fg='red')

    def done_change_password(self, dialbox):
        """Done Callback for the Change Password Dialbox."""
        if self.gui.client.dbcom.identify(dialbox.username_str.get(), \
        dialbox.old_password_str.get()):
            if dialbox.new_password_str1.get() == dialbox.new_password_str2.get():
                if len(dialbox.new_password_str1.get()) >= 4:
                    new_salt = bcrypt.gensalt()
                    while not self.gui.client.dbcom.check_salt(new_salt):
                        new_salt = bcrypt.gensalt()
                    new_password = bcrypt.hashpw(dialbox.new_password_str1.get().encode(), new_salt)
                    self.gui.client.dbcom.update_password(dialbox.username_str.get(), \
                    new_salt, new_password)
                    mBox.showinfo(self.gui.res.password_changed, \
                    self.gui.res.password_changed)
                    dialbox.cancel(dialbox)
                else:
                    dialbox.output_label.configure(text=self.gui.res.password_too_short, fg='red')
            else:
                dialbox.output_label.configure(text=self.gui.res.password_non_identical, fg='red')
        else:
            dialbox.output_label.configure(text=self.gui.res.bad_name_pass_combo, fg='red')

    def done_connect_to(self, dialbox):
        """Done Callback for the Connect to a Server Dialbox."""
        server_name = dialbox.server_name_entry.get()
        server_address = dialbox.address_entry.get()
        server_port = dialbox.port_entry.get()
        if (server_name != "" and                   \
        server_address != "" and                    \
        server_port != "" and                       \
        self.gui.client.username is not None and    \
        self.gui.client.username != ''):
            self.gui.client.server.connect_to(server_name, \
            (server_address, int(server_port)), self.gui.client)
            dialbox.cancel(dialbox)
        else:
            mBox.showwarning(self.gui.res.server_connect_empty_title, \
            self.gui.res.server_connect_empty_msg)

    def done(self, dialbox):
        """Done Command."""
        #SERVERS MANAGEMENT
        if dialbox.body_type == 'manage_server':
            self.done_manage(dialbox)
        #PSEUDO CHANGE
        if dialbox.body_type == 'change_pseudo':
            self.done_change_pseudo(dialbox)
        #PASSWORD CHANGE
        if dialbox.body_type == 'change_password':
            self.done_change_password(dialbox)
        #CONNECT TO SERVER
        if dialbox.body_type == 'connect':
            self.done_connect_to(dialbox)

    def server_connect(self):
        """Creates a Dialbox to connect to a server."""
        self.dialbox = dialogbox.Dialog(self.gui, 'connect')

    def check_entry(self):
        """Check if the Entries content obey certain Regex."""
        if self.gui.client.dbcom.check_username(self.gui.username_entry.get()) \
            and self.gui.client.dbcom.check_mail(self.gui.mail_entry.get()) \
            and self.gui.client.dbcom.check_phone_number(self.gui.number_entry.get()):
            self.ask_code()

    def ask_code(self):
        """Send then Ask the user for the Confirmation Code sent by SMS."""
        #Send the Confirmation Code
        correct_code = sms_code.send_code(self.gui.number_str.get())
        #Clean the UI
        self.gui.username_label.grid_remove()
        self.gui.username_entry.grid_remove()
        self.gui.password_label.grid_remove()
        self.gui.password_entry.grid_remove()
        self.gui.mail_label.grid_remove()
        self.gui.mail_entry.grid_remove()
        self.gui.number_label.grid_remove()
        self.gui.number_entry.grid_remove()
        #Confirmation Code Field
        self.gui.confirmation_code_str = tk.StringVar()
        self.gui.confirmation_code_label = tk.Label(self.gui.infos_frame, \
        text=self.gui.res.confirmation_code, pady=5)
        self.gui.confirmation_code_entry = tk.Entry(self.gui.infos_frame, \
        textvariable=self.gui.confirmation_code_str)
        self.gui.confirmation_code_label.grid(row=0, column=0)
        self.gui.confirmation_code_entry.grid(row=1, column=0)
        #Output Label
        self.gui.output_label = tk.Label(self.gui.infos_frame)
        self.gui.output_label.grid(row=2, column=0)
        #Confirm command
        self.gui.log_in_button.config(text=self.gui.res.done, \
        command=lambda: self.confirm_code(correct_code))

    def confirm_code(self, correct_code):
        """Check if the SMS Confirmation Code Input is Correct."""
        if self.gui.confirmation_code_str.get() == correct_code:
            self.new_user()
        else:
            self.gui.output_label.configure(text='Wrong Code', fg='red')

    def new_user(self):
        """Create a new User to the ProjectM Database."""
        username = self.gui.username_entry.get()
        salt = bcrypt.gensalt()
        while not self.gui.client.dbcom.check_salt(salt):
            salt = bcrypt.gensalt()
        password = bcrypt.hashpw(self.gui.password_entry.get().encode(), salt)
        email = self.gui.mail_entry.get()
        phone_number = self.gui.number_entry.get()
        self.gui.client.dbcom.add_user(username, salt, password, email, phone_number)
        self.gui.build_log_in_ui()

    def log_in(self):
        """Try to log in to the ProjectM Server."""
        username = self.gui.username_entry.get()
        password = self.gui.password_entry.get()
        success = False
        try:
            success = self.gui.client.dbcom.identify(username, password)
        except:
            self.gui.error_label.config(text=self.gui.res.connection_to_projectm_failed)
            return
        if success:
        #if self.gui.client.dbcom.identify(username, password):
            self.gui.client.username = username
            self.gui.build_main_ui()
        else:
            self.gui.error_label.config(text=self.gui.res.bad_name_pass_combo)
