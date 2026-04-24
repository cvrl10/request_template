from create_template import Template
import xlsxwriter
from tkinter import *
from tkinter import ttk
import re

class App:
    def __init__(self):
        self.root = Tk()

        self.root.title('template_creator')
        self.root.geometry('325x250')
        #self.root.geometry('325x500')

        self.root.columnconfigure(0, weight=1)#
        self.root.columnconfigure(1, weight=1)#
        self.root.columnconfigure(2, weight=1)#

        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=4)
        self.root.rowconfigure(2, weight=3)

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

        request_id_label = Label(self.top_frame, text='Request ID:')
        request_id_label.grid(row=0, column=0, sticky='e')
        self.request_id_entry = Entry(self.top_frame)
        self.request_id_entry.grid(row=0, column=1, sticky='w')
        sample = Label(self.top_frame, text='Sample(s):')
        sample.grid(row=1, column=0, sticky='e')
        self.sample_entry = Entry(self.top_frame)
        self.sample_entry.grid(row=1, column=1, sticky='w')

        self.replicates = IntVar()
        Radiobutton(radio_frame, text='duplicate', variable=self.replicates, value=2).grid(row=0, column=0)
        Radiobutton(radio_frame, text='triplicate', variable=self.replicates, value=3).grid(row=0, column=1)
        self.replicates.set(2)

        loi = Label(self.top_frame, text='L.O.I')
        loi.grid(row=2, column=0, sticky='e')
        self.loi = IntVar()
        loi_checkbox = Checkbutton(self.top_frame, variable=self.loi)
        loi_checkbox.grid(row=2, column=1, sticky='w')

        self.middle_frame = Frame(self.root, bg='pink')
        self.middle_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.middle_frame.columnconfigure(0, weight=2)
        self.middle_frame.columnconfigure(1, weight=2)
        self.middle_frame.columnconfigure(2, weight=1)
        self.middle_frame.columnconfigure(3, weight=4)

        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.rowconfigure(1, weight=1)
        self.middle_frame.rowconfigure(2, weight=1)
        self.middle_frame.rowconfigure(3, weight=1)

        self.menu_list = []
        self.check_vars = {}

        self.element_label = Label(self.middle_frame, text='element(s)')
        self.element_label.grid(row=0, column=1, sticky='w')

        self.microwave_label = Label(self.middle_frame, text='Microwave')
        self.microwave_label.grid(row=1, column=0, sticky='e')
        self.microwave_element_frame, self.microwave_sample_frame = self.create_element_and_sample_frame(1)

        self.katanax_label = Label(self.middle_frame, text='Katanax')
        self.katanax_label.grid(row=2, column=0, sticky='e')
        self.katanax_element_frame, self.katanax_sample_frame = self.create_element_and_sample_frame(2, color='purple')

        self.hotplate_label = Label(self.middle_frame, text='Hotplate')
        self.hotplate_label.grid(row=3, column=0, sticky='e')
        self.hotplate_element_frame, self.hotplate_sample_frame = self.create_element_and_sample_frame(3, color='orange')

        self.sample_entry.bind('<Return>', self.__add_checkbutton(self.menu_list))

        self.bottom_frame = Frame(self.root, bg='red')
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew')

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.submit = Button(self.bottom_frame, text='Submit', command=lambda: self.__submit())
        self.submit.grid(row=0, column=0)

    def create_element_and_sample_frame(self, row: int, color=''):
        element_frame = Frame(self.middle_frame, bg='')
        element_frame.grid(row=row, column=1, sticky='nsew')

        spinbox = Spinbox(self.middle_frame, from_=1, to=10, width=2)
        spinbox.grid(row=row, column=2, sticky='w')

        sample_frame = Frame(self.middle_frame, bg=color)
        sample_frame.grid(row=row, column=3, sticky='nsew')

        entry = Entry(element_frame)
        entry.pack(side='top')

        menubutton = Menubutton(sample_frame, width=9, text='select', name=f'button_{0}')
        menubutton.pack(side='top')

        menu = Menu(menubutton, tearoff=0)
        self.menu_list.append(menu)  # added initial menu button here
        menubutton.config(menu=menu)

        spinbox.config(command=self.__spinbox_handler(spinbox, element_frame, sample_frame))

        return element_frame, sample_frame

    def __add_checkbutton(self, menu_list):
        def func(_):
            self.check_vars = {}
            print(f'size of menu_list: {len(menu_list)}')
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

                    print(self.check_vars)
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

    def __spinbox_handler(self, spinbox, element_frame, sample_frame):
        print(f'initial child cound: {len(element_frame.winfo_children())}')
        def func():
            count = int(spinbox.get())
            child_count = len(element_frame.winfo_children())
            #print(f'count {count}')
            print(f'child_count {child_count}')
            if count > child_count:
                for i in range(count - child_count):
                    entry = Entry(element_frame, name=f'entry_{child_count}')
                    entry.pack(side='top')
                    button = Menubutton(sample_frame, width=9, text='select', name=f'button_{child_count}')
                    button.pack(side='top')
                    print(f'inside __spinbox_handler, button name={str(button)}')
                    menu = Menu(button, tearoff=0)#
                    self.menu_list.append(menu)#
                    button.config(menu=menu)#
                    #evoke entry enter event to force sample updates on new menubuttons

            elif child_count > count:
                print('True')
                for i in reversed(range(count, child_count)):
                    element_frame.nametowidget(f'entry_{i}').destroy()
                    button = sample_frame.nametowidget(f'button_{i}')
                    menu = button.winfo_children()[0]
                    self.menu_list.remove(menu)
                    button.destroy()
            # evoke entry enter event to force sample updates on new menubuttons
            self.sample_entry.focus_set()
            self.sample_entry.event_generate('<Return>')
            spinbox.focus_set()
            print(f'count {count}')

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
            print(f'elements: {elements}')
            digestion.append((elements, selected_sample))
        return digestion

    def __submit(self):
        microwave = self.__grab_data(self.microwave_element_frame, self.microwave_sample_frame)
        katanax = self.__grab_data(self.katanax_element_frame, self.katanax_sample_frame)
        hotplate = self.__grab_data(self.hotplate_element_frame, self.hotplate_sample_frame)
        print(f'microwave: {microwave}')
        print(katanax)
        print(hotplate)
        print()

        COPY = self.replicates.get()
        loi = self.loi.get()
        url = 'master_template.xlsx'
        workbook = xlsxwriter.Workbook(url)
        template = Template(workbook, self.request_id_entry.get(), COPY, loi=loi)
        print(f'{self.loi.get()} value')
        for elements, samples in microwave:
            print(f'elements: {elements}')
            print(f'samples: {samples}')
            template.add_microwave(elements, samples)

        for elements, samples in katanax:
            template.add_katanax(elements, samples)

        for elements, samples in hotplate:
            template.add_hotplate(elements, samples)

        template.create_analysis_table()
        workbook.close()


    def run(self):
        self.root.mainloop()
        print('is it empty')
        print(self.check_vars)




app = App()
app.run()