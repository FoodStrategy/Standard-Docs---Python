from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import date
import cover_backend

class AreaEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', borderwidth=2)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.area_name = StringVar()
        self.area_name.trace_add("write", self.area_name_callback)
        self.area = ttk.Entry(self, textvariable=self.area_name, width=25)
        self.area.grid(row=0, column=0)

        self.area_abbr = StringVar()
        self.area_abbr.trace_add("write", self.area_abbr_callback)
        self.abbr = ttk.Entry(self, textvariable=self.area_abbr, width=5)
        self.abbr.grid(row=0, column=1, sticky='ne')

        self.columnconfigure(0, weight=1)  
        self.columnconfigure(1, weight=1)  

    def area_name_callback(self, *args):
        print(self.area_name.get())

    def area_abbr_callback(self, *args):
        print(self.area_abbr.get())

class CutCover(Toplevel):
    def __init__(self, title, size):
        super().__init__()
        self.setup_window(title, size)
        self.add_menu()
        
    def add_menu(self):
        menu = CoverOptions(self)
        menu.grid(column=0, row=0)

    def setup_window(self, title, size):
        self.title(title)
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2
        self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')

class CoverOptions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.existing_entries = {}
        self.grid(column=0, row=0, sticky='nsew')
        self.create_widgets()
        
    def create_widgets(self):

        today = date.today().strftime('%B %d, %Y')
        today_formatted = date.today().strftime('%y%m%d')

        self.date_string = StringVar()
        self.date_string.set('Today is ' + today + ' [' + today_formatted + ']')
        you_r_here = ttk.Label(self, textvariable=self.date_string)
        you_r_here.grid(row=0, column=1)
        
        

        info = ttk.Label(self, text='*Information below should correctly autopopulate when you choose a directory.*')
        info.grid(column=1, row=3, sticky=E)

        ttk.Label(self, text='File(s) to be saved at:').grid(column=0, row=2, sticky=E)
        ttk.Label(self, text='Project Location:').grid(column=0, row=1, sticky=E)
        ttk.Button(self, text='Edit', command=self.modal_input_box).grid(row=1, column =2, sticky=E)
        
        self.dir_path = StringVar()
        self.dir_path.trace_add('write', self.dir_path_callback)
        directory = ttk.Label(self, textvariable=self.dir_path, width=55, relief='sunken')
        directory.grid(column=1, row=2, sticky='ew')

        ttk.Button(self, text="Generate Covers", command=self.make_covers).grid(row=20, column=1)
        ttk.Button(self, text='Pick Directory', command=self.dir_pick).grid(column=2, row=2, sticky='sew')
        
        self.area_table = AreaTable(self)
        self.area_table.grid(column=1, row=6, sticky='nsew')

        self.main_buttons = ThreeButtons(self)
        self.main_buttons.grid(column=1, row=13, sticky='nsew')

        self.entry_frame = AreaEntry(self)
        self.entry_frame.grid(column=1, row=12)

        self.status = StringVar()
        self.status.trace_add('write', self.status_callback)
        self.entry_status = ttk.Label(self, textvariable=self.status)
        self.entry_status.grid(column=2, row=12, sticky='nw')

        self.proj_frame = ProjectEntry(self)
        self.proj_frame.grid(column=1, row=4)
        
        self.loc = StringVar()
        self.loc_lbl = ttk.Label(self, textvariable=self.loc, relief='sunken')
        self.loc_lbl.grid(column=1, row=1, sticky='new')

        pad_config(self, 5)
        self.modal_input_box()

        
    def modal_input_box(self):
        self.dlg = InputBox(self, 'Location', "Where is this project located? (i.e. 'Rockville, MD')", (300, 150))
        self.dlg.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.dlg.transient(self)
        self.dlg.wait_visibility()
        self.dlg.grab_set()
        self.dlg.wait_window()
        self.loc.set(self.dlg.loc)
        self.date_string.set(self.date_string.get() + ' | Date on covers: '\
                             + self.dlg.date)

    def dismiss(self):
        self.dlg.grab_release()
        self.dlg.destroy()
    
    def dir_pick(self):
        path = filedialog.askdirectory(title='File(s) to be saved at:')
        self.dir_path.set(path)
        self.proj_frame.proj_num.set(path[path.index('/') + 1:path.index('-') - 1])
        self.proj_frame.job_title.set(path[path.index('-') + 2:path.index('/', 3)])
        
    def dir_path_callback(self, *args):
        print(self.dir_path.get())

    def status_callback(self, *args):
        print(self.status.get())

    def is_unique_entry(self, area_name, area_abbr):
        # Check if the area name or abbreviation already exists
        name_lower = area_name.lower()
        abbr_lower = area_abbr.lower()
        if name_lower in self.existing_entries.values():
            messagebox.showinfo("Duplicate", "This area name already exists.")
            return False
        if abbr_lower in self.existing_entries.keys():
            messagebox.showinfo("Duplicate", "This abbreviation already exists.")
            return False
        # No duplicates found, add to tracking sets and return True
        
        return True

    def make_covers(self):
        ready = True
        err_message = []
        
        TEMPLATE_PATH = r"Q:\Standard Documents\Templates\CUTBOOK COVER.docx"
        
        areas = self.existing_entries

        if len(areas) == 0:
            ready = False
            err_message.append('Area List')
        
        proj_num = self.proj_frame.proj_num.get()

        if proj_num is None or proj_num == '':
            ready = False
            err_message.append('Project Number')
            
        proj_title = self.proj_frame.job_title.get()

        if proj_title is None or proj_title == '':
            ready = False
            err_message.append('Project Title')
        
        directory = self.dir_path.get()

        if directory is None or directory == '':
            ready = False
            err_message.append('Directory')
        
        cover_date = self.dlg.date

        if cover_date is None or cover_date == '':
            ready = False
            err_message.append('Cover Date')
            
        location = self.dlg.loc

        if location is None or location == '':
            ready = False
            err_message.append('Location')

        if not ready:
            err = 'The following fields are missing information: '
            for i in err_message:
                err += i + ', '
            err = err[:len(err) - 2]
            print(err)
            messagebox.showerror(message=err, title='Error')
        else:
            cover_backend.main(areas, proj_num, proj_title, directory, location, cover_date)
            messagebox.showinfo(title='Saved!', message='Files saved to: {}'.format(directory))
