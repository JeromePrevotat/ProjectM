"""Module to build the Manage Servers Window."""

import tkinter as tk

def build_frames(dialbox):
    """Adds the Frames to the gui."""
    #Window Frame
    dialbox.manage_frame = tk.Frame(dialbox.master_frame)
    dialbox.manage_frame.grid(row=0, column=0)
    #SERVER LIST FRAME
    dialbox.server_list_frame = tk.Frame(dialbox.manage_frame)
    dialbox.server_list_frame.grid(row=0, column=0)
    #SERVER INFOS FRAME
    dialbox.server_infos_frame = tk.Frame(dialbox.manage_frame)
    dialbox.server_infos_frame.grid(row=0, column=1, sticky='N')
    #BUTTON FRAME
    dialbox.button_frame = tk.Frame(dialbox.manage_frame)
    dialbox.button_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

def fill_server_list_frame(dialbox):
    """Adds the Servers List Listbox."""
    #LISTBOX
    dialbox.server_listbox = tk.Listbox(dialbox.server_list_frame, \
    selectmode='single', height=20)
    #ADD ALL SERVER SAVED TO LISTBOX
    for srv in dialbox.gui.client.server_list:
        dialbox.server_listbox.insert(tk.END, srv.name)
    dialbox.server_listbox.grid(row=0, column=0, rowspan=6)

def fill_server_infos_frame(dialbox):
    """Adds Labels and Entries to display the Server Infos."""
    #SERVER NAME
    dialbox.server_name_label = tk.Label(dialbox.server_infos_frame, \
    text=dialbox.gui.res.server_name_label)
    dialbox.server_name_label.grid(row=0, column=1, sticky='W', padx=5)
    dialbox.server_name = tk.StringVar()
    dialbox.server_name_entry = tk.Entry(dialbox.server_infos_frame, \
    textvariable=dialbox.server_name, width=25, state='disabled')
    dialbox.server_name_entry.grid(row=1, column=1, padx=5)
    #ADDRESS
    dialbox.address_label = tk.Label(dialbox.server_infos_frame, \
    text=dialbox.gui.res.address_label)
    dialbox.address_label.grid(row=2, column=1, sticky='W', padx=5)
    dialbox.server_address = tk.StringVar()
    dialbox.address_entry = tk.Entry(dialbox.server_infos_frame, \
    textvariable=dialbox.server_address, width=25, state='disabled')
    dialbox.address_entry.grid(row=3, column=1, padx=5)
    #PORT
    dialbox.port_label = tk.Label(dialbox.server_infos_frame, \
    text=dialbox.gui.res.port_label)
    dialbox.port_label.grid(row=4, column=1, sticky='W', padx=5)
    dialbox.port = tk.StringVar()
    dialbox.port_entry = tk.Entry(dialbox.server_infos_frame, \
    textvariable=dialbox.port, width=25, state='disabled')
    dialbox.port_entry.grid(row=5, column=1, padx=5)

def fill_button_frame(dialbox):
    """Adds Buttons to the gui."""
    #ADD BUTTON
    dialbox.add_button = tk.Button(dialbox.button_frame,    \
    text=dialbox.gui.res.add_server, width=10,              \
    command=lambda: dialbox.gui.callbacks.add(dialbox))
    dialbox.add_button.grid(row=0, column=0)
    #DELETE BUTTON
    dialbox.del_button = tk.Button(dialbox.button_frame,    \
    text=dialbox.gui.res.delete, width=10)
    dialbox.del_button.grid(row=0, column=1)
    #EDIT BUTTON
    dialbox.edit_button = tk.Button(dialbox.button_frame,   \
    text=dialbox.gui.res.edit, width=10,                    \
    command=lambda: dialbox.gui.callbacks.edit(dialbox))
    dialbox.edit_button.grid(row=0, column=2)
    #DONE BUTTON
    dialbox.done_button = tk.Button(dialbox.button_frame,   \
    text=dialbox.gui.res.done, width=10,                    \
    command=lambda: dialbox.gui.callbacks.done(dialbox))
    dialbox.done_button.grid(row=0, column=3)
    #CANCEL BUTTON
    dialbox.cancel_button = tk.Button(dialbox.button_frame, \
    text=dialbox.gui.res.cancel, width=10,                  \
    command=lambda: dialbox.gui.callbacks.cancel(dialbox))
    dialbox.cancel_button.grid(row=0, column=4)
