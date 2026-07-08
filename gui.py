from tkinter.ttk import Style

from create_workbook import Template
import xlsxwriter
from tkinter import *
from tkinter import ttk
import re
import subprocess
import os
from pathlib import Path
import sys
from configparser import ConfigParser
from utility import MenubuttonTooltip, PeriodicTable, Modal

file = open('stdout_err.log', mode='w')
sys.stdout = file
sys.stderr = file

BACKGROUND = '#e6e6e6'
ACTIVE_BACKGROUND = '#5a5a5a'

HIGHLIGHT = '#4a90e2'

parser = ConfigParser()
parser.read('config.ini')

UPPER_LIMIT = parser.getint('Parameters', 'upper_limit')
# PERIODIC_TABLE = None
TEMP_CONFIG = [None]

SAMPLE_COPY = {2: 'duplicate', 3: 'triplicate'}


class App:
    def __init__(self):
        self.RETURN = False
        self.root = Tk()
        self.root.withdraw()
        self.root.iconbitmap('img/logo.ico')

        self.root.title('WORKBOOK TEMPLATE')
        self.root.resizable(False, False)
        self.root.geometry('325x500')

        global PERIODIC_TABLE, MODAL, TEMP_CONFIG

        PERIODIC_TABLE = PeriodicTable(self.root)


        #MODAL.ok()  # call to initially set up the parser in TEMP_CONFIG
        #TEMP_CONFIG.insert(PERIODIC_TABLE)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=4)
        self.root.rowconfigure(2, weight=2)

        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=4)
        self.root.rowconfigure(2, weight=2)

        self.top_frame = Frame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky='ew')
        #self.top_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(34, 14))
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        self.top_frame.rowconfigure(2, weight=1)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.columnconfigure(2, weight=1)

        radio_frame = Frame(self.top_frame)
        radio_frame.grid(row=1, column=2, sticky='nsew')
        radio_frame.rowconfigure(0, weight=1)
        radio_frame.columnconfigure(0, weight=1)
        radio_frame.columnconfigure(1, weight=1)

        request_id_label = Label(self.top_frame, text='Request ID:')
        request_id_label.grid(row=0, column=0, sticky='e')
        self.request_id_entry = Entry(self.top_frame, highlightthickness=1)
        self.request_id_entry.grid(row=0, column=1, sticky='w')

        preset = parser.get('Autofill', 'request')
        self.request_id_entry.bind('<Double-Button-1>', self.__autofill(self.request_id_entry, preset))
        self.__textbox_handler(self.request_id_entry)

        sample = Label(self.top_frame, text='Sample(s):')
        sample.grid(row=1, column=0, sticky='e')
        self.sample_entry = Entry(self.top_frame, highlightthickness=1)
        self.sample_entry.grid(row=1, column=1, sticky='w')

        preset = parser.get('Autofill', 'sample')
        self.sample_entry.bind('<Double-Button-1>', self.__autofill(self.sample_entry, preset))
        self.__textbox_handler(self.sample_entry)

        self.replicates = IntVar()
        radio_button = Radiobutton(radio_frame, text='duplicate', variable=self.replicates, value=2)
        radio_button.grid(row=0, column=0)
        # self.__radio_handler(radio_button)
        parser.read('config.ini')
        i = parser.getint('Parameters', 'max_sample_copies')
        self.radio_button = Radiobutton(radio_frame, text=SAMPLE_COPY.get(i, f'{i}x'), variable=self.replicates, value=i)
        self.radio_button.grid(row=0, column=1)
        # self.__radio_handler(radio_button)
        self.replicates.set(2)

        loi = Label(self.top_frame, text='L.O.I')
        loi.grid(row=2, column=0, sticky='e')
        self.loi = IntVar()
        loi_checkbox = Checkbutton(self.top_frame, variable=self.loi, highlightthickness=1)
        loi_checkbox.grid(row=2, column=1, sticky='w')

        self.middle_frame = Frame(self.root, name='dynamic', bg='SystemButtonFace')
        #self.middle_frame = Frame(self.root, name='dynamic', bg='red')
        self.middle_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.middle_frame.configure(height=120)
        self.middle_frame.grid_propagate(False)
        self.middle_frame.columnconfigure(0, weight=2)
        self.middle_frame.columnconfigure(1, weight=2)
        self.middle_frame.columnconfigure(2, weight=1)
        self.middle_frame.columnconfigure(3, weight=4)

        self.middle_frame.rowconfigure(0, weight=1)
        #self.middle_frame.rowconfigure(0, weight=0)
        self.middle_frame.rowconfigure(1, weight=1)
        self.middle_frame.rowconfigure(2, weight=1)
        self.middle_frame.rowconfigure(3, weight=1)
        # self.middle_frame.rowconfigure(4, weight=1)

        ttk.Separator(self.middle_frame, orient=HORIZONTAL).grid(row=0, columnspan=4, sticky='new')

        self.menu_list = []
        self.check_vars = {}

        self.element_label = Label(self.middle_frame, text='analyte(s)')
        self.element_label.grid(row=0, column=1, sticky='sw', padx=(3, 0))
        #self.element_label.grid(row=0, column=1, sticky='w', pady=(42, 0), padx=(3, 0))

        self.microwave_label = Label(self.middle_frame, text='Microwave')
        self.microwave_label.grid(row=1, column=0, sticky='ne')
        self.microwave_element_frame, self.microwave_sample_frame = self.create_element_and_sample_frame(1,
                                                                                                         name='microwave')

        self.microwave_spinbox = Spinbox(self.middle_frame, from_=1, to=UPPER_LIMIT, width=2, name='microwave')
        self.microwave_spinbox.grid(row=1, column=2, sticky='nw')
        self.microwave_spinbox.config(command=self.__spinbox_handler(self.microwave_spinbox,
                                                                     self.microwave_element_frame,
                                                                     self.microwave_sample_frame, name='microwave'))

        self.katanax_label = Label(self.middle_frame, text='Katanax')
        self.katanax_label.grid(row=2, column=0, sticky='ne')
        self.katanax_element_frame, self.katanax_sample_frame = self.create_element_and_sample_frame(2, color='',
                                                                                                     name='katanax')

        self.katanax_spinbox = Spinbox(self.middle_frame, from_=1, to=UPPER_LIMIT, width=2, name='katanax')
        self.katanax_spinbox.grid(row=2, column=2, sticky='nw')
        self.katanax_spinbox.config(command=self.__spinbox_handler(self.katanax_spinbox,
                                                                   self.katanax_element_frame,
                                                                   self.katanax_sample_frame, name='katanax'))

        self.hotplate_label = Label(self.middle_frame, text='Hotplate')
        self.hotplate_label.grid(row=3, column=0, sticky='ne')
        self.hotplate_element_frame, self.hotplate_sample_frame = self.create_element_and_sample_frame(3, color='',
                                                                                                       name='hotplate')

        self.hotplate_spinbox = Spinbox(self.middle_frame, from_=1, to=UPPER_LIMIT, width=2, name='hotplate')
        self.hotplate_spinbox.grid(row=3, column=2, sticky='nw')
        self.hotplate_spinbox.config(command=self.__spinbox_handler(self.hotplate_spinbox,
                                                                    self.hotplate_element_frame,
                                                                    self.hotplate_sample_frame, name='hotplate'))

        self.sample_entry.bind('<Return>', self.__add_checkbutton(self.menu_list))

        bg = 'red'
        self.bottom_frame = Frame(self.root)
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky='ew')
        #self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(5, 35))

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.submit = Button(self.bottom_frame, text='SUBMIT', command=lambda: self.__submit(), bg=BACKGROUND)
        self.submit.grid(row=0, column=0)

        old_color = '#82DF7C'
        self.submit.bind('<Enter>', lambda _: self.submit.config(bg=ACTIVE_BACKGROUND, fg='white', cursor='hand2'))
        self.submit.bind('<Leave>', lambda _: self.submit.config(bg=BACKGROUND, fg='black', cursor='arrow'))

        self.root.bind('<Control-,>', lambda _: os.startfile('config.ini'))
        self.root.bind('<Alt-c>', lambda _: os.startfile('config.ini'))
        self.root.bind('<F1>', lambda _: os.startfile('config.ini'))

        try:
            self.root.bind('<Control-l>',
                           lambda _: subprocess.Popen([Path(r'C:\Windows\System32\notepad.exe'), 'lot.csv']))
            self.root.bind('<Alt-l>', lambda _: subprocess.Popen([Path(r'C:\Windows\System32\notepad.exe'), 'lot.csv']))

        except Exception as e:
            print(e)

        TEMP_CONFIG.insert(1, (self.radio_button, self.replicates))
        MODAL = Modal(self.root, TEMP_CONFIG)
        self.root.bind('<Double-Button-1>', lambda _: PERIODIC_TABLE.hide())
        self.root.bind('<Control-,>', lambda _: MODAL.show())
        self.root.bind('<Escape>', lambda _: self.root.destroy())

    def __radio_handler(self, radio):
        radio.bind('<Enter>', lambda _: radio.config(fg=HIGHLIGHT))
        radio.bind('<Leave>', lambda _: radio.config(fg='black'))

    @staticmethod
    def __autofill(entry, preset):
        def func(_):
            text = entry.get()
            entry.delete(0, END)
            if text == '':
                entry.insert(0, preset)
            else:
                entry.insert(0, '')
            return 'break'

        return func

    def __textbox_handler(self, entry):
        default = entry.cget('highlightbackground')
        entry.bind('<Enter>', lambda _: entry.config(highlightbackground='#4a90e2'))
        entry.bind('<Leave>', lambda _: entry.config(highlightbackground=default))
        #entry.bind('<Leave>',
                   #lambda _: entry.config(bg='#F0F0F0', highlightbackground=default) if entry == self.root.focus_get()
                   #else entry.config(bg='white', highlightbackground=default))

        entry.bind('<FocusIn>', lambda _: entry.config(highlightcolor='#4a90e2'))
        entry.bind('<FocusOut>', lambda _: entry.config(highlightcolor=default))

        #entry.bind('<FocusIn>', lambda _: entry.config(bg='#F0F0F0', highlightbackground=default))
        #entry.bind('<FocusOut>', lambda _: entry.config(bg='white', highlightbackground=default))

    def __menubutton_handler(self, menubutton):
        # menubutton.bind('<Enter>', lambda _: menubutton.config(activebackground=ACTIVE_BACKGROUND, activeforeground='white', cursor='hand2'))
        menubutton.bind('<Leave>',
                        lambda _: (menubutton.config(bg=BACKGROUND, fg='black', cursor='arrow'), print('leaving')))

    def __unclick(self, menu_list):
        # delete this method
        print('inside unclick')
        for menu in menu_list:
            print(menu.master)
            menu.master.event_generate('<FocusOut>')

    def create_element_and_sample_frame(self, row: int, name, color=''):
        element_frame = Frame(self.middle_frame, bg='SystemButtonFace', name=f'{name}_element')
        element_frame.grid(row=row, column=1, sticky='nsew')

        # spinbox = Spinbox(self.middle_frame, from_=1, to=SPINBOX_TO, width=2, name=name)
        # spinbox.grid(row=row, column=2, sticky='w')

        sample_frame = Frame(self.middle_frame, bg='SystemButtonFace', name=f'{name}_sample')
        sample_frame.grid(row=row, column=3, sticky='nsew')

        entry = Entry(element_frame, name=f'{name}entry_{0}', highlightthickness=1)
        entry.pack(side='top')

        PERIODIC_TABLE.add_textbox(entry)
        entry.bind('<Double-Button-1>', PERIODIC_TABLE.show(entry))

        self.__textbox_handler(entry)

        menubutton = Menubutton(sample_frame, width=9, text='select', name=f'{name}button_{0}', relief='raised',
                                bg=BACKGROUND)
        menubutton.pack(side='top')

        self.__menubutton_handler(menubutton)
        MenubuttonTooltip(menubutton, 'selected sample(s) for digestion')

        menu = Menu(menubutton, tearoff=0)
        self.menu_list.append(menu)  # added initial menu button here
        menubutton.config(menu=menu)

        # spinbox.config(command=self.__spinbox_handler(spinbox, element_frame, sample_frame, name=name))

        return element_frame, sample_frame

    def __add_checkbutton(self, menu_list):
        def func(_):
            self.check_vars = {}
            for menu in menu_list:
                menu.delete(0, 'end')
                for sample in self.__extract_sample_id():
                    if sample == '':
                        continue
                    # change to a dictionary mapping if the key exsist append to dictionary and new key create empty list
                    key = menu.winfo_parent()
                    if key not in self.check_vars:
                        self.check_vars[key] = []

                    var = IntVar(value=1)
                    self.check_vars[key].append(var)
                    menu.add_checkbutton(label=sample, variable=var)

                    # print(self.check_vars)

        return func

    def __extract_sample_id(self):
        match = re.search(r'(\d+)\((\d+)\)', self.sample_entry.get())
        if match:
            sample_id, sample_count = match.groups()
            sample_id = int(sample_id)
            sample_count = int(sample_count)
            samples = [sample_id + i for i in range(sample_count)]
        else:
            samples = re.split(r'[,\s]+', self.sample_entry.get())
        return samples

    def __spinbox_handler(self, spinbox, element_frame, sample_frame, name):
        def func():
            count = int(spinbox.get())
            child_count = len(element_frame.winfo_children())

            if count > child_count:
                for i in range(child_count, count):
                    entry = Entry(element_frame, name=f'{name}entry_{i}', highlightthickness=1)
                    entry.pack(side='top')

                    PERIODIC_TABLE.add_textbox(entry)
                    entry.bind('<Double-Button-1>', PERIODIC_TABLE.show(entry))
                    self.__textbox_handler(entry)

                    button = Menubutton(sample_frame, width=9, text='select', name=f'{name}button_{i}', relief='raised',
                                        bg=BACKGROUND)
                    button.pack(side='top')

                    self.__menubutton_handler(button)
                    MenubuttonTooltip(button, 'selected sample(s) for digestion')

                    menu = Menu(button, tearoff=0)
                    # menu.bind('<Unmap>', lambda _: button.config(relief='raised'))
                    self.menu_list.append(menu)
                    button.config(menu=menu)

                # evoke entry <Return> to force sample updates on new menu_buttons
                self.sample_entry.focus_set()
                self.sample_entry.event_generate('<Return>')

            elif child_count > count:
                for i in reversed(range(count, child_count)):
                    entry = element_frame.nametowidget(f'{name}entry_{i}')
                    entry.destroy()

                    button = sample_frame.nametowidget(f'{name}button_{i}')

                    menu = button.cget('menu')

                    menu = self.root.nametowidget(menu)
                    self.menu_list.remove(menu)

                    button.destroy()

                element_frame.update_idletasks()
                sample_frame.update_idletasks()

        return func

    def __grab_data(self, element_frame, sample_frame):
        element_frame_children = element_frame.winfo_children()
        sample_frame_children = sample_frame.winfo_children()
        samples = self.__extract_sample_id()
        digestion = []

        for entry, menubutton in zip(element_frame_children, sample_frame_children):
            if entry.get() == '':
                continue
            selected_sample = [sample for sample, var in zip(samples, self.check_vars[str(menubutton)]) if
                               var.get() == 1]
            elements = re.split(r'[,\s]+', entry.get())
            digestion.append((elements, selected_sample))

        return digestion

    def __submit(self):
        microwave = self.__grab_data(self.microwave_element_frame, self.microwave_sample_frame)
        katanax = self.__grab_data(self.katanax_element_frame, self.katanax_sample_frame)
        hotplate = self.__grab_data(self.hotplate_element_frame, self.hotplate_sample_frame)

        global TEMP_CONFIG
        temp_parser = TEMP_CONFIG[0]

        parser.read('config.ini')
        #i = parser.getint('Parameters', 'max_sample_copies')
        #self.radio_button.config(text=SAMPLE_COPY.get(i, f'{i}x'), value=i)


        request = self.request_id_entry.get()
        replicates = self.replicates.get()
        loi = self.loi.get()
        url = temp_parser.get('Save', 'save as')

        try:  # this is still required for users that type destination in config file to prevent mistakes
            destination = Path(parser.get('Path', 'directory'))
            if destination.exists():
                url = destination / url
        except Exception as e:
            print(e)

        print(f'path={url}')
        color = temp_parser.get('General', 'calculation')
        sort = bool(temp_parser.getint('General', 'sort'))
        include_expired = temp_parser.getint('Database', 'expired')

        note = temp_parser.get('General', 'note(s)')

        workbook = xlsxwriter.Workbook(url)
        template = Template(workbook, request=request, replicates=replicates, loi=loi, font_color=color)

        for elements, samples in microwave:
            template.add_microwave(elements, samples)

        for elements, samples in katanax:
            template.add_katanax(elements, samples)

        for elements, samples in hotplate:
            template.add_hotplate(elements, samples)

        if sort:
            template.sort_analytes()

        template.add_note(note=note)
        template.create_analysis_worksheet(include_expired=include_expired)
        workbook.close()
        os.startfile(url)

    def run(self):
        self.root.deiconify()
        self.root.mainloop()
