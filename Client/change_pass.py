"""Module to build the gui of the Change Password Dialbox."""

import tkinter as tk

def set_var(dialbox):
    """Initialize variables."""
    dialbox.username_str = tk.StringVar()
    dialbox.old_password_str = tk.StringVar()
    dialbox.new_password_str1 = tk.StringVar()
    dialbox.new_password_str2 = tk.StringVar()

def build_frames(dialbox):
    """Add Frames to gui."""
    dialbox.button_frame = tk.Frame(dialbox.master_frame)
    dialbox.button_frame.grid(row=4, column=1)
    dialbox.output_frame = tk.Frame(dialbox.master_frame)
    dialbox.output_frame.grid(row=5, column=0, columnspan=2)

def build_labels(dialbox):
    """Add Labels to gui."""
    #Input Label
    dialbox.username_label = tk.Label(dialbox.master_frame, \
    text=dialbox.gui.res.username_label)
    dialbox.old_password_label1 = tk.Label(dialbox.master_frame, \
    text=dialbox.gui.res.old_password_label)
    dialbox.new_password_label1 = tk.Label(dialbox.master_frame, \
    text=dialbox.gui.res.new_password_label)
    dialbox.new_password_label2 = tk.Label(dialbox.master_frame, \
    text=dialbox.gui.res.new_password_label)
    dialbox.username_label.grid(row=0, column=0)
    dialbox.old_password_label1.grid(row=1, column=0)
    dialbox.new_password_label1.grid(row=2, column=0)
    dialbox.new_password_label2.grid(row=3, column=0)
    #Output Label
    dialbox.output_label = tk.Label(dialbox.output_frame, wraplength=190)
    dialbox.output_label.grid(row=0, column=0)

def build_entry(dialbox):
    """Add Entries to gui."""
    dialbox.username_entry = tk.Entry(dialbox.master_frame, \
    textvariable=dialbox.username_str, width=20)
    dialbox.old_password_entry = tk.Entry(dialbox.master_frame, \
    textvariable=dialbox.old_password_str, width=20, show='*')
    dialbox.new_password_entry1 = tk.Entry(dialbox.master_frame, \
    textvariable=dialbox.new_password_str1, width=20, show='*')
    dialbox.new_password_entry2 = tk.Entry(dialbox.master_frame, \
    textvariable=dialbox.new_password_str2, width=20, show='*')
    dialbox.username_entry.grid(row=0, column=1)
    dialbox.old_password_entry.grid(row=1, column=1)
    dialbox.new_password_entry1.grid(row=2, column=1)
    dialbox.new_password_entry2.grid(row=3, column=1)

def fill_button_frame(dialbox):
    """Add Buttons to gui."""
    dialbox.button_done = tk.Button(dialbox.button_frame, text='Done', width=8, \
    command=lambda: dialbox.gui.callbacks.done(dialbox))
    dialbox.button_done.grid(row=0, column=1)
    dialbox.button_cancel = tk.Button(dialbox.button_frame, text='Cancel', width=8, \
    command=lambda: dialbox.gui.callbacks.cancel(dialbox))
    dialbox.button_cancel.grid(row=0, column=0)
