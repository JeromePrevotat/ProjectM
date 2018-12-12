"""Custom DialogBox Module."""

import tkinter as tk

class Dialog(tk.Toplevel):
    """Custom DialogBox Class."""

    def __init__(self, gui, body_type, title=None):
        self.gui = gui
        self.body_type = body_type
        tk.Toplevel.__init__(self, self.gui.root)
        #Associate with a parent window
        self.transient(self.gui.root)
        self.resizable(False, False)
        if title:
            self.title(title)
        self.parent = self.gui.root
        self.return_value = None
        self.master_frame = tk.Frame(self)
        self.body_build()
        self.master_frame.grid(row=0, column=0, padx=5, pady=5)
        self.grab_set()
        self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" %    (self.gui.root.winfo_rootx() + 50,
                                     self.gui.root.winfo_rooty() + 50))
        self.initial_focus.focus_get()
        ########################################################################
        # THREAD UPDATE ENTRIES ON LISTBOX SELECTION                           #
        ########################################################################
        if self.body_type == 'manage_server' or self.body_type == 'connect':
            self.gui.client.thread_list.create_thread(self.body_type, self)
        #Wait for the dialogbox to be validated or closed
        self.wait_window(self)

    def body_build(self):
        """Method to create the Body of the DialogBox."""
        if self.body_type == 'connect':
            self.build_connect()
        if self.body_type == 'manage_server':
            self.build_manage_server()
        if self.body_type == 'change_pseudo':
            self.build_change_pseudo()
        if self.body_type == 'change_password':
            self.build_change_password()
        if self.body_type == 'server_infos':
            self.build_server_infos()

    def build_manage_server(self):
        """Build the Manage Servers Window."""
        import manage_server
        manage_server.build_frames(self)
        manage_server.fill_server_list_frame(self)
        manage_server.fill_server_infos_frame(self)
        manage_server.fill_button_frame(self)

    def build_connect(self):
        """Build the Connect Window."""
        import manage_server
        manage_server.build_frames(self)
        manage_server.fill_server_list_frame(self)
        manage_server.fill_server_infos_frame(self)
        #BUTTONS
        self.button_done = tk.Button(self.button_frame, \
        text=self.gui.res.server_connect, width=8, \
        command=lambda: self.gui.callbacks.done(self))
        self.button_done.grid(row=1, column=1)
        self.button_cancel = tk.Button(self.button_frame, \
        text=self.gui.res.cancel, width=8, \
        command=lambda: self.gui.callbacks.cancel(self))
        self.button_cancel.grid(row=1, column=0)

    def build_change_pseudo(self):
        """Build the Change Pseudo Window."""
        import change_username
        change_username.set_var(self)
        change_username.build_frames(self)
        change_username.build_labels(self)
        change_username.build_entry(self)
        change_username.fill_button_frame(self)

    def build_change_password(self):
        """Build the Change Password Window."""
        import change_pass
        change_pass.set_var(self)
        change_pass.build_frames(self)
        change_pass.build_labels(self)
        change_pass.build_entry(self)
        change_pass.fill_button_frame(self)

    def build_server_infos(self):
        """Build the Server Infos Window."""
        #SERVER NAME
        self.server_name_label = tk.Label(self.master_frame, \
        text=self.gui.res.server_name_label)
        self.server_name_label.grid(row=0, column=0, sticky='W')
        self.server_name = tk.StringVar()
        self.server_name_entry = tk.Entry(self.master_frame, \
        textvariable=self.server_name, width=25, state='disabled')
        self.server_name_entry.grid(row=0, column=1)
        #ADRESS
        self.adress_label = tk.Label(self.master_frame, \
        text=self.gui.res.adress_label)
        self.adress_label.grid(row=1, column=0, sticky='W')
        self.server_adress = tk.StringVar()
        self.adress_entry = tk.Entry(self.master_frame, \
        textvariable=self.server_adress, width=25, state='disabled')
        self.adress_entry.grid(row=1, column=1)
        #PORT
        self.port_label = tk.Label(self.master_frame, text=self.gui.res.port_label)
        self.port_label.grid(row=2, column=0, sticky='W')
        self.port = tk.StringVar()
        self.port_entry = tk.Entry(self.master_frame, textvariable=self.port, \
        width=25, state='disabled')
        self.port_entry.grid(row=2, column=1)

    def cancel(self, event=None):
        """Command to Quit and Destroy the DialogBox."""
        self.parent.focus_set()
        self.destroy()
