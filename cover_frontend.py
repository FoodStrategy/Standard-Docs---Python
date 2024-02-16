from tkinter import*
from tkinter import ttk, messagebox, filedialog
import cover_backend
from datetime import date

def pad_config(self, pad_amt):
    for child in self.winfo_children():
        child.grid_configure(padx=pad_amt, pady=pad_amt)   

class AreaEntry(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, relief='groove', borderwidth=2)
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

        self.columnconfigure(0, weight=1)  # Left column
        self.columnconfigure(1, weight=1)  # Right column

        pad_config(self, 1)

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
        self.menu = CoverOptions(self)
        self.menu.grid(column=0, row=0)

    def setup_window(self, title, size):
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

class CoverOptions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.existing_entries = {}
        
        self.grid(column=0, row=0, sticky='nsew')
        self.create_widgets()

    def create_widgets(self):

        today = date.today().strftime('%B %d, %Y')
        today_formatted = date.today().strftime('%y%m%d')

        you_r_here = ttk.Label(self, text = 'Today is ' + today + \
                               ' [' + today_formatted + ']')
        you_r_here.grid(row=0, column=1)

        info = ttk.Label(self, text='*Information below should correctly '\
                         + 'autopopulate when you choose a directory.*')
        info.grid(column=1, row=3, sticky=E)

        dir_label = ttk.Label(self, text='File(s) to be saved at:')
        dir_label.grid(column=0, row=2, sticky=E)

        location_label = ttk.Label(self, text='Project Location:')
        location_label.grid(column=0, row=1, sticky=E)
        
        self.dir_path = StringVar()
        self.dir_path.trace_add('write', self.dir_path_callback)
        directory = ttk.Label(self, textvariable=self.dir_path,\
                                width=55, relief='sunken')
        directory.grid(column=1, row=2, sticky='ew')

        gen_button = ttk.Button(self, text="Generate Covers", command=self.make_covers)
        gen_button.grid(row=20, column = 1, columnspan=2)

        dir_button = ttk.Button(self, text='Pick Directory',
                                command=self.dir_pick)
        dir_button.grid(column=0, row=3, sticky='sew')
        
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
        self.loc_lbl = ttk.Label(self, textvariable=self.loc,\
                                 relief='sunken')
        self.loc_lbl.grid(column=1, row=1, sticky='new')
        
        pad_config(self, 5)

        self.dlg = InputBox('Location', "Where is this project located? (i.e. 'Rockville, MD')", (300, 150))
        self.dlg.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.dlg.transient(self)   # dialog window is related to main
        self.dlg.wait_visibility() # can't grab until window appears, so we wait
        self.dlg.grab_set()        # ensure all input goes to our window
        self.dlg.wait_window()

        self.loc.set(self.dlg.loc)

    def dismiss(self):
        self.dlg.grab_release()
        self.dlg.destroy()
    
    def dir_pick(self):
        path = filedialog.askdirectory()
        self.dir_path.set(path)
        self.proj_frame.proj_num.set(path[path.index('/') + 1:path.index('-') - 1])
        self.proj_frame.job_title.set(path[path.index('-') + 2:path.index('/', 3)])
        
    def dir_path_callback(self, *args):
        print(self.dir_path.get())

    def status_callback(self, *args):
        print(self.status.get())

    def filename_callback(self, *args):
        print(self.filename.get())
        
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

        TEMPLATE_PATH = r"Q:\Programming\Standard Documents\Templates\Cutbook Cover.docx"
        areas = self.existing_entries
        proj_num = self.proj_frame.proj_num.get()
        proj_title = self.proj_frame.job_title.get()
        directory = self.dir_path.get()
        
        cover_date = self.dlg.cover_date
        location = self.dlg.loc
        print(location)
        
        cover_backend.main(TEMPLATE_PATH, areas, proj_num, proj_title, directory, location, cover_date)

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
        super().__init__(parent, borderwidth=2)
        self.create_widgets()

    def create_widgets(self):

        self.new = ttk.Button(self, text='Add', command=self.new_area)
        self.new.grid(row=0, column=0, sticky='nsew')

        self.edit = ttk.Button(self, text='Edit', command=self.edit_area)
        self.edit.grid(row=0, column=1, sticky='nsew', padx=5)

        self.remove = ttk.Button(self, text='Remove', command=self.remove_area)
        self.remove.grid(row=0, column=2, sticky='nsew')

        self.columnconfigure(0, weight=1)  # Left column
        self.columnconfigure(1, weight=1)  # Center column
        self.columnconfigure(2, weight=1)  # Right column

    def new_area(self):
        area_name = self.parent.entry_frame.area_name.get().strip()
        area_abbr = self.parent.entry_frame.area_abbr.get().strip()

        if area_name is None or area_name == '':
            messagebox.showerror("Error", "Area name cannot be empty.")
            return
        if len(area_abbr) > 3:
            messagebox.showerror("Error", "Area abbreviation cannot be longer than 3 characters.")
            return
        if not self.confirming:
            if self.parent.is_unique_entry(area_name, area_abbr):
                # No duplicates found, insert the new area
                self.parent.existing_entries[area_abbr.lower()] = area_name.lower()
                inserted = self.parent.area_table.table.insert('', 'end', values=(area_name, area_abbr))
                print(self.parent.area_table.table.item(inserted))
                self.parent.entry_frame.area_name.set('')
                self.parent.entry_frame.area_abbr.set('')
        else:
            tree = self.parent.area_table.table
            index = tree.index(tree.selection()[0])
            tree.delete(tree.selection())
            self.parent.existing_entries[area_abbr.lower()] = area_name.lower()
            tree.insert('', index, values=(area_name, area_abbr))
            print(f"Added new area: {area_name}, abbreviation: {area_abbr}")
            self.parent.entry_frame.area_name.set('')
            self.parent.entry_frame.area_abbr.set('')
   
                
    def edit_area(self):
        
        selected_item = self.parent.area_table.table.selection()
        

        if len(selected_item) == 1:
            self.parent.area_table.table['selectmode'] = 'none'
            self.parent.status.set('Editing...')
            area_name, area_abbr = self.parent.area_table.table.item(selected_item,
                                                                         "values")
            self.parent.entry_frame.area_name.set(area_name)
            self.parent.entry_frame.area_abbr.set(area_abbr)
            self.edit['text'] = 'Confirm'
            self.edit['command'] = self.confirm_edit
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

    def confirm_edit(self):
        self.confirming = True
        self.new_area()
        self.parent.area_table.table['selectmode'] = 'extended'
        self.edit['text'] = 'Edit'
        self.edit['command'] = self.edit_area
        self.remove['command'] = self.remove_area
        self.confirming = False
        self.new['text'] = 'New'
        self.new['command'] = self.new_area
        self.parent.status.set('')
        
    def remove_area(self):
        selected_items = self.parent.area_table.table.selection()

        # Check if there is at least one selected item
        if selected_items:
            for selected_item in selected_items:
                # Get the values of the selected item
                area_name, area_abbr = self.parent.area_table.table.item(selected_item,
                                                                         "values")
                area_name_lower = area_name.lower()
                area_abbr_lower = area_abbr.lower()

                # Confirm before removal
                self.parent.area_table.table.delete(selected_item)
                    
                # Remove from the dictionary tracking the entries
                self.parent.existing_entries.pop(area_abbr_lower)
        else:
            messagebox.showinfo("Remove", "Please select an item to remove.")

