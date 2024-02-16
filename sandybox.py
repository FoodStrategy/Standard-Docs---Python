import tkinter as tk
from tkinter import ttk
from math import floor

def on_variable_change(*args):
    # This function will be called whenever the variable changes
    entry_var.set(entry_var.get())

root = tk.Tk()

# Create a StringVar and link it to an Entry widget
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var)
entry.pack(padx=10, pady=10)

# Attach the callback function to the variable
entry_var.trace_add("write", on_variable_change)

# Function to update the variable and trigger the callback
def update_variable():
    new_value = entry_var.get() + "X"
    entry_var.set(new_value)

# Button to update the variable
update_button = tk.Button(root, text="Update Variable", command=update_variable)
update_button.pack(pady=10)

root.mainloop()
