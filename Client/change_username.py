"""Module to build the gui of the Change Username Dialbox."""

import tkinter as tk

def build_frames(dialbox):
    """Add Frames to the gui."""
    #Buttons Frame
    dialbox.button_frame = tk.Frame(dialbox.master_frame)
    dialbox.button_frame.grid(row=3, column=1)
    #Output Frame
    dialbox.output_frame = tk.Frame(dialbox.master_frame)
    dialbox.output_frame.grid(row=4, column=0, columnspan=2)

def build_labels(dialbox):
    """Add Labels to the gui."""
    #Input Fields
    dialbox.old_pseudo_label = tk.Label(dialbox.master_frame, \
    text=dialbox.gui.res.old_pseudo_label)
    dialbox.new_pseudo_label = tk.Label(dialbox.master_frame, \
    text=dialbox.gui.res.new_pseudo_label)
    dialbox.password_label = tk.Label(dialbox.master_frame, \
    text=dialbox.gui.res.password_label)
    dialbox.old_pseudo_label.grid(row=0, column=0)
    dialbox.new_pseudo_label.grid(row=1, column=0)
    dialbox.password_label.grid(row=2, column=0)
    #Output Label
    dialbox.output_label = tk.Label(dialbox.output_frame, wraplength=190)
    dialbox.output_label.grid(row=0, column=0)

def build_entry(dialbox):
    """Add Entries to the gui."""
    dialbox.old_pseudo_entry = tk.Entry(dialbox.master_frame, \
    textvariable=dialbox.old_pseudo_str, width=20)
    dialbox.new_pseudo_entry = tk.Entry(dialbox.master_frame, \
    textvariable=dialbox.new_pseudo_str, width=20)
    dialbox.password_entry = tk.Entry(dialbox.master_frame, \
    textvariable=dialbox.password_str, width=20, show='*')
    dialbox.old_pseudo_entry.grid(row=0, column=1)
    dialbox.new_pseudo_entry.grid(row=1, column=1)
    dialbox.password_entry.grid(row=2, column=1)

def fill_button_frame(dialbox):
    """Add Buttons to the gui."""
    dialbox.button_done = tk.Button(dialbox.button_frame, text='Done', width=8, \
    command=lambda: dialbox.gui.callbacks.done(dialbox))
    dialbox.button_done.grid(row=1, column=1)
    dialbox.button_cancel = tk.Button(dialbox.button_frame, text='Cancel', width=8, \
    command=lambda: dialbox.gui.callbacks.cancel(dialbox))
    dialbox.button_cancel.grid(row=1, column=0)

def set_var(dialbox):
    """Initialize Variables."""
    dialbox.old_pseudo_str = tk.StringVar()
    dialbox.new_pseudo_str = tk.StringVar()
    dialbox.password_str = tk.StringVar()
    if len(dialbox.gui.client.username) >= 5:
        dialbox.old_pseudo_str.set(dialbox.gui.client.username)
