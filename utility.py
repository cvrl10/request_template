import tkinter as tk
import re

AUTO_CLOSE = 3000

BACKGROUND = '#e6e6e6'
ACTIVE_BACKGROUND = '#5a5a5a'

ALKALI_BG = '#FFF4F2'
METALLOIDS_BG = 'white'
NOBLE_BG = 'black'
NOBLE_FG = 'white'
TRANSITION_BG = '#FFFFE0'
ACTINIDE_BG = '#A8DCAB'
#ACTINIDE_BG = '#BEFDB7'

DEFAULT = {'bg': BACKGROUND}

PARAMETERS = {
    'Li': {'bg': ALKALI_BG},
    'Na': {'bg': ALKALI_BG},
    'K':  {'bg': ALKALI_BG},
    'Rb': {'bg': ALKALI_BG},
    'Cs': {'bg': ALKALI_BG},
    'Fr': {'bg': ALKALI_BG},

    'B': {'bg': METALLOIDS_BG},
    'Si': {'bg': METALLOIDS_BG},
    'Ge': {'bg': METALLOIDS_BG},
    'Po': {'bg': METALLOIDS_BG},
    'As': {'bg': METALLOIDS_BG},
    'Sb': {'bg': METALLOIDS_BG},
    'Te': {'bg': METALLOIDS_BG},
    'At': {'bg': METALLOIDS_BG},

    'He': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Ne': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Ar': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Kr': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Xe': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Rn': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Og': {'bg': NOBLE_BG, 'fg': NOBLE_FG},

    'Sc': {'bg': TRANSITION_BG},
    'Ti': {'bg': TRANSITION_BG},
    'V':  {'bg': TRANSITION_BG},
    'Cr': {'bg': TRANSITION_BG},
    'Mn': {'bg': TRANSITION_BG},
    'Fe': {'bg': TRANSITION_BG},
    'Co': {'bg': TRANSITION_BG},
    'Ni': {'bg': TRANSITION_BG},
    'Cu': {'bg': TRANSITION_BG},
    'Zn': {'bg': TRANSITION_BG},

    'Y':  {'bg': TRANSITION_BG},
    'Zr': {'bg': TRANSITION_BG},
    'Nb': {'bg': TRANSITION_BG},
    'Mo': {'bg': TRANSITION_BG},
    'Tc': {'bg': TRANSITION_BG},
    'Ru': {'bg': TRANSITION_BG},
    'Rh': {'bg': TRANSITION_BG},
    'Pd': {'bg': TRANSITION_BG},
    'Ag': {'bg': TRANSITION_BG},
    'Cd': {'bg': TRANSITION_BG},

    'Hf': {'bg': TRANSITION_BG},
    'Ta': {'bg': TRANSITION_BG},
    'W':  {'bg': TRANSITION_BG},
    'Re': {'bg': TRANSITION_BG},
    'Os': {'bg': TRANSITION_BG},
    'Ir': {'bg': TRANSITION_BG},
    'Pt': {'bg': TRANSITION_BG},
    'Au': {'bg': TRANSITION_BG},
    'Hg': {'bg': TRANSITION_BG},

    'Rf': {'bg': TRANSITION_BG},
    'Db': {'bg': TRANSITION_BG},
    'Sg': {'bg': TRANSITION_BG},
    'Bh': {'bg': TRANSITION_BG},
    'Hs': {'bg': TRANSITION_BG},
    'Mt': {'bg': TRANSITION_BG},
    'Ds': {'bg': TRANSITION_BG},
    'Rg': {'bg': TRANSITION_BG},
    'Cn': {'bg': TRANSITION_BG},

    'Ac': {'bg': ACTINIDE_BG},
    'Th': {'bg': ACTINIDE_BG},
    'Pa': {'bg': ACTINIDE_BG},
    'U':  {'bg': ACTINIDE_BG},
    'Np': {'bg': ACTINIDE_BG},
    'Pu': {'bg': ACTINIDE_BG},
    'Am': {'bg': ACTINIDE_BG},
    'Cm': {'bg': ACTINIDE_BG},
    'Bk': {'bg': ACTINIDE_BG},
    'Cf': {'bg': ACTINIDE_BG},
    'Es': {'bg': ACTINIDE_BG},
    'Fm': {'bg': ACTINIDE_BG},
    'Md': {'bg': ACTINIDE_BG},
    'No': {'bg': ACTINIDE_BG},
    'Lr': {'bg': ACTINIDE_BG},
}

