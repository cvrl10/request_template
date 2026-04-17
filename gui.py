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


        request = Label(self.top_frame, text='Request ID:')
        request.grid(row=0, column=0, sticky='e')
        request_entry = Entry(self.top_frame)
        request_entry.grid(row=0, column=1, sticky='w')
        sample = Label(self.top_frame, text='Sample(s):')
        sample.grid(row=1, column=0, sticky='e')
        self.sample_entry = Entry(self.top_frame)
        self.sample_entry.grid(row=1, column=1, sticky='w')
        #self.sample_entry.bind('<Key>', self.__extract_sample_id)

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

        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.rowconfigure(1, weight=1)
        self.middle_frame.rowconfigure(2, weight=1)
        self.middle_frame.rowconfigure(3, weight=1)

        self.menu_list = []

        self.element_label = Label(self.middle_frame, text='element(s)')
        self.element_label.grid(row=0, column=1, sticky='w')

        self.microwave_label = Label(self.middle_frame, text='Microwave')
        self.microwave_label.grid(row=1, column=0, sticky='e')
        self.microwave_element_frame = Frame(self.middle_frame, bg='green')
        self.microwave_element_frame.grid(row=1, column=1, sticky='nsew')

        self.microwave_spinbox = Spinbox(self.middle_frame, from_=1, to=10, width=2)
        self.microwave_spinbox.grid(row=1, column=2, sticky='w')

        self.microwave_sample_frame = Frame(self.middle_frame, bg='green')
        self.microwave_sample_frame.grid(row=1, column=3, sticky='nsew')

        self.microwave_entry_0 = Entry(self.microwave_element_frame)
        self.microwave_entry_0.pack(side='top')
        self.microwave_menubutton_0 = Menubutton(self.microwave_sample_frame, width=9, text='select')
        self.microwave_menubutton_0.pack(side='top')

        self.microwave_menu_0 = Menu(self.microwave_menubutton_0, tearoff=0)
        self.menu_list.append(self.microwave_menu_0)
        self.microwave_menubutton_0.config(menu=self.microwave_menu_0)
        self.check_vars = [] #needed so samples are initially check, if I don't kee references they will get garbage collected
        print(self.check_vars)
        #self.sample_entry.bind('<Key>', self.__extract_sample_id(self.check_vars, self.menu_list))
        self.sample_entry.bind('<Return>', self.__extract_sample_id(self.check_vars, self.menu_list))

        self.katanax_label = Label(self.middle_frame, text='Katanax')
        self.katanax_label.grid(row=2, column=0, sticky='e')
        self.katanax_element_frame = Frame(self.middle_frame, bg='purple')
        self.katanax_element_frame.grid(row=2, column=1, sticky='nsew')

        self.hotplate_label = Label(self.middle_frame, text='Hotplate')
        self.hotplate_label.grid(row=3, column=0, sticky='e')
        self.hotplate_element_frame = Frame(self.middle_frame, bg='orange')
        self.hotplate_element_frame.grid(row=3, column=1, sticky='nsew')
        #make those frames not grid

        self.bottom_frame = Frame(self.root, bg='red')
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew')

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.submit = Button(self.bottom_frame, text='Submit')
        self.submit.grid(row=0, column=0)

    def __extract_sample_id(self, variables, menu_list):
        def func(_):
            match = re.search(r'(\d+)\((\d+)\)', self.sample_entry.get())
            if match:
                sample_id, sample_count = match.groups()
                sample_id = int(sample_id)
                sample_count = int(sample_count)
                samples = [sample_id + i for i in range(sample_count)]
            else:
                samples = re.split(r'[,\s]+', self.sample_entry.get())
            for menu in menu_list:
                menu.delete(0, 'end')
                print(samples)
                for sample in samples:
                    if sample == '':
                        continue
                    variables.append(IntVar(value=1))
                    menu.add_checkbutton(label=sample, variable=variables[-1])

                #menu.add_command(command=lambda: 'break')
                    print(variables)
        return func
    def __add_checkbutton(self):
        pass
    def __spinbox_handler(self, element_frame, sample_frame):
        pass

    def run(self):
        self.root.mainloop()
        print('is it empty')
        print(self.check_vars)




app = App()
app.run()