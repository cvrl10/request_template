from tkinter import *

from tkinter import *

root = Tk()

root.geometry('250x250')

mb = Menubutton(root, text="Options", relief="raised")
mb = Menubutton(root, text="Options", relief="sunken")
mb = Menubutton(root, text="Options", relief="groove")
mb = Menubutton(root, text="Options", relief="ridge")
#mb = Menubutton(root, text="Options", relief="solid")
menu = Menu(mb, tearoff=0)
mb.config(menu=menu)

var1 = IntVar()
var2 = IntVar()

menu.add_checkbutton(label="Option 1", variable=var1)
menu.add_checkbutton(label="Option 2", variable=var2)

mb.pack()

# Remove "Option 1" (index 0)
#menu.delete(0)

root.mainloop()