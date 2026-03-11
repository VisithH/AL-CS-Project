import tkinter as tk
from LoginAccount import login_registration_frame

class main_program(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Shifter")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.login_launch()

    def login_launch(self):
        login_registration_frame(self).pack(expand=True, fill="both")


if __name__ == '__main__':
    x: main_program = main_program()
    x.mainloop()