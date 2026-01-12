import tkinter as tk
from MusicShifter import music_shifter
from LoginAccount import login_registration_frame

class main_program(tk.Tk):
    def __init__(self):
        super().__init__()
        self.userInSession = None
        self.title("Music Shifter")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # self.configure(bg="#ff8000")
        self.login_launch()

    def login_launch(self):
        # LoginFrame(self, backToLRF=self.setUserInSession)
        login_registration_frame(self, back_to_main=self.set_user_in_session).pack(expand=True, fill="both")

    def set_user_in_session(self, username):
        self.userInSession = username
        for widget in self.winfo_children():
            widget.destroy()
        self.music_shifter_launch()

    def music_shifter_launch(self):
        music_shifter(self, self.userInSession).pack(expand=True,fill="both")


if __name__ == '__main__':
    x: main_program = main_program()
    x.mainloop()