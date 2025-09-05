import tkinter as tk

class musicShifter(tk.Frame):
    def __init__(self, windowRef: tk.Tk, userInSession):
        super().__init__(windowRef)
        self.userInSession = userInSession
        self.configure(bg="#ff8000")
        self.accountSignIn()

    def accountSignIn(self):
        tk.Label(self, text=f"Welcome, {self.userInSession}").grid(row=1,column=1)