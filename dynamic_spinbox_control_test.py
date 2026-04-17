from tkinter import *

root = Tk()
root.columnconfigure(0, weight=4)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=4)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

def spinbox_handler(spinbox, element_frame, sample_frame):
    print(f'initial child cound: {len(element_frame.winfo_children())}')
    def func():
        count = int(spinbox.get())
        child_count = len(element_frame.winfo_children())
        print(f'count {count}')
        print(f'child_count {child_count}')
        if count>child_count:
            for i in range(count-child_count):
                entry = Entry(element_frame, name=f'entry_{child_count}')
                entry.pack(side='top')
                button = Button(sample_frame, text='select', name=f'button_{child_count}')
                button.pack(side='top')
        elif child_count>count:
            print('True')
            for i in reversed(range(count, child_count)):
                element_frame.nametowidget(f'entry_{i}').destroy()
                sample_frame.nametowidget(f'button_{i}').destroy()


    return func

spin_1 = Spinbox(root, from_=1, to=10, width=2)
spin_1.grid(row=0, column=1)

spin_2 = Spinbox(root, from_=1, to=10, width=2)
spin_2.grid(row=1, column=1)

element_frame_1 = Frame(root, bg='blue')
element_frame_1.grid(row=0, column=0, sticky='nsew')
sample_frame_1 = Frame(root, bg='blue')
sample_frame_1.grid(row=0, column=2, sticky='nsew')

entry_1 = Entry(element_frame_1)
entry_1.pack(side='top')
button_1 = Button(sample_frame_1, text='select')
button_1.pack(side='top')

spin_1.config(command=spinbox_handler(spin_1, element_frame_1, sample_frame_1))

element_frame_2 = Frame(root, bg='red')
element_frame_2.grid(row=1, column=0, sticky='nsew')
sample_frame_2 = Frame(root, bg='red')
sample_frame_2.grid(row=1, column=2, sticky='nsew')

entry_2 = Entry(element_frame_2)
entry_2.pack(side='top')
button_2 = Button(sample_frame_2, text='select')
button_2.pack(side='top')

spin_2.config(command=spinbox_handler(spin_2, element_frame_2, sample_frame_2))

root.geometry('500x500')



root.mainloop()