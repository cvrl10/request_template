from tkinter import *
import re



root = Tk()

root.geometry('250x250')

sample = Entry(root)
sample.pack()


def extract_sample_id():
    global sample
    match = re.search(r'(\d+)\((\d+)\)', sample.get())
    if match:
        sample_id, sample_count = match.groups()
        sample_id = int(sample_id)
        sample_count = int(sample_count)
        samples = [sample_id+i for i in range(sample_count)]
    else:
        samples = re.split(r'[,\s]+', sample.get())
    return samples



mb = Menubutton(root, text="Options", relief="raised")
#mb = Menubutton(root, text="Options", relief="sunken")
#mb = Menubutton(root, text="Options", relief="groove")
#mb = Menubutton(root, text="Options", relief="ridge")
#mb = Menubutton(root, text="Options", relief="solid")
menu = Menu(mb, tearoff=0)
mb.config(menu=menu)

#var1 = IntVar(value=1)
#var2 = IntVar(value=1)

variables = {}
def add_checkbutton(m):
    def func(_):
        m.delete(0, 'end')
        samples = extract_sample_id()
        for sample in samples:
            if sample == '':
                continue
            var = IntVar(value=1)
            m.add_checkbutton(label=sample, variable=var)
            print(variables)
    return func

sample.bind('<Key>', add_checkbutton(menu))

mb.pack()

# Remove "Option 1" (index 0)
#menu.delete(0)

root.mainloop()
print('end')
print(variables)