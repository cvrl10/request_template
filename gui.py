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
from utility import ToolTip, PeriodicTable

file = open('stdout_err.log', mode='w')
#sys.stdout = file
#sys.stderr = file

BACKGROUND = '#e6e6e6'
ACTIVE_BACKGROUND = '#5a5a5a'

HIGHLIGHT = '#4a90e2'

parser = ConfigParser()
parser.read('config.ini')

SPINBOX_TO = parser.getint('Parameters', 'spinbox_to')
PERIODIC_TABLE = None

class App:
    def __init__(self):
        self.RETURN = False
        self.root = Tk()

        global PERIODIC_TABLE
        PERIODIC_TABLE = PeriodicTable(self.root)

        self.root.iconbitmap('img/logo.ico')

        self.root.title('workbook_creator')
        self.root.resizable(False, False)
        self.root.geometry('325x500')

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=4)
        self.root.rowconfigure(2, weight=2)

        self.top_frame = Frame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky='ew')
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

        self.__textbox_handler(self.request_id_entry)

        sample = Label(self.top_frame, text='Sample(s):')
        sample.grid(row=1, column=0, sticky='e')
        self.sample_entry = Entry(self.top_frame, highlightthickness=1)
        self.sample_entry.grid(row=1, column=1, sticky='w')

        self.__textbox_handler(self.sample_entry)

        self.replicates = IntVar()
        r = Radiobutton(radio_frame, text='duplicate', variable=self.replicates, value=2)
        r.grid(row=0, column=0)
        #self.__radio_handler(r)
        parser.read('config.ini')
        r = Radiobutton(radio_frame, text='triplicate', variable=self.replicates, value=parser.getint('Parameters', 'triplicate'))
        r.grid(row=0, column=1)
        #self.__radio_handler(r)
        self.replicates.set(2)

        loi = Label(self.top_frame, text='L.O.I')
        loi.grid(row=2, column=0, sticky='e')
        self.loi = IntVar()
        loi_checkbox = Checkbutton(self.top_frame, variable=self.loi, highlightthickness=1)
        loi_checkbox.grid(row=2, column=1, sticky='w')


        self.middle_frame = Frame(self.root, name='dynamic')
        self.middle_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.middle_frame.configure(height=120)
        self.middle_frame.grid_propagate(False)
        self.middle_frame.columnconfigure(0, weight=2)
        self.middle_frame.columnconfigure(1, weight=2)
        self.middle_frame.columnconfigure(2, weight=1)
        self.middle_frame.columnconfigure(3, weight=4)

        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.rowconfigure(1, weight=1)
        self.middle_frame.rowconfigure(2, weight=1)
        self.middle_frame.rowconfigure(3, weight=1)
        #self.middle_frame.rowconfigure(4, weight=1)

        ttk.Separator(self.middle_frame, orient=HORIZONTAL).grid(row=0, columnspan=4, sticky='new')

        self.menu_list = []
        self.check_vars = {}

        self.element_label = Label(self.middle_frame, text='analyte(s)')
        self.element_label.grid(row=0, column=1, sticky='w')

        self.microwave_label = Label(self.middle_frame, text='Microwave')
        self.microwave_label.grid(row=1, column=0, sticky='ne')
        self.microwave_element_frame, self.microwave_sample_frame = self.create_element_and_sample_frame(1, name='microwave')

        self.microwave_spinbox = Spinbox(self.middle_frame, from_=1, to=SPINBOX_TO, width=2, name='microwave')
        self.microwave_spinbox.grid(row=1, column=2, sticky='nw')
        self.microwave_spinbox.config(command=self.__spinbox_handler(self.microwave_spinbox,
                                                                     self.microwave_element_frame,
                                                                     self.microwave_sample_frame, name='microwave'))

        self.katanax_label = Label(self.middle_frame, text='Katanax')
        self.katanax_label.grid(row=2, column=0, sticky='ne')
        self.katanax_element_frame, self.katanax_sample_frame = self.create_element_and_sample_frame(2, color='', name='katanax')

        self.katanax_spinbox = Spinbox(self.middle_frame, from_=1, to=SPINBOX_TO, width=2, name='katanax')
        self.katanax_spinbox.grid(row=2, column=2, sticky='nw')
        self.katanax_spinbox.config(command=self.__spinbox_handler(self.katanax_spinbox,
                                                                     self.katanax_element_frame,
                                                                     self.katanax_sample_frame, name='katanax'))

        self.hotplate_label = Label(self.middle_frame, text='Hotplate')
        self.hotplate_label.grid(row=3, column=0, sticky='ne')
        self.hotplate_element_frame, self.hotplate_sample_frame = self.create_element_and_sample_frame(3, color='', name='hotplate')

        self.hotplate_spinbox = Spinbox(self.middle_frame, from_=1, to=SPINBOX_TO, width=2, name='hotplate')
        self.hotplate_spinbox.grid(row=3, column=2, sticky='nw')
        self.hotplate_spinbox.config(command=self.__spinbox_handler(self.hotplate_spinbox,
                                                                     self.hotplate_element_frame,
                                                                     self.hotplate_sample_frame, name='hotplate'))

        self.sample_entry.bind('<Return>', self.__add_checkbutton(self.menu_list))

        bg = 'red'
        self.bottom_frame = Frame(self.root)
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky='ew')

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.submit = Button(self.bottom_frame, text='SUBMIT', command=lambda: self.__submit(), bg=BACKGROUND)
        self.submit.grid(row=0, column=0)

        old_color = '#82DF7C'
        self.submit.bind('<Enter>', lambda _: self.submit.config(bg=ACTIVE_BACKGROUND, fg='white', cursor='hand2'))
        self.submit.bind('<Leave>', lambda _: self.submit.config(bg=BACKGROUND, fg='black', cursor='arrow'))

        self.root.bind('<Control-comma>', lambda _: os.startfile('config.ini'))
        self.root.bind('<Alt-c>', lambda _: os.startfile('config.ini'))
        self.root.bind('<F1>', lambda _: os.startfile('config.ini'))

        try:
            self.root.bind('<Control-l>', lambda _: subprocess.Popen([Path(r'C:\Windows\System32\notepad.exe'), 'lot.csv']))
            self.root.bind('<Alt-l>', lambda _: subprocess.Popen([Path(r'C:\Windows\System32\notepad.exe'), 'lot.csv']))

        except Exception as e:
            print(e)

        #self.root.bind_all('<ButtonRelease-1>', lambda _: self.root.after(10, self.__unclick(self.menu_list)))

    def __radio_handler(self, radio):
        radio.bind('<Enter>', lambda _: radio.config(fg=HIGHLIGHT))
        radio.bind('<Leave>', lambda _: radio.config(fg='black'))

    def __textbox_handler(self, entry):
        default = entry.cget('highlightbackground')
        entry.bind('<Enter>', lambda _: entry.config(highlightbackground='#4a90e2'))
        entry.bind('<Leave>', lambda _: entry.config(highlightbackground=default))

        entry.bind('<FocusIn>', lambda _: entry.config(highlightcolor='#4a90e2'))
        entry.bind('<FocusOut>', lambda _: entry.config(highlightcolor=default))

    def __menubutton_handler(self, menubutton):
        #menubutton.bind('<Enter>', lambda _: menubutton.config(activebackground=ACTIVE_BACKGROUND, activeforeground='white', cursor='hand2'))
        menubutton.bind('<Leave>', lambda _: (menubutton.config(bg=BACKGROUND, fg='black', cursor='arrow'), print('leaving')))


    def __unclick(self, menu_list):
        #delete this method
        print('inside unclick')
        for menu in menu_list:
            print(menu.master)
            menu.master.event_generate('<FocusOut>')



    def create_element_and_sample_frame(self, row: int, name, color=''):
        element_frame = Frame(self.middle_frame, bg='', name=f'{name}_element')
        element_frame.grid(row=row, column=1, sticky='nsew')

        #spinbox = Spinbox(self.middle_frame, from_=1, to=SPINBOX_TO, width=2, name=name)
        #spinbox.grid(row=row, column=2, sticky='w')

        sample_frame = Frame(self.middle_frame, bg=color, name=f'{name}_sample')
        sample_frame.grid(row=row, column=3, sticky='nsew')

        entry = Entry(element_frame, name=f'{name}entry_{0}', highlightthickness=1)
        entry.pack(side='top')

        PERIODIC_TABLE.add_textbox(entry)
        entry.bind('<Double-Button-1>', PERIODIC_TABLE.show(entry))

        self.__textbox_handler(entry)

        menubutton = Menubutton(sample_frame, width=9, text='select', name=f'{name}button_{0}', relief='raised', bg=BACKGROUND)
        menubutton.pack(side='top')

        #menubutton.bind('<Enter>', lambda _: menubutton.config(activebackground=ACTIVE_BACKGROUND, cursor='hand2'))
        #menubutton.bind('<Leave>', lambda _: menubutton.config(bg='SystemButtonFace', cursor='arrow'))
        self.__menubutton_handler(menubutton)
        ToolTip(menubutton, 'selected sample(s) for digestion', position='e', offset=5)

        menu = Menu(menubutton, tearoff=0)
        #menu.bind('<<MenuSelect>>', lambda _: menubutton.config(relief='sunken', background=ACTIVE_BACKGROUND, foreground='white'))
        #menu.bind('<FocusOut>', lambda _: (menubutton.config(relief='raised', background=BACKGROUND, foreground='black'),print('FocusOut')))
        #menu.bind('<Unmap>', lambda _: menubutton.config(relief='raised', background=BACKGROUND, foreground='black'))
        #menu.bind('<Unmap>', lambda _: (menubutton.config(relief='raised', background=BACKGROUND, foreground='black'), print('FocusOut')))
        self.menu_list.append(menu)  # added initial menu button here
        menubutton.config(menu=menu)

        #spinbox.config(command=self.__spinbox_handler(spinbox, element_frame, sample_frame, name=name))

        return element_frame, sample_frame

    def __add_checkbutton(self, menu_list):
        def func(_):
            self.check_vars = {}
            for menu in menu_list:
                menu.delete(0, 'end')
                for sample in self.__extract_sample_id():
                    if sample == '':
                        continue
                    #change to a dictionary mapping if the key exsist append to dictionary and new key create empty list
                    key = menu.winfo_parent()
                    if key not in self.check_vars:
                        self.check_vars[key] = []

                    var = IntVar(value=1)
                    self.check_vars[key].append(var)
                    menu.add_checkbutton(label=sample, variable=var)

                    #print(self.check_vars)
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
            #print(f'child_count {child_count}')
            if count > child_count:
                for i in range(child_count, count):
                    entry = Entry(element_frame, name=f'{name}entry_{i}', highlightthickness=1)
                    entry.pack(side='top')

                    PERIODIC_TABLE.add_textbox(entry)
                    entry.bind('<Double-Button-1>', PERIODIC_TABLE.show(entry))
                    self.__textbox_handler(entry)

                    button = Menubutton(sample_frame, width=9, text='select', name=f'{name}button_{i}', relief='raised', bg=BACKGROUND)
                    button.pack(side='top')

                    self.__menubutton_handler(button)
                    ToolTip(button, 'selected sample(s) for digestion', position='e', offset=5)

                    menu = Menu(button, tearoff=0)
                    #menu.bind('<Unmap>', lambda _: button.config(relief='raised'))
                    self.menu_list.append(menu)
                    button.config(menu=menu)
                #evoke entry <Return> to force sample updates on new menu_buttons
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
                    #print(f'menu is: {menu}')

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
            selected_sample = [sample for sample, var in zip(samples, self.check_vars[str(menubutton)]) if var.get() == 1]
            elements = re.split(r'[,\s]+', entry.get())
            #print(f'elements: {elements}')
            digestion.append((elements, selected_sample))
        return digestion

    def __submit(self):
        microwave = self.__grab_data(self.microwave_element_frame, self.microwave_sample_frame)
        katanax = self.__grab_data(self.katanax_element_frame, self.katanax_sample_frame)
        hotplate = self.__grab_data(self.hotplate_element_frame, self.hotplate_sample_frame)

        COPY = self.replicates.get()
        loi = self.loi.get()
        url = 'master_workbook.xlsx'
        try:
            parser.read('config.ini')
            destination = Path(parser.get('Path', 'directory'))
            if destination.exists():
                url = destination/url
        except Exception as e:
            print(e)

        print(f'path={url}')
        workbook = xlsxwriter.Workbook(url)
        template = Template(workbook, self.request_id_entry.get(), COPY, loi=loi)

        for elements, samples in microwave:
            template.add_microwave(elements, samples)

        for elements, samples in katanax:
            template.add_katanax(elements, samples)

        for elements, samples in hotplate:
            template.add_hotplate(elements, samples)

        template.create_analysis_worksheet()
        workbook.close()
        os.startfile(url)


    def run(self):
        self.root.mainloop()

