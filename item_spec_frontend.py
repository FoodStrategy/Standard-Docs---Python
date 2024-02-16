from tkinter import*
from tkinter import ttk, messagebox, filedialog
import cover_backend
import item_spec_backend as spec_backend
from datetime import date
from math import floor


class ItemSpec(Toplevel):
    def __init__(self, title, size):
        super().__init__()
        self.setup_window(title, size)
        self.add_menu()

    def add_menu(self):
        self.menu = ItemOptions(self)
        self.menu.grid(column=0, row=0)

    def setup_window(self, title, size):
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')


class ItemOptions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(column=0, row=0, sticky='nsew')
        self.create_widgets()

    def create_widgets(self):
        
        today = date.today().strftime('%B %d, %Y')
        today_formatted =date.today().strftime('%y%m%d')

        you_r_here = ttk.Label(self, text = 'Today is ' + today + \
                               ' [' + today_formatted + ']')
        you_r_here.grid(row=0, column=0, columnspan=2)

        aq_export = ttk.Label(self, text='Excel file exported from AutoQuotes:')
        aq_export.grid(column=0, row=1, sticky=E)
       
        dir_label = ttk.Label(self, text='File to be saved at:')
        dir_label.grid(column=0, row=3, sticky=E)
        
        name_label = ttk.Label(self, text='Save as:')
        name_label.grid(column=0, row=5, sticky=E)

        xl_button = ttk.Button(self, text='Pick Excel File',command=self.xl_pick)
        xl_button.grid(column=0, row=2, sticky=E)
        
        dir_button = ttk.Button(self, text='Pick Directory', command=self.dir_pick)
        dir_button.grid(column=0, row=4, sticky=E)
        
        gen_button = ttk.Button(self, text="Generate", command=lambda: \
                                self.make_spec(self.xl_path.get(),
                                               self.filename.get(),
                                               self.dir_path.get()))
        gen_button.grid(row=8, column = 0, columnspan=2)

        self.xl_path = StringVar()
        self.xl_path.trace_add('write', self.xl_path_callback)
        spreadsheet = ttk.Label(self, textvariable=self.xl_path,\
                                width=55, relief='sunken')
        spreadsheet.grid(column=1, row=1, sticky = 'ew')

        self.dir_path = StringVar()
        self.dir_path.trace_add('write', self.dir_path_callback)
        directory = ttk.Label(self, textvariable=self.dir_path,\
                                width=55, relief='sunken')
        directory.grid(column=1, row=3, sticky='ew')
        
        self.filename = StringVar()
        self.filename.trace_add('write', self.filename_callback)
        self.filename.set(today_formatted + ' Foodservice Section 114000')
        save_as = ttk.Entry(self, textvariable=self.filename)
        save_as.grid(column=1, row=5, sticky='ew')


        pad_config(self, 5)

    def dir_pick(self):
        self.dir_path.set(filedialog.askdirectory())

    def xl_pick(self):
        self.xl_path.set(filedialog.askopenfilename\
                    (filetypes=[('Excel Files', '*.xlsx')]))
        

    def xl_path_callback(self, *args):
        print(self.xl_path.get())

    def dir_path_callback(self, *args):
        print(self.dir_path.get())

    def filename_callback(self, *args):
        print(self.filename.get())

    def make_spec(self, xl_path, filename, save_path):
        spec_backend.main(xl_path, filename, save_path)

def pad_config(self, pad_amt):
    for child in self.winfo_children():
        child.grid_configure(padx=pad_amt, pady=pad_amt)

