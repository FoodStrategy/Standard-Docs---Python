from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import date
from math import floor
import item_spec_backend as backend  # Assuming you have this module

def menubar_config(win):
    win.option_add('*tearOff', FALSE)
    menubar = Menu(win)
    win['menu'] = menubar

    menu_file = Menu(menubar)
    menu_edit = Menu(menubar)

    menubar.add_cascade(menu=menu_file, label='File')
    menubar.add_cascade(menu=menu_edit, label='Edit')

    menu_file.add_command(label='New')
    menu_file.add_command(label='Open...')
    menu_file.add_cascade(label='Open Recent...')
    menu_file.add_command(label='Close')

    sysmenu = Menu(menubar, name='system')
    menubar.add_cascade(menu=sysmenu)

class HomeScreen(Tk):
    def __init__(self, title, size):
        super().__init__()
        menubar_config(self)
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(floor(size[0]/2), floor(size[1]/2))

        frame1 = init_frame(self)
        
        itemspec = ttk.Button(frame1, text="Item Spec", command=lambda: start_ispec(self))\
                   .grid(column=0, row=0, sticky=(W,E))
        ttk.Button(frame1, text="General Spec")\
                           .grid(column=0, row=1, sticky=(W,E))
        ttk.Button(frame1, text="Cutbook Covers")\
                           .grid(column=0, row=2, sticky=(W,E))
        ttk.Button(frame1, text="Cutbook")\
                           .grid(column=0, row=3, sticky=(W,E))

        ttk.Label(frame1, text='Creates itemized specification from AQ excel file')\
                          .grid(column=1, row=0, sticky=W)
        ttk.Label(frame1, text='Creates general specification with desired header/footer from word doc')\
                          .grid(column=1, row=1, sticky=W)
        ttk.Label(frame1, text='Creates cutbook covers - *Feature not yet implemented*')\
                          .grid(column=1, row=2, sticky=W)
        ttk.Label(frame1, text='Creates a cutbook - *Feature not yet implemented*')\
                          .grid(column=1, row=3, sticky=W)

        pad_config(frame1)
        self.mainloop()

def start_ispec(win):
    item_spec_instance = ItemSpec(win)
    win.withdraw()
    win.item_spec_instance = item_spec_instance

class ItemSpec(Tk):

    def header_pick(win):
        win.word_path.set(filedialog.askopenfilename(filetypes=[('Word Files', '*.docx')]))

    def aq_pick(win):
        win.xl_path.set(filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')]))
    
    def __init__(self, parent):
        super().__init__()
        self.geometry('600x600')
        self.minsize(600, 300)
        self.title('Generate Itemized Specification')
        self.parent = parent
        self.filename = StringVar()
        self.word_path = StringVar()
        self.xl_path = StringVar()

        frame1 = init_frame(self)

        ttk.Label(frame1, text='Today Is:')\
                          .grid(column=0, row=0, sticky=E)
        ttk.Label(frame1, text='Save As:')\
                          .grid(column=0, row=3, sticky=E)
        ttk.Label(frame1, text='Excel file from AQ:')\
                          .grid(column=0, row=1, sticky=E, columnspan=1)
        ttk.Label(frame1, text='Take header from Word Doc:')\
                          .grid(column=0, row=3, sticky=E, columnspan=1)
        ttk.Label(frame1, text='Save As:')\
                          .grid(column=0, row=5, sticky='e')

        xl_pick = ttk.Button(frame1, text='Pick Excel File', command=lambda: aq_pick(self))\
                  .grid(column=0, row=2, sticky=E)
        word_pick = ttk.Button(frame1, text='Pick Word Doc', command=lambda: header_pick(self))\
                    .grid(column=0, row=4, sticky=E)

        ttk.Button(frame1, text='Generate', command=lambda:\
                   backend.main(fr"{self.xl_path.get()}", fr"{self.word_path.get()}", self.filename))\
                           .grid(column=0, row=6, columnspan=2)

        today = date.today().strftime('%B %d, %Y')
        today_formatted = date.today().strftime('%y%m%d')

        self.filename.trace_add('write', self.my_callback)
        self.filename.set(today_formatted + ' Foodservice Section 114000')
        save_as = ttk.Entry(frame1, textvariable=self.filename, width=50)
        save_as.grid(column=1, row=5)

        ttk.Label(frame1, text=today + ' - [' + today_formatted + ']').grid(row=0, column=1, sticky='w')

        word_path_label = ttk.Label(frame1, textvariable=self.word_path, relief="sunken").grid(row=3, column=1, sticky='we')      
        xl_path_label = ttk.Label(frame1, textvariable=self.xl_path, relief="sunken").grid(row=1, column=1, sticky='we',)

        pad_config(frame1)
        self.lift()
        
    def my_callback(self, *args):
        print("Variable changed:{}".format(self.filename.get()))


def init_frame(window):
    frame = ttk.Frame(window, padding="3 3 12 12")
    frame.grid(column=0, row=0, sticky=(N,W,E,S))
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(1, weight=1)
    return frame

def pad_config(frame):
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

HomeScreen('Document Generator', (600, 600))