class AreaTable(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='sunken', borderwidth=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.table = ttk.Treeview(self, columns=('area', 'abbr'), show='headings')
        self.table['selectmode'] = 'extended'
        self.table.heading('area', text='Area')
        self.table.heading('abbr', text ='Abbr.')
        self.table.grid(row=0, column=0, sticky='news')
            
class ThreeButtons(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.user_input = False
        self.confirming = False
        self.name_holder = ''
        self.abbr_holder = ''
        super().__init__(parent, borderwidth=2)
        self.create_widgets()

    def create_widgets(self):

        self.new = ttk.Button(self, text='Add', command=self.new_area)
        self.new.grid(row=0, column=0, sticky='nsew')

        self.edit = ttk.Button(self, text='Edit', command=self.edit_area)
        self.edit.grid(row=0, column=1, sticky='nsew', padx=5)

        self.remove = ttk.Button(self, text='Remove', command=self.remove_area)
        self.remove.grid(row=0, column=2, sticky='nsew')

        self.columnconfigure(0, weight=1)  
        self.columnconfigure(1, weight=1)  
        self.columnconfigure(2, weight=1)  

    def new_area(self):

        area_name = self.parent.entry_frame.area_name.get()
        area_abbr = self.parent.entry_frame.area_abbr.get()

        if area_name is None or area_name == '':
            messagebox.showerror("Error", "Area name cannot be empty.")
            return
        if len(area_abbr) > 3:
            messagebox.showerror("Error", "Area abbreviation cannot be longer than 3 characters.")
            return
        if not self.confirming:
            if self.parent.is_unique_entry(area_name, area_abbr):
                self.parent.existing_entries[area_abbr.lower()] = area_name.lower()
                inserted = self.parent.area_table.table.insert('', 'end', values=(area_name, area_abbr))
                print(self.parent.area_table.table.item(inserted))
                self.parent.entry_frame.area_name.set('')
                self.parent.entry_frame.area_abbr.set('')
              
    def edit_area(self):
        selected_item = self.parent.area_table.table.selection()
        

        if len(selected_item) == 1:
            self.parent.area_table.table['selectmode'] = 'none'
            self.parent.status.set('Editing...')
            area_name, area_abbr = self.parent.area_table.table.item(selected_item, "values")
            self.name_holder = area_name
            self.abbr_holder = area_abbr
            self.parent.entry_frame.area_name.set(area_name)
            self.parent.entry_frame.area_abbr.set(area_abbr)
            self.edit['text'] = 'Confirm'
            self.edit['command'] = lambda: self.confirm_edit(area_name, area_abbr)
            self.remove['command'] = ''
            self.new['text'] = 'Cancel'
            self.new['command'] = self.cancel_edit
        elif len(selected_item) > 1:
            messagebox.showinfo('Edit', "Only one item may be edited at a time")
        else:
            messagebox.showinfo('Edit', "Please select an area to edit")

    def cancel_edit(self):
        self.parent.area_table.table['selectmode'] = 'extended'
        self.edit['text'] = 'Edit'
        self.edit['command'] = self.edit_area
        self.remove['command'] = self.remove_area
        self.new['text'] = 'New'
        self.new['command'] = self.new_area
        self.confirming = False
        self.parent.entry_frame.area_name.set('')
        self.parent.entry_frame.area_abbr.set('')
        self.name_holder = ''
        self.abbr_holder = ''

    def confirm_edit(self, area_name, area_abbr):
        self.confirm_area(area_name, area_abbr)
        self.parent.area_table.table['selectmode'] = 'extended'
        self.edit['text'] = 'Edit'
        self.edit['command'] = self.edit_area
        self.remove['command'] = self.remove_area
        self.confirming = False
        self.new['text'] = 'New'
        self.new['command'] = self.new_area
        self.parent.status.set('')

    def confirm_area(self, area_name, area_abbr):
        tree = self.parent.area_table.table
        index = tree.index(tree.selection()[0])

        old_name = self.name_holder
        new_name = self.parent.entry_frame.area_name.get()

        old_abbr = self.abbr_holder
        new_abbr = self.parent.entry_frame.area_abbr.get()
        
        if old_abbr != new_abbr and old_name == new_name:
            print('1')
            del self.parent.existing_entries[old_abbr.lower()]
            self.parent.existing_entries[new_abbr.lower()] = old_name.lower()
            tree.insert('', index, values=(old_name, new_abbr))
            tree.delete(tree.selection())
            self.parent.entry_frame.area_name.set('')
            self.parent.entry_frame.area_abbr.set('')
            self.name_holder = ''
            self.abbr_holder = ''
        elif old_abbr == new_abbr and old_name != new_name:
            print('2')
            self.parent.existing_entries[old_abbr.lower()] = new_name.lower()
            tree.insert('', index, values=(new_name, old_abbr))
            tree.delete(tree.selection())
            self.parent.entry_frame.area_name.set('')
            self.parent.entry_frame.area_abbr.set('')
            self.name_holder = ''
            self.abbr_holder = ''
        elif old_abbr != new_abbr and old_name != new_name:
            print('3')
            del self.parent.existing_entries[old_abbr.lower()]
            self.parent.existing_entries[new_abbr.lower()] = new_name.lower()
            tree.insert('', index, values=(new_name, new_abbr))
            tree.delete(tree.selection())
            self.parent.entry_frame.area_name.set('')
            self.parent.entry_frame.area_abbr.set('')
            self.name_holder = ''
            self.abbr_holder = ''
        else:
            messagebox.showinfo(title='Oops!', message='Edit the area, abbreviation,'\
                            + 'both fields, or cancel the edit to continue editing'\
                            + 'the rest of your list.') 

    def remove_area(self):
        selected_items = self.parent.area_table.table.selection()

        if selected_items:
            for selected_item in selected_items:
                area_name, area_abbr = self.parent.area_table.table.item(selected_item, "values")
                area_name_lower = area_name.lower()
                area_abbr_lower = area_abbr.lower()
                self.parent.area_table.table.delete(selected_item)
                self.parent.existing_entries.pop(area_abbr_lower)
        else:
            messagebox.showinfo("Remove", "Please select an item to remove.")

class ProjectEntry(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, relief='groove', borderwidth=2)
        self.create_widgets()

    def create_widgets(self):
        job_lbl_lbl = ttk.Label(self, text='Project: ', relief='flat')
        job_lbl_lbl.grid(column=0, row=0, sticky='nw')

        self.job_title = StringVar()
        self.job_title.trace_add('write', self.job_title_callback)
        job_label = ttk.Entry(self, textvariable=self.job_title, width=35)
        job_label.grid(column=1, row=0, sticky='new')

        proj_num_lbl = ttk.Label(self, text='Number: ', relief='flat')
        proj_num_lbl.grid(column=2, row=0, sticky='new')

        self.proj_num = StringVar()
        self.proj_num.trace_add('write', self.proj_num_callback)
        proj_label = ttk.Entry(self, textvariable=self.proj_num, width=15)
        proj_label.grid(column=3, row=0, sticky='ne')

        self.columnconfigure(0, weight=1)  
        self.columnconfigure(1, weight=1)  
        self.columnconfigure(2, weight=1)  
        self.columnconfigure(3, weight=1)  

    def proj_num_callback(self, *args):
        print(self.proj_num.get())
        
    def job_title_callback(self, *args):
        print(self.job_title.get())

class InputBox(Toplevel):
    def __init__(self, parent, title, prompt, size):
        super().__init__(parent)
        self.setup_window(title, size)
        self.create_widgets(prompt)
        self.loc = None
        self.date = None

    def setup_window(self, title, size):
        self.title(title)
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2
        self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')

    def create_widgets(self, prompt):
        ttk.Label(self, text=prompt).grid(row=0, column=0, sticky='nsew')
        self.location_var = StringVar()
        self.location_entry = ttk.Entry(self, textvariable=self.location_var)
        self.location_entry.grid(row=1, column=0, sticky='nsew')
        ttk.Button(self, text='OK', command=self.on_ok).grid(row=4, column=0, sticky='nsew')


        ttk.Label(self, text='Enter a date for covers to be generated')\
                        .grid(row=2, column=0, sticky='nsew')
        self.date_var = StringVar()
        self.date_entry = ttk.Entry(self, textvariable=self.date_var)
        self.date_entry.grid(row=3, column=0, sticky='nsew')
        pad_config(self, 2)

    def on_ok(self):
        self.loc = self.location_var.get().strip()
        self.date = self.date_var.get() 
        self.destroy()

def destroy():
    self.parent.destroy()

def ok(input_frame):
    input_frame.parent.loc = input_frame.entry.get()
    input_frame.parent.cover_date = input_frame.entry_2.get()
    input_frame.parent.destroy()

def cancel(input_frame):
    input_frame.parent.loc = None
    input_frame.parent.destroy()

def pad_config(widget, pad_amt):
    for child in widget.winfo_children():
        child.grid_configure(padx=pad_amt, pady=pad_amt)
