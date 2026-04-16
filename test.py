from tkinter import *
import re



root = Tk()

root.geometry('250x250')

sample = Entry(root)
sample.pack()


def extract_sample_id(_):
    global sample
    print(type(sample))
    samples = re.split(r'[,\s]+', sample.get())
    for s in samples:
        #print(sample)
        pass
    print(samples)
    return samples



mb = Menubutton(root, text="Options", relief="raised")
mb = Menubutton(root, text="Options", relief="sunken")
mb = Menubutton(root, text="Options", relief="groove")
mb = Menubutton(root, text="Options", relief="ridge")
#mb = Menubutton(root, text="Options", relief="solid")
menu = Menu(mb, tearoff=0)
mb.config(menu=menu)

var1 = IntVar(value=1)
var2 = IntVar(value=1)

#menu.add_checkbutton(label="Option 1", variable=var1)
#menu.add_checkbutton(label="Option 2", variable=var2)

def add_checkbutton(m):
    def func(_):
        m.delete(0, 'end')
        variables = []
        samples = extract_sample_id('')
        #for i, sample in zip(range(len(samples)), samples):
            #variables.append(IntVar())
            #m.add_checkbutton(label=sample, variable=var1)

        for sample in samples:
            if sample == '':
                continue
            variables.append(IntVar(value=1))
            m.add_checkbutton(label=sample, variable=variables[-1])
    return func

sample.bind('<Key>', add_checkbutton(menu))

mb.pack()

# Remove "Option 1" (index 0)
#menu.delete(0)

root.mainloop()