from tkinter import *
from tkinter import ttk
import re

class App:
    def __init__(self):
        self.root = Tk()

        self.root.geometry('325x250')

        self.root.columnconfigure(0, weight=1)#
        self.root.columnconfigure(1, weight=1)#
        self.root.columnconfigure(2, weight=1)#

        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=4)
        self.root.rowconfigure(2, weight=2)

        self.top_frame = Frame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
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


        request = Label(self.top_frame, text='Request ID:')
        request.grid(row=0, column=0, sticky='e')
        request_entry = Entry(self.top_frame)
        request_entry.grid(row=0, column=1, sticky='w')
        sample = Label(self.top_frame, text='Sample(s):')
        sample.grid(row=1, column=0, sticky='e')
        self.sample_entry = Entry(self.top_frame)
        self.sample_entry.grid(row=1, column=1, sticky='w')
        self.sample_entry.bind('<Key>', self.__extract_sample_id)

        self.replicates = IntVar()
        Radiobutton(radio_frame, text='duplicate', variable=self.replicates, value=2).grid(row=0, column=0)
        Radiobutton(radio_frame, text='triplicate', variable=self.replicates, value=3).grid(row=0, column=1)
        self.replicates.set(2)

        loi = Label(self.top_frame, text='L.O.I')
        loi.grid(row=2, column=0, sticky='e')
        check = IntVar()
        loi_checkbox = Checkbutton(self.top_frame, variable=check)
        loi_checkbox.grid(row=2, column=1, sticky='w')

        self.middle_frame = Frame(self.root, bg='pink')
        self.middle_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.middle_frame.columnconfigure(0, weight=2)
        self.middle_frame.columnconfigure(1, weight=2)
        self.middle_frame.columnconfigure(2, weight=1)
        self.middle_frame.columnconfigure(3, weight=4)

        self.element_label = Label(self.middle_frame, text='element(s)')
        self.element_label.grid(row=0, column=1, sticky='w')

        self.microwave_label = Label(self.middle_frame, text='Microwave')
        self.microwave_label.grid(row=1, column=0, sticky='e')
        self.element_frame = Frame(self.middle_frame,bg='black')
        self.element_frame.grid(row=1, column=1, sticky='nsew')

        self.microwave_spinbox = Spinbox(self.middle_frame, from_=1, to=10, width=2)
        self.microwave_spinbox.grid(row=1, column=2, sticky='w')

        #self.microwave_combobox = ttk.Combobox(self.middle_frame, values=[])
        #self.microwave_combobox.grid(row=1, column=3, sticky='w')

        #self.microwave_listbox = Listbox(self.middle_frame, selectmode='multiple')
        #self.microwave_listbox.grid(row=1, column=3, sticky='w')

        self.microwave_menu = Menubutton(self.middle_frame, width=9)
        self.microwave_menu.grid(row=1, column=3, sticky='w')
        self.menu = Menu(self.microwave_menu, tearoff=0)
        self.microwave_menu.config(menu=self.menu)

        self.katanax_label = Label(self.middle_frame, text='Katanax')
        self.katanax_label.grid(row=2, column=0, sticky='e')
        self.katanax_frame = Frame(self.middle_frame, bg='purple')
        self.katanax_frame.grid(row=2, column=1, sticky='nsew')

        self.hotplate_label = Label(self.middle_frame, text='Hotplate')
        self.hotplate_label.grid(row=3, column=0, sticky='e')
        self.hotplate_frame = Frame(self.middle_frame, bg='orange')
        self.hotplate_frame.grid(row=3, column=1, sticky='nsew')
        #make those frames not grid

        self.bottom_frame = Frame(self.root, bg='red')
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew')

    def __extract_sample_id(self, _):
        samples = re.split(r'[,\s]+', self.sample_entry.get())
        #self.microwave_combobox['values'] = samples
        for sample in samples:
            #self.microwave_listbox.insert(END, sample)
            pass
        print(samples)

    def __create_menu_checkbox(self):
        i = self.menu.index('end')
        for i in range(self.menu.index('end')):
            pass
        samples = re.split(r'[,\s]+', self.sample_entry.get())
        for sample in samples:
            self.menu.add_checkbutton(label=sample)

    def run(self):
        self.root.mainloop()




app = App()
app.run()