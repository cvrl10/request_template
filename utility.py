import os
import tkinter as tk
from tkinter import ttk, filedialog
from configparser import ConfigParser
from pathlib import Path
import re

TEMP_CONFIG = None

AUTO_CLOSE = 3000

BACKGROUND = '#e6e6e6'
ACTIVE_BACKGROUND = '#5a5a5a'

NONMETAL_BG = '#E6CCFF'
NONMETAL_BG = '#F9CD9D'
NON_METAL_FG = 'black'
#ALKALI_BG = '#FFF4F2'
ALKALI_BG = '#F3CDC3'
ALKALINE_EARTH_BG = '#DCA195'
ALKALINE_EARTH_FG = 'black'
METALLOIDS_BG = '#748B7A'
NOBLE_BG = 'black'
NOBLE_FG = 'white'
HALOGEN_BG = '#DC8A5D'
TRANSITION_BG = '#FFFFE0'
ACTINIDE_BG = '#A8DCAB'
#ACTINIDE_BG = '#BEFDB7'
LANTHANIDE_BG = '#718DA5'
POST_TRANSITION_BG = '#A3B2A6'
POST_TRANSITION_FG = 'black'

DEFAULT = {'bg': BACKGROUND, 'fg': 'black'}

PARAMETERS = {

    #'*': {'bg': BACKGROUND, 'fg': BACKGROUND},

    'H': {'bg': '#F9CD9D', 'fg': 'black'},

    'C': {'bg': NONMETAL_BG, 'fg': NON_METAL_FG},
    'N': {'bg': NONMETAL_BG, 'fg': NON_METAL_FG},
    'O': {'bg': NONMETAL_BG, 'fg': NON_METAL_FG},
    'P': {'bg': NONMETAL_BG, 'fg': NON_METAL_FG},
    'S': {'bg': NONMETAL_BG, 'fg': NON_METAL_FG},
    'Se': {'bg': NONMETAL_BG, 'fg': NON_METAL_FG},

    'F': {'bg': HALOGEN_BG, 'fg': NON_METAL_FG},
    'Cl': {'bg': HALOGEN_BG, 'fg': NON_METAL_FG},
    'Br': {'bg': HALOGEN_BG, 'fg': NON_METAL_FG},
    'I': {'bg': HALOGEN_BG, 'fg': NON_METAL_FG},
    'Ts': {'bg': HALOGEN_BG, 'fg': NON_METAL_FG},

    'Li': {'bg': ALKALI_BG, 'fg': 'black'},
    'Na': {'bg': ALKALI_BG, 'fg': 'black'},
    'K':  {'bg': ALKALI_BG, 'fg': 'black'},
    'Rb': {'bg': ALKALI_BG, 'fg': 'black'},
    'Cs': {'bg': ALKALI_BG, 'fg': 'black'},
    'Fr': {'bg': ALKALI_BG, 'fg': 'black'},

    'Be': {'bg': ALKALINE_EARTH_BG, 'fg': ALKALINE_EARTH_FG},
    'Mg': {'bg': ALKALINE_EARTH_BG, 'fg': ALKALINE_EARTH_FG},
    'Ca': {'bg': ALKALINE_EARTH_BG, 'fg': ALKALINE_EARTH_FG},
    'Sr': {'bg': ALKALINE_EARTH_BG, 'fg': ALKALINE_EARTH_FG},
    'Ba': {'bg': ALKALINE_EARTH_BG, 'fg': ALKALINE_EARTH_FG},
    'Ra': {'bg': ALKALINE_EARTH_BG, 'fg': ALKALINE_EARTH_FG},

    'B': {'bg': METALLOIDS_BG, 'fg': 'black'},
    'Si': {'bg': METALLOIDS_BG, 'fg': 'black'},
    'Ge': {'bg': METALLOIDS_BG, 'fg': 'black'},
    'Po': {'bg': METALLOIDS_BG, 'fg': 'black'},
    'As': {'bg': METALLOIDS_BG, 'fg': 'black'},
    'Sb': {'bg': METALLOIDS_BG, 'fg': 'black'},
    'Te': {'bg': METALLOIDS_BG, 'fg': 'black'},
    'At': {'bg': HALOGEN_BG, 'fg': 'black'},

    'He': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Ne': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Ar': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Kr': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Xe': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Rn': {'bg': NOBLE_BG, 'fg': NOBLE_FG},
    'Og': {'bg': NOBLE_BG, 'fg': NOBLE_FG},

    'Sc': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Ti': {'bg': TRANSITION_BG, 'fg': 'black'},
    'V':  {'bg': TRANSITION_BG, 'fg': 'black'},
    'Cr': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Mn': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Fe': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Co': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Ni': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Cu': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Zn': {'bg': TRANSITION_BG, 'fg': 'black'},

    'Y':  {'bg': TRANSITION_BG, 'fg': 'black'},
    'Zr': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Nb': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Mo': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Tc': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Ru': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Rh': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Pd': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Ag': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Cd': {'bg': TRANSITION_BG, 'fg': 'black'},

    'Hf': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Ta': {'bg': TRANSITION_BG, 'fg': 'black'},
    'W':  {'bg': TRANSITION_BG, 'fg': 'black'},
    'Re': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Os': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Ir': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Pt': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Au': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Hg': {'bg': TRANSITION_BG, 'fg': 'black'},

    'Rf': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Db': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Sg': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Bh': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Hs': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Mt': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Ds': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Rg': {'bg': TRANSITION_BG, 'fg': 'black'},
    'Cn': {'bg': TRANSITION_BG, 'fg': 'black'},

    'La': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Ce': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Pr': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Nd': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Pm': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Sm': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Eu': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Gd': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Tb': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Dy': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Ho': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Er': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Tm': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Yb': {'bg': LANTHANIDE_BG, 'fg': 'black'},
    'Lu': {'bg': LANTHANIDE_BG, 'fg': 'black'},

    'Ac': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Th': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Pa': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'U':  {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Np': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Pu': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Am': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Cm': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Bk': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Cf': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Es': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Fm': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Md': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'No': {'bg': ACTINIDE_BG, 'fg': 'black'},
    'Lr': {'bg': ACTINIDE_BG, 'fg': 'black'},

    'Al': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Ga': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'In': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Sn': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Tl': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Pb': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Bi': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    #'Po': {'bg': BACKGROUND, 'fg': POST_TRANSITION_FG},
    'Nh': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Fl': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Mc': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
    'Lv': {'bg': POST_TRANSITION_BG, 'fg': POST_TRANSITION_FG},
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


class Tooltip:
    def __init__(self, widget):
        self.widget = widget


class ButtonTooltip(Tooltip):
    def __init__(self, widget, adjacent):
        super().__init__(widget)
        self.adjacent = widget.master.nametowidget(adjacent)
        self.tip_window = None

        widget.bind('<Enter>', self.show)
        widget.bind('<Leave>', self.hide)

    def show(self, _):
        if self.widget.cget('relief') == 'raised':
            self.widget.focus_set()
            self.widget.config(bg='#4a90e2', fg='black')

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


class MenubuttonTooltip(Tooltip):
    def __init__(self, widget, tip):
        super().__init__(widget)
        self.message = tip
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

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty()
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

    def hide(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

    def cancel_tip(self, event):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

        self.hide()


class PeriodicTable:
    def __init__(self, root):
        self.root = root
        self.location = False
        self.window = tk.Toplevel(root)
        self.hide()
        #self.window.iconbitmap(r'img/periodic_table.ico')
        self.window.iconbitmap(r'img/blank.ico')

        self.selected = {}
        self.active_frame = None
        self.window.protocol('WM_DELETE_WINDOW', self.clear)

        root.update_idletasks()
        x = root.winfo_x() + root.winfo_width() + 5
        y = root.winfo_y()
        self.window.geometry(f'+{x}+{y}')

    def add_textbox(self, entry):
        key = entry.winfo_name()
        self.selected[key] = []
        frame = tk.Frame(self.window, name=key)
        self.__create_grid(frame)
        self.__fill_grid(frame)

    def clear(self):
        frame, textbox = self.active_frame
        key = frame.winfo_name()

        ELEMENTS = set([button.cget('text') for button in frame.winfo_children()])
        ENTRY = set(re.split(r'[,\s]+', textbox.get()))
        textbox.delete(0, tk.END)

        ENTRY.discard('')

        COMPOUNDS = ENTRY - ELEMENTS
        analytes = self.selected[key].copy()

        analytes.extend(COMPOUNDS)
        analytes.sort()

        textbox.insert(0, ', '.join(analytes))
        self.hide()

    def hide(self):
        self.window.withdraw()

    def __show(self):
        if not self.location:#sets the location of Toplevel next to root initially then location is tied to wherever I move it.
            self.root.update_idletasks()
            x = self.root.winfo_x() + self.root.winfo_width() + 5
            y = self.root.winfo_y()
            self.window.geometry(f'+{x}+{y}')
            self.location = True
        self.window.deiconify()

    @staticmethod
    def __create_grid(frame):
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
        LANTHANIDES = ACTINIDES = [i for i in range(3, 17)]

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
                '''this part functions to update tk.Entry as button is clicked, it is not required for normal operation.
                 Follow current_entry'''
                _, textbox = self.active_frame
                current_entry = set(re.split(r'[,\s]+', textbox.get()))
                current_entry.discard('')
                #
                selected = self.selected[key]
                relief = button.cget('relief')
                if relief == 'raised':
                    button.config(relief='sunken', bg=ACTIVE_BACKGROUND, fg='white')
                    current_entry.add(button.cget('text'))#comment this out
                    selected.append(button.cget('text'))
                else:
                    button.config(relief='raised', **PARAMETERS.get(element, DEFAULT))
                    current_entry.discard(button.cget('text'))#
                    selected.remove(button.cget('text'))
                #
                current_entry = list(current_entry)
                current_entry.sort()#
                textbox.delete(0, tk.END)#
                textbox.insert(0, ', '.join(current_entry))#
                #
            return func

        button = tk.Button(frame, text=element, relief='raised', highlightthickness=2, name=element.lower(), **PARAMETERS.get(element, DEFAULT))
        ButtonTooltip(button, 'h')
        button.config(command=clicked(button))
        return button

    def show(self, entry):
        ''':param entry: takes a tk.Entry object
            :return: the handler for <Double-Button-1> that displays the periodic frame inside tk.Toplevel
             for selecting elements tied to the tk.Entry
        '''

        def func(_):
            name = entry.winfo_name()
            title = name.replace('entry', '')
            self.window.title(title)
            frame = self.window.nametowidget(name)

            if self.active_frame == None:#currently no active frame, so set the current frame to the frame tied to the tk.Entry evoking <Double-Button-1>
                frame.pack()
                self.active_frame = (frame, entry)
            else:#here we hide the old frame to set active_frame to display the frame tied to the tk.Entry evoking <Double-Button-1>
                hide_this_frame, _ = self.active_frame
                hide_this_frame.pack_forget()
                self.active_frame = (frame, entry)
                frame.pack()

            elements = list(map(lambda e: e.title(), re.split(r'[,\s]+', entry.get())))
            #print(f'show() tk.Entry={elements}')
            #print(elements)
            entry_set = set(elements)
            entry_set.discard('')
            selected_set = set(self.selected[name])
            frame, _ = self.active_frame
            ELEMENTS = set([button.cget('text') for button in frame.winfo_children()])

            entry_set.discard('')
            DESELECTED = selected_set - entry_set
            click_me = (entry_set & ELEMENTS) - DESELECTED

            for element in DESELECTED:
                button = frame.nametowidget(element.lower())
                button.invoke()

            for element in click_me:
                button = frame.nametowidget(element.lower())
                relief = button.cget('relief')
                if relief == 'sunken':
                    continue
                button.invoke()

            self.__show()
            #print()
            return 'break'
        return func


'''
root = tk.Tk()
root.geometry('600x400')
entry = tk.Entry(root, name='test_microwave_0entry')
other = tk.Entry(root, name='test_katanax_0entry')
entry.pack()
other.pack()

pt = PeriodicTable(root)
pt.add_textbox(entry)
pt.add_textbox(other)

entry.bind('<Double-Button-1>', pt.show(entry))
other.bind('<Double-Button-1>', pt.show(other))

root.mainloop()#'''

parser = ConfigParser()
parser.read('config.ini')


class Modal:
    def __init__(self, root, _):
        self.config = _
        self.ACTIVE_FRAME = None
        self.root = root
        self.dialog = tk.Toplevel(root, bg='#FFFFFF')
        self.dialog.protocol('WM_DELETE_WINDOW', self.hide)
        self.hide()
        self.dialog.title('Options')
        self.dialog.iconbitmap('img/blank.ico')
        self.dialog.rowconfigure(0, weight=1)
        self.dialog.rowconfigure(1, weight=0)

        self.dialog.columnconfigure(0, weight=0)
        self.dialog.columnconfigure(1, weight=1)

        border = tk.Frame(self.dialog, bg='black', padx=1, pady=1)
        border.rowconfigure(0, weight=1)
        border.columnconfigure(0, weight=1)
        border.grid(row=0, column=0, sticky='nsew')

        #self.button_frame = tk.Frame(self.dialog, bg='#F0F0F0', bd=1, relief='groove')
        self.button_frame = tk.Frame(border, bg='#F0F0F0')
        self.button_frame.grid(row=0, column=0, sticky='nsew')

        self.horizontal_frame = tk.Frame(self.dialog, bg='#FFFFFF')
        #self.horizontal_frame = tk.Frame(self.dialog, bg='red')
        self.horizontal_frame.grid(row=1, column=0, columnspan=2, sticky='sew')

        cancel = tk.Button(self.horizontal_frame, text='Cancel', relief='groove', bg='#FFFFFF', width=8, command=self.__cancel)
        cancel.pack(side='right', padx=(5, 6), pady=(0, 6))
        self.__handler(cancel)

        ok = tk.Button(self.horizontal_frame, text='Ok', relief='groove', bg='#FFFFFF', width=8, command=self.ok)
        ok.pack(side='right', padx=5, pady=(0, 6))
        self.__handler(ok)

        container = self.__general_frame()
        self.__add_button(self.button_frame, '   General         ', container=container)

        container = self.__save_frame()
        self.__add_button(self.button_frame, '   Save           ', container=container)

        exit = tk.Button(self.button_frame, text='   Exit', relief='flat', activebackground='#C42B1C',
                         activeforeground='white', anchor='w', command=self.__cancel)
        exit.pack(expand=False, fill='x', side=tk.BOTTOM)
        exit.bind('<Enter>', lambda _: exit.config(relief='groove', bg='#C42B1C', fg='white'))
        exit.bind('<Leave>', lambda _: exit.config(relief='flat', bg='SystemButtonFace', fg='black'))

    def __handler(self, button):
        button.bind('<Enter>', lambda _: button.config(bg='#F0F0F0'))
        button.bind('<Leave>', lambda _: button.config(bg='#FFFFFF'))

    def __tkentry_handler(self, entry):
        entry.bind('<Enter>', lambda _: entry.config(bg='#F0F0F0'))
        entry.bind('<Leave>',
                   lambda _: entry.config(bg='#F0F0F0') if entry == self.dialog.focus_get() else entry.config(bg='white'))

        entry.bind('<FocusIn>', lambda _: entry.config(bg='#F0F0F0'))
        entry.bind('<FocusOut>', lambda _: entry.config(bg='white'))

    def hide(self):
        self.dialog.withdraw()
        self.dialog.grab_release()

    def show(self):
        parser.read('config.ini')
        destination = Path(parser.get('Path', 'directory')).resolve()
        #print(f'inside show(), destination is: {destination}')
        self.entry.delete(0, tk.END)

        if destination.exists():
            print(f'inside if, destination is:{destination}')
            self.entry.insert(0, destination)
        else:
            inmemory_config = self.config[0]
            directory = inmemory_config.get('Save', 'directory')
            print(f'inside else, destination is:{directory}')

            parser['Path']['directory'] = directory
            file = open('config.ini', 'w')
            parser.write(file)
            file.close()

            self.entry.insert(0, directory)

        self.ok()
        self.dialog.update_idletasks()
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - self.dialog.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f'700x400+{x}+{y}')
        self.dialog.transient(self.root)
        self.dialog.grab_set()
        self.dialog.deiconify()

    def __cancel(self):
        inmemory_config = self.config[0]
        #print({section: dict(inmemory_config.items(section)) for section in inmemory_config.sections()})
        sort = inmemory_config.get('General', 'sort')
        color = inmemory_config.get('General', 'calculation')
        file = inmemory_config.get('Save', 'save as')
        file = Path(file).stem
        #print('inside __cancel()')
        #print(file)
        directory = inmemory_config.get('Save', 'directory')

        self.sort_var.set(int(sort))
        self.calc_var.set(color)

        self.entry.delete(0, tk.END)
        self.entry.insert(0, directory)

        self.file.delete(0, tk.END)
        self.file.insert(0, file)

        self.hide()

    def ok(self):
        file = open('config.ini', 'w')
        parser.write(file)
        file.close()

        #if self.config:
            #inmemory_config = self.config[0]
            #print({section: dict(inmemory_config.items(section)) for section in inmemory_config.sections()})
        #print({section: dict(parser.items(section)) for section in parser.sections()})

        file = Path(self.file.get())
        ext = self.extension.get()
        ext = re.search(r'(\.\w+)', ext).group()
        #print('inside ok()')
        #print(file)
        #print(ext)
        file = file.with_suffix(ext)
        #print(file)

        config = ConfigParser()
        config['General'] = {}
        config['General']['sort'] = str(self.sort_var.get())
        config['General']['calculation'] = str(self.calc_var.get())
        config['Save'] = {}
        config['Save']['save as'] = str(file)
        config['Save']['directory'] = self.entry.get()

        self.config.insert(0, config)
        self.hide()

    def __add_button(self, frame, text, container):
        def func():
            self.ACTIVE_FRAME.grid_remove()
            unclick = self.button_frame.nametowidget(self.ACTIVE_FRAME.winfo_name())
            unclick.config(bg='SystemButtonFace', relief='flat')
            self.ACTIVE_FRAME = container
            name = self.ACTIVE_FRAME.winfo_name()
            #print(name)
            button = self.button_frame.nametowidget(name)
            self.dialog.focus_set()
            bg = button.cget('bg')

            if bg == 'SystemButtonFace':
                button.config(bg='#FFFFFF', relief='groove')
            container.grid()

        #print(f'text={text}')
        button = tk.Button(frame, text=text, name=text.lower().strip(), activebackground='white',
                           relief='flat', anchor='w', command=func, pady=0, width=20)
        if text.lower().strip() == 'general':
            button.invoke()
        #print(f'button: {button.winfo_name()}')
        #print(f'button: {button._w}')
        #button.grid(row=row, column=0, sticky='new')
        button.pack(expand=False, fill='x', anchor='n')
        button.bind('<Enter>', lambda _: button.config(relief='groove') if button.cget('bg') == 'SystemButtonFace' else None)
        button.bind('<Leave>', lambda _: button.config(relief='flat') if button.cget('bg') == 'SystemButtonFace' else None)

    def __general_frame(self):
        frame = tk.Frame(self.dialog, bg='#FFFFFF', name='general')
        frame.grid(row=0, column=1, sticky='nsew')

        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)

        #import tkinter.font as font
        #d = font.nametofont('TkDefaultFont')
        #print(d.actual())
        title = tk.Label(frame, text='Workbook options', font=('Segoe UI', 9, 'bold'), bg='#FFFFFF')
        title.grid(row=0, column=0, columnspan=2, stick='nw', pady=(0, 2))

        seperator = ttk.Separator(frame, orient=tk.HORIZONTAL)
        seperator.grid(row=1, column=0, columnspan=2, sticky='new')

        self.sort_var = tk.IntVar(value=1)
        checkbox = tk.Checkbutton(frame, variable=self.sort_var, text='sort analyte(s)', bg='#FFFFFF')
        checkbox.grid(row=2, column=0, sticky='nw')

        self.calc_var = tk.StringVar(value='#FFFFFF')
        checkbox = tk.Checkbutton(frame, variable=self.calc_var, text='show calculations', bg='#FFFFFF', onvalue='red',
                                  offvalue='#FFFFFF')
        checkbox.grid(row=3, column=0, sticky='nw')

        frame.grid_remove()
        self.ACTIVE_FRAME = frame
        return frame

    def __save_frame(self):
        frame = tk.Frame(self.dialog, bg='#FFFFFF', name='save')
        frame.grid(row=0, column=1, sticky='nsew')

        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=0)
        frame.rowconfigure(2, weight=0)
        frame.rowconfigure(3, weight=0)
        frame.rowconfigure(4, weight=0)

        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)

        title = tk.Label(frame, text='Save Documents', font=('Segoe UI', 9, 'bold'), bg='#FFFFFF')
        title.grid(row=0, column=0, columnspan=2, stick='nw', pady=(0, 2))

        seperator = ttk.Separator(frame, orient=tk.HORIZONTAL)
        seperator.grid(row=1, column=0, columnspan=3, sticky='new')

        label = tk.Label(frame, text='Default local file location:', bg='#FFFFFF')
        label.grid(row=2, column=0, sticky='nw')

        destination = Path(parser.get('Path', 'directory'))
        if not destination.exists():
            destination = Path.cwd()

        self.entry = tk.Entry(frame, width=50)
        self.__tkentry_handler(self.entry)
        self.entry.grid(row=2, column=1, sticky='w')
        self.entry.insert(0, str(destination.resolve()))

        browse = tk.Button(frame, text='Browse...', relief='groove', bg='#FFFFFF', command=self.__askdirectory, pady=0)
        browse.grid(row=2, column=2, sticky='w', padx=10, pady=(4, 0))
        self.__handler(browse)

        label = tk.Label(frame, text='Save As', bg='#FFFFFF')
        label.grid(row=3, column=0, sticky='nw')

        self.file = tk.Entry(frame, width=50)
        self.__tkentry_handler(self.file)
        self.file.grid(row=3, column=1, sticky='w')
        self.file.insert(0, 'master_workbook')

        self.extension = ttk.Combobox(frame, values=['Excel Workbook (*.xlsx)'], state='readonly')
        self.extension.current(0)
        self.extension.grid(row=4, column=1, sticky='w')


        frame.grid_remove()

        return frame

    def __askdirectory(self):
        directory = filedialog.askdirectory(parent=self.dialog, title='Modify Location', mustexist=True )
        if not directory:
            directory = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, directory)

        #apply
        parser['Path']['directory'] = directory

'''
root = tk.Tk()
m = Modal(root, [])
m.show()

root.bind('<Double-Button-1>', lambda _: m.show())
root.mainloop()#'''



