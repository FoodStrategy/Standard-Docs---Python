from tkinter import *
from tkinter import ttk, messagebox, filedialog
import item_spec_backend as spec_backend
import item_spec_frontend as spec_frontend
from datetime import date
from math import floor
import cover_frontend

HOME_SIZE = (500,200)
COVER_WINDOW_SIZE = (650, 550)
ITEM_WINDOW_SIZE = (650, 500)

class Home(Tk):
    def __init__(self, title, size):
        super().__init__()
        self.setup_window(title, size)
        self.add_menu()


    def setup_window(self, title, size):
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

    def add_menu(self):
        self.menu = HomeMenu(self)
        self.menu.grid(row=0, column=0)
        
        '''self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)'''

class HomeMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):

        self.itemspec = ttk.Button(self, text="Item Spec",\
                                   command=lambda: self.item_spec(self.parent))
        self.itemspec.grid(column=0, row=0, sticky='we')                      

        self.genspec = ttk.Button(self, text="General Spec")
        self.genspec.grid(column=0, row=1, sticky='we')

        self.covers = ttk.Button(self, text="Cutbook Covers",\
                                 command=lambda: self.cut_covers(self.parent))
        self.covers.grid(column=0, row=2, sticky='we')
        
        self.cutbook = ttk.Button(self, text='Cutbook')
        self.cutbook.grid(column=0, row=3, sticky='we')

        self.item_desc = ttk.Label(self, text='Item Specification')
        self.item_desc.grid(column=1, row=0, sticky='we')
        
        self.gen_desc = ttk.Label(self, text='General Specification')
        self.gen_desc.grid(column=1, row=1, sticky='we')

        self.cover_desc = ttk.Label(self, text='Cutbook Cover(s)')
        self.cover_desc.grid(column=1, row=2, sticky='we')

        self.cutbook_desc = ttk.Label(self, text='Cutbook')
        self.cutbook_desc.grid(column=1, row=3, sticky='we')
        
        pad_config(self, 5)

    def item_spec(self, parent):
        parent.withdraw()
        win = spec_frontend.ItemSpec('Item Specification', ITEM_WINDOW_SIZE)
        win.lift()
        
    def cut_covers(self, parent):
        self.parent.withdraw()
        win = cover_frontend.CutCover('Cutbook Covers', COVER_WINDOW_SIZE)
        win.lift()



def pad_config(self, pad_amt):
    for child in self.winfo_children():
        child.grid_configure(padx=pad_amt, pady=pad_amt)   

if __name__ == "__main__":
  
    app = Home('Document Generator', HOME_SIZE)
    app.lift()
    app.mainloop()
