import tkinter as tk
from ProjectLibrary.LoginAccount import loginRegistrationFrame

class mainProgram(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Registraton")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.configure(bg="#ff8000")
        loginRegistrationFrame(self)
        self.mainloop()

if __name__ == '__main__':
    x: mainProgram = mainProgram()