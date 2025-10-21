import tkinter as tk
from MusicShifter import musicShifter
from LoginAccount import LoginFrame
from LoginAccount import loginRegistrationFrame

class mainProgram(tk.Tk):
    def __init__(self):
        super().__init__()
        self.userInSession = None
        self.title("Music Shifter")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # self.configure(bg="#ff8000")
        self.loginLaunch()

    def loginLaunch(self):
        # LoginFrame(self, backToLRF=self.setUserInSession)
        loginRegistrationFrame(self, backToMain=self.setUserInSession).pack(expand=True,fill="both")

    def setUserInSession(self,username):
        self.userInSession = username
        for widget in self.winfo_children():
            widget.destroy()
        self.musicShifterLaunch()

    def musicShifterLaunch(self):
        musicShifter(self, self.userInSession).pack(expand=True,fill="both")


if __name__ == '__main__':
    x: mainProgram = mainProgram()
    x.mainloop()