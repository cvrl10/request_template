import tkinter as tk
import re

AUTO_CLOSE = 3000

BACKGROUND = '#e6e6e6'
ACTIVE_BACKGROUND = '#5a5a5a'

class ToolTip:
    def __init__(self, widget, tip, position, offset):
        self.widget = widget
        self.message = tip
        self.position = position
        self.offset = offset
        self.tip_window = None
        self.after_id = None

        widget.bind('<Enter>', self.schedule_tip)
        widget.bind('<Leave>', self.cancel_tip)

    def schedule_tip(self, event):
        self.after_id = self.widget.after(500, self.show)

    def show(self):
        self.widget.config(activebackground=ACTIVE_BACKGROUND, activeforeground='white', cursor='hand2')
        #self.widget.config(activebackground=ACTIVE_BACKGROUND, activeforeground='white', cursor='hand2', bg=ACTIVE_BACKGROUND, fg='white')
        if self.tip_window:
            return
        #x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        #y = self.widget.winfo_rooty()
        x, y = self.positioning(self.position, self.offset)
        self.tip_window = tk.Toplevel(self.widget)

        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f'+{x}+{y}')

        tip = tk.Label(
            self.tip_window,
            text=self.message,
            bg='#FFFFE0',
            #bg='#4a90e2',
            fg='black',
            relief='solid',
            borderwidth=0,
            padx=5,
            pady=2
        )

        tip.pack()

        self.tip_window.after(AUTO_CLOSE, self.hide)

    def positioning(self, location, offset):
        if location == 'e':
            print(location)
            x = self.widget.winfo_rootx() + self.widget.winfo_width() + offset
            y = self.widget.winfo_rooty()
        if location == 'n':
            print(location)
            x = self.widget.winfo_rootx()
            y = self.widget.winfo_rooty() + offset
        return x, y


    def hide(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

    def cancel_tip(self, event):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

        self.hide()


#root = tk.Tk()

#button = tk.Button(root, text='click me')
#button.pack(padx=40, pady=40)

#ToolTip(button)

#root.mainloop()

class PeriodicTable:
    def __init__(self, textbox):
        self.window = tk.Toplevel(textbox)
        self.entry = textbox
        self.hide()
        self.__create_grid()
        self.__fill_grid()


        self.selected = []
        self.window.protocol('WM_DELETE_WINDOW', self.__clear())


    def __clear(self):
        def func():
            print(self.selected)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, ', '.join(self.selected))
            self.hide()
        return func

    def hide(self):
        self.window.withdraw()

    def show(self):
        self.window.deiconify()
    def __create_grid(self):
        for i in range(9):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(18):
            self.window.grid_columnconfigure(i, weight=1)

    def __fill_grid(self):
        def fill_row(row, range, elements):
            for i, element in zip(range, elements):
                button = self.__button(element)
                button.grid(row=row, column=i, sticky='nsew')

        FULL_RANGE = [i for i in range(18)]
        LANTHANIDES = ACTINIDES = [i for i in range(3 ,17)]
        fill_row(row=0, range=[0, 17], elements=['H', 'He'])
        fill_row(row=1, range=[0, 1, 12, 13, 14, 15, 16, 17], elements=['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'])
        fill_row(row=2, range=[0, 1, 12, 13, 14, 15, 16, 17], elements=['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar'])
        fill_row(row=3, range=FULL_RANGE, elements=['K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co',
                                                                'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'])
        fill_row(row=4, range=FULL_RANGE, elements=['Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh',
                                                                'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe'])
        fill_row(row=5, range=FULL_RANGE, elements=['Cs', 'Ba', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir',
                                                                'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'])
        fill_row(row=6, range=FULL_RANGE, elements=['Fr', 'Ra', 'Ac', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
                                                                'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'])
        fill_row(row=7, range=LANTHANIDES, elements=['Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',
                                                                'Ho', 'Er', 'Tm', 'Yb', 'Lu'])
        fill_row(row=8, range=ACTINIDES, elements=['Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es',
                                                                'Fm', 'Md', 'No', 'Lr'])


    def __button(self, element):
        def clicked(button):
            def func():
                relief = button.cget('relief')
                if relief == 'raised':
                    button.config(relief='sunken', bg=ACTIVE_BACKGROUND, fg='white')
                    self.selected.append(button.cget('text'))
                else:
                    button.config(relief='raised', bg=BACKGROUND, fg='black')
                    self.selected.remove(button.cget('text'))
                print(self.selected)
            return func
        def highlight(button):
            def func(_):
                if button.cget('relief')=='raised':
                    button.focus_set()
                    button.config(highlightcolor='#4a90e2')
            return func

        button = tk.Button(self.window, text=element, bg=BACKGROUND, relief='raised', highlightthickness=2)
        button.bind('<Enter>', highlight(button))
        #ToolTip(button, button.cget('text'), position='n', offset=-5)
        button.config(command=clicked(button))
        return button

def show(entry, table):
    def func(_):
        elements = list(map(lambda e: e.title(), re.split(r'[,\s]+', entry.get())))
        print('inside show')
        print(elements)
        if '' in elements:#to capture cleared textbox reset the  buttons
            for button in table.window.winfo_children():
                relief = button.cget('relief')
                if relief == 'sunken':
                    button.invoke()
        for button in table.window.winfo_children():
            element = button.cget('text')
            if element in elements:
                if element not in table.selected:
                    button.invoke()
        table.show()

    return func


root = tk.Tk()
root.geometry('600x400')
entry = tk.Entry(root)
entry.pack()

p = PeriodicTable(entry)

entry.bind('<Double-Button-1>', show(entry, p))

root.mainloop()








