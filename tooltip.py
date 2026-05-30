import tkinter as tk

AUTO_CLOSE = 3000

BACKGROUND = '#e6e6e6'
ACTIVE_BACKGROUND = '#5a5a5a'

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None
        self.after_id = None

        widget.bind('<Enter>', self.schedule_tip)
        widget.bind('<Leave>', self.cancel_tip)

    def schedule_tip(self, event):
        self.after_id = self.widget.after(500, self.show)

    def show(self):
        self.widget.config(activebackground=ACTIVE_BACKGROUND, activeforeground='white', cursor='hand2')
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty()

        self.tip_window = tk.Toplevel(self.widget)

        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f'+{x}+{y}')

        tip = tk.Label(
            self.tip_window,
            text='selected sample(s) for digestion',
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


#root = tk.Tk()

#button = tk.Button(root, text='click me')
#button.pack(padx=40, pady=40)

#ToolTip(button)

#root.mainloop()