class ProjectEntry(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, relief='groove', borderwidth=2)
        self.create_widgets()

    def create_widgets(self):

        job_lbl_lbl = ttk.Label(self, text='Project: ', relief='groove')
        job_lbl_lbl.grid(column=0, row=0, sticky='nw')

        self.job_title = StringVar()
        self.job_title.trace_add('write', self.job_title_callback)
        job_label = ttk.Entry(self, textvariable=self.job_title, width=35)
        job_label.grid(column=1, row=0, sticky='new')

        proj_num_lbl = ttk.Label(self, text='Number: ', relief='groove')
        proj_num_lbl.grid(column=2, row=0, sticky='new')

        self.proj_num = StringVar()
        self.proj_num.trace_add('write', self.proj_num_callback)
        proj_label = ttk.Entry(self, textvariable=self.proj_num, width=15)
        proj_label.grid(column=3, row=0, sticky='ne')

        self.columnconfigure(0, weight=1)  # Left column
        self.columnconfigure(1, weight=1)  # Center column
        self.columnconfigure(2, weight=1)  # Left column
        self.columnconfigure(3, weight=1)  # Center column

        pad_config(self, 1)

    def proj_num_callback(self, *args):
        print(self.proj_num.get())
        
    def job_title_callback(self, *args):
        print(self.job_title.get())

        pad_config(self, 3)    


class InputBox(Toplevel):

    def __init__(self, title, prompt, size):
        super().__init__()

        self.loc = None
        self.cover_date = None
        self.setup_window(title, size)
        self.add_menu(prompt)

    def add_menu(self, prompt):
        self.menu = InputBoxOptions(self, prompt)
        self.menu.grid(column=0, row=0)

    def setup_window(self, title, size):
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')

class InputBoxOptions(ttk.Frame):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.parent = parent
        self.grid(column=0, row=0, sticky='nsew')
        self.create_widgets(prompt)

    def create_widgets(self, prompt):

        label = ttk.Label(self, text=prompt)
        label.grid(row=0, column=0, sticky='nsew')

        label_2 = ttk.Label(self, text='Enter the date you would like on the covers')
        label_2.grid(row=2, column=0, sticky='nsew')

        self.entry_2 = ttk.Entry(self)
        self.entry_2.grid(row=3, column=0, sticky='nsew')

        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=0, sticky='nsew')

        self.main_buttons = TwoButtons(self)
        self.main_buttons.grid(column=0, row=12, sticky='nsew')

        pad_config(self, 2)
        
def destroy():
    self.parent.destroy()
        

class TwoButtons(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.user_input = False
        super().__init__(parent, borderwidth=2)
        self.create_widgets()

    def create_widgets(self):

        self.ok = ttk.Button(self, text='Ok', command=lambda: ok(self.parent))
        self.ok.grid(row=0, column=0, sticky='nsew')

        self.cancel = ttk.Button(self, text='Cancel', command=cancel)
        self.cancel.grid(row=0, column=1, sticky='nsew', padx=5)

        self.columnconfigure(0, weight=1)  # Left column
        self.columnconfigure(1, weight=1)  # Center column
        self.columnconfigure(2, weight=1)  # Right column

def ok(input_frame):
    input_frame.parent.loc = input_frame.entry.get()
    input_frame.parent.cover_date = input_frame.entry_2.get()
    input_frame.parent.destroy()

def cancel(input_frame):
    input_frame.parent.loc = None
    input_frame.parent.destroy()


                