ELEMENT_FULL_NAME = {    # Period 1
    'H': 'H: Hydrogen',
    'He': 'He: Helium',

    # Period 2
    'Li': 'Li: Lithium',
    'Be': 'Be: Beryllium',
    'B': 'B: Boron',
    'C': 'C: Carbon',
    'N': 'N: Nitrogen',
    'O': 'O: Oxygen',
    'F': 'F: Fluorine',
    'Ne': 'Ne: Neon',

    # Period 3
    'Na': 'Na: Sodium',
    'Mg': 'Mg: Magnesium',
    'Al': 'Al: Aluminum',
    'Si': 'Si: Silicon',
    'P': 'P: Phosphorus',
    'S': 'S: Sulfur',
    'Cl': 'Cl: Chlorine',
    'Ar': 'Ar: Argon',

    # Period 4
    'K': 'K: Potassium',
    'Ca': 'Ca: Calcium',
    'Sc': 'Sc: Scandium',
    'Ti': 'Ti: Titanium',
    'V': 'V: Vanadium',
    'Cr': 'Cr: Chromium',
    'Mn': 'Mn: Manganese',
    'Fe': 'Fe: Iron',
    'Co': 'Co: Cobalt',
    'Ni': 'Ni: Nickel',
    'Cu': 'Cu: Copper',
    'Zn': 'Zn: Zinc',
    'Ga': 'Ga: Gallium',
    'Ge': 'Ge: Germanium',
    'As': 'As: Arsenic',
    'Se': 'Se: Selenium',
    'Br': 'Br: Bromine',
    'Kr': 'Kr: Krypton',

    # Period 5
    'Rb': 'Rb: Rubidium',
    'Sr': 'Sr: Strontium',
    'Y': 'Y: Yttrium',
    'Zr': 'Zr: Zirconium',
    'Nb': 'Nb: Niobium',
    'Mo': 'Mo: Molybdenum',
    'Tc': 'Tc: Technetium',
    'Ru': 'Ru: Ruthenium',
    'Rh': 'Rh: Rhodium',
    'Pd': 'Pd: Palladium',
    'Ag': 'Ag: Silver',
    'Cd': 'Cd: Cadmium',
    'In': 'In: Indium',
    'Sn': 'Sn: Tin',
    'Sb': 'Sb: Antimony',
    'Te': 'Te: Tellurium',
    'I': 'I: Iodine',
    'Xe': 'Xe: Xenon',

    # Period 6
    'Cs': 'Cs: Cesium',
    'Ba': 'Ba: Barium',

    # Lanthanides
    'La': 'La: Lanthanum',
    'Ce': 'Ce: Cerium',
    'Pr': 'Pr: Praseodymium',
    'Nd': 'Nd: Neodymium',
    'Pm': 'Pm: Promethium',
    'Sm': 'Sm: Samarium',
    'Eu': 'Eu: Europium',
    'Gd': 'Gd: Gadolinium',
    'Tb': 'Tb: Terbium',
    'Dy': 'Dy: Dysprosium',
    'Ho': 'Ho: Holmium',
    'Er': 'Er: Erbium',
    'Tm': 'Tm: Thulium',
    'Yb': 'Yb: Ytterbium',
    'Lu': 'Lu: Lutetium',

    # Continue Period 6
    'Hf': 'Hf: Hafnium',
    'Ta': 'Ta: Tantalum',
    'W': 'W: Tungsten',
    'Re': 'Re: Rhenium',
    'Os': 'Os: Osmium',
    'Ir': 'Ir: Iridium',
    'Pt': 'Pt: Platinum',
    'Au': 'Au: Gold',
    'Hg': 'Hg: Mercury',
    'Tl': 'Tl: Thallium',
    'Pb': 'Pb: Lead',
    'Bi': 'Bi: Bismuth',
    'Po': 'Po: Polonium',
    'At': 'At: Astatine',
    'Rn': 'Rn: Radon',

    # Period 7
    'Fr': 'Fr: Francium',
    'Ra': 'Ra: Radium',

    # Actinides
    'Ac': 'Ac: Actinium',
    'Th': 'Th: Thorium',
    'Pa': 'Pa: Protactinium',
    'U': 'U: Uranium',
    'Np': 'Np: Neptunium',
    'Pu': 'Pu: Plutonium',
    'Am': 'Am: Americium',
    'Cm': 'Cm: Curium',
    'Bk': 'Bk: Berkelium',
    'Cf': 'Cf: Californium',
    'Es': 'Es: Einsteinium',
    'Fm': 'Fm: Fermium',
    'Md': 'Md: Mendelevium',
    'No': 'No: Nobelium',
    'Lr': 'Lr: Lawrencium',

    # Continue Period 7
    'Rf': 'Rf: Rutherfordium',
    'Db': 'Db: Dubnium',
    'Sg': 'Sg: Seaborgium',
    'Bh': 'Bh: Bohrium',
    'Hs': 'Hs: Hassium',
    'Mt': 'Mt: Meitnerium',
    'Ds': 'Ds: Darmstadtium',
    'Rg': 'Rg: Roentgenium',
    'Cn': 'Cn: Copernicium',
    'Nh': 'Nh: Nihonium',
    'Fl': 'Fl: Flerovium',
    'Mc': 'Mc: Moscovium',
    'Lv': 'Lv: Livermorium',
    'Ts': 'Ts: Tennessine',
    'Og': 'Og: Oganesson'
}

class ButtonTooltip:
    def __init__(self, widget, adjacent):
        self.widget = widget
        #print(f'winfo_name: {self.widget.winfo_name()}')
        self.adjacent = widget.master.nametowidget(adjacent)
        self.tip_window = None

        widget.bind('<Enter>', self.show)
        widget.bind('<Leave>', self.hide)

    def show(self, _):
        if self.widget.cget('relief') == 'raised':
            self.widget.focus_set()
            self.widget.config(bg='#4a90e2')
        if self.tip_window:
            return

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)

        element = self.widget.cget('text')
        tip = tk.Label(
            self.tip_window,
            text=ELEMENT_FULL_NAME.get(element, f'{element}: Placeholder'),
            bg='#FFFFE0',
            #bg='#4a90e2',
            fg='black',
            relief='solid',
            borderwidth=0,
            padx=5,
            pady=2
        )

        tip.pack()

        self.tip_window.update_idletasks()
        x = self.adjacent.winfo_rootx() + self.adjacent.winfo_width()*3
        y = self.adjacent.winfo_rooty() + self.widget.winfo_height() // 2
        y = y - self.tip_window.winfo_height() // 2

        self.tip_window.wm_geometry(f'+{x}+{y}')

    def hide(self, _):
        if self.widget.cget('relief') == 'raised':
            self.widget.focus_set()
            text = self.widget.cget('text')
            self.widget.config(**PARAMETERS.get(text, DEFAULT))
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

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

    def set_positiion(self):
        pass

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
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.iconbitmap(r'img/periodic_table.ico')
        self.hide()

        self.textbox = {}
        self.selected = {}
        self.active_frame = None
        self.window.protocol('WM_DELETE_WINDOW', self.clear())

        root.update_idletasks()
        x = root.winfo_x() + root.winfo_width() + 5
        y = root.winfo_y()
        self.window.geometry(f'+{x}+{y}')

    def add_textbox(self, entry):
        key = entry.winfo_name()
        self.selected[key] = []
        frame = tk.Frame(self.window, name=key)
        self.textbox[key] = frame
        self.__create_grid(frame)
        self.__fill_grid(frame)


    def clear(self):
        def func():
            frame, textbox = self.active_frame
            print(f'frame_name={frame.winfo_name()}')
            key = frame.winfo_name()

            ELEMENTS = set([button.cget('text') for button in frame.winfo_children()])
            entry = re.split(r'[,\s]+', textbox.get())
            print(f'entry contains: {entry}')
            textbox.delete(0, tk.END)

            if '' in entry:
                entry_set = set()
            else:
                entry_set = set(entry)

            not_periodic = entry_set - ELEMENTS
            analytes = self.selected[key].copy()

            for analyte in not_periodic:
                analytes.insert(0, analyte)
            analytes.sort()

            textbox.insert(0, ', '.join(analytes))
            self.hide()

        return func

    def hide(self):
        self.window.withdraw()

    def __show(self):
        self.window.deiconify()

    def __create_grid(self, frame):
        #for i in range(9):
        for i in range(10):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(18):
            frame.grid_columnconfigure(i, weight=1)

    def __fill_grid(self, frame):
        def fill_row(row, range, elements):
            for i, element in zip(range, elements):
                button = self.__button(element, frame)
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
        fill_row(row=7, range=[0], elements=['*'])
        fill_row(row=8, range=LANTHANIDES, elements=['Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',
                                                                'Ho', 'Er', 'Tm', 'Yb', 'Lu'])
        fill_row(row=9, range=ACTINIDES, elements=['Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es',
                                                                'Fm', 'Md', 'No', 'Lr'])

    def __button(self, element, frame):
        def clicked(button):
            def func():
                key = frame.winfo_name()
                #
                #_, textbox = self.active_frame
                #print(f'frame.master: {frame.master}')
                #print(f'inside_clicked: {textbox.get()}')
                #current_entry = re.split(r'[,\s]+', textbox.get())
                #
                selected = self.selected[key]
                print(f'inside clicked handler, what is selected: {selected}')
                relief = button.cget('relief')
                if relief == 'raised':
                    button.config(relief='sunken', bg=ACTIVE_BACKGROUND, fg='white')
                    #current_entry.append(button.cget('text'))#
                    selected.append(button.cget('text'))
                else:
                    button.config(relief='raised', bg=BACKGROUND, fg='black')
                    #current_entry.remove(button.cget('text'))#
                    selected.remove(button.cget('text'))
                #current_entry.sort()
                #textbox.insert(0, ', '.join(current_entry))#
            return func

        def highlight(button):
            def func(_):
                if button.cget('relief')=='raised':
                    button.focus_set()
                    button.config(bg='#4a90e2')
            return func

        def dehighlight(button):
            def func(_):
                if button.cget('relief')=='raised':
                    button.focus_set()
                    #button.config(highlightcolor='#4a90e2')
                    button.config(bg=BACKGROUND)
            return func

        button = tk.Button(frame, text=element, relief='raised', highlightthickness=2, name=element.lower(), **PARAMETERS.get(element, DEFAULT))
        button.bind('<Enter>', highlight(button))
        button.bind('<Leave>', dehighlight(button))
        ButtonTooltip(button, 'h')
        button.config(command=clicked(button))
        return button

    def show(self, entry):
        ''':param entry: takes a tk.Entry object
            :return: the handler for <Double-Button-1> that displays the periodic frame inside tk.Toplevel
             for selecting elements tied to the tk.Entry
        '''

        def func(_):
            if self.active_frame:
            #if self.active_frame and re.split(r'[,\s]+', entry.get())==['']:#this boolean is to prevent exception when there's no active frame
                self.clear()()#this is to allow me to save entry while changing between frame w/o closing Toplevel
            name = entry.winfo_name()
            print(f'name={name}')
            title = name.replace('entry', '')
            self.window.title(title)
            frame = self.textbox[entry.winfo_name()]
            if self.active_frame == None:#currently no active frame, so set the current frame to the frame tied to the tk.Entry evoking <Double-Button-1>
                frame.pack()
                self.active_frame = (frame, entry)
            else:#here we hide the old frame to set active_frame to display the frame tied to the tk.Entry evoking <Double-Button-1>
                hide_this_frame, _ = self.active_frame
                hide_this_frame.pack_forget()
                self.active_frame = (frame, entry)
                frame.pack()

            print(f'opening this frame: {frame.winfo_name}')

            elements = list(map(lambda e: e.title(), re.split(r'[,\s]+', entry.get())))
            print('inside show')
            print(elements)
            entry_set = set(elements)
            selected_set = set(self.selected[name])
            print(f'entry contains: {entry_set}')
            if '' in entry_set:
                diff = set()
            else:
                diff = selected_set - entry_set
            print(f'difference should be unselected: {diff}')
            for element in diff:
                print(f'diff: {element}')
                #button = table.window.nametowidget(element.lower())
                button = frame.nametowidget(element.lower())
                button.invoke()
                print(f'evoking {button}')

            if '' in elements: #to capture cleared textbox reset the  buttons
                for button in frame.winfo_children():
                    relief = button.cget('relief')
                    if relief == 'sunken':
                        button.invoke()

            for button in frame.winfo_children():
                element = button.cget('text')
                if element in elements:
                    if element not in self.selected[name]:
                        button.invoke()

            self.__show()

        return func

'''
root = tk.Tk()
root.geometry('600x400')
entry = tk.Entry(root, name='microwave_0entry')
other = tk.Entry(root, name='katanax_0entry')
entry.pack()
other.pack()

p = PeriodicTable(root)
p.add_textbox(entry)
p.add_textbox(other)

entry.bind('<Double-Button-1>', p.show(entry))
other.bind('<Double-Button-1>', p.show(other))

root.mainloop()'''




