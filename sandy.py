import tkinter as tk
from tkinter import ttk

def add_item():
    # Add an item to the Treeview
    tree.insert('', 'end', text='Canvas')

def replace_selected_item():
    selected = tree.selection()

    # Check if an item is selected
    if selected:
        # Get the index of the selected item
        index = tree.index(selected[0])

        # Remove the selected item
        tree.delete(selected[0])

        # Insert a new item at the same position
        tree.insert('', index, text='Tree')

# Create the main window
root = tk.Tk()
root.title("Treeview Example")

# Create a Treeview widget
tree = ttk.Treeview(root)
tree.pack()

# Create buttons for adding and replacing items
add_button = ttk.Button(root, text="Add Item", command=add_item)
add_button.pack()

replace_button = ttk.Button(root, text="Replace Selected Item", command=replace_selected_item)
replace_button.pack()

# Run the application
root.mainloop()
