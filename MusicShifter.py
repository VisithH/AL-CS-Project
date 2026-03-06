import tkinter as tk
from tkinter import ttk, Button

from django.contrib.messages import success

# from MS_Main import test
from ProjectLibrary import databaseGet
from ProjectLibrary.Spotify_oauth import spotify_oauth
from ProjectLibrary.passwordValidator import password_validator


class step_1(ttk.Frame):
    def __init__(self, parent, go_next, user_in_session):
        super().__init__(parent)
        self.user_in_session = user_in_session
        # self.configure(bg="#0d1b2a")
        self.account_sign_in(go_next)
        # self.account_sign_in_oldtk(go_next)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

    def account_sign_in_oldtk(self, go_next):
        tk.Label(self, text=f"Welcome, {self.user_in_session}").grid(row=0, column=1, pady=(6, 0))
        tk.Button(self, text="Spotify Login", command=lambda: self.spotify_sign_in(), font=["Century Gothic", 12],
                  width=15, bg="#b8fce2").grid(row=1, column=1, pady=5)
        tk.Button(self, text="soundcloud Login", command=lambda: self.soundcloud_sign_in(), font=["Century Gothic", 12],
                  width=15, bg="#fcbeb8").grid(row=2, column=1, pady=5)
        tk.Button(self, text="Next", command=lambda: go_next, font=["Century Gothic", 12],
                  width=15, bg="#fcbeb8").grid(row=3, column=1, pady=5)

    def account_sign_in(self, go_next):
        ttk.Label(self, text=f"Welcome, {self.user_in_session}").grid(row=0, column=1, pady=(6, 0))
        tk.Button(self, text="Spotify Login", command=lambda: self.spotify_sign_in(), font=["Century Gothic", 12],
                  width=15, bg="#b8fce2").grid(row=1, column=1, pady=5)
        # tk.Button(self, text="soundcloud Login", command=lambda: self.soundcloud_sign_in(), font=["Century Gothic", 12],
        #           width=15, bg="#fcbeb8").grid(row=4, column=1, pady=5)
        ttk.Button(self, text="Next", command=go_next, width=15).grid(row=6, column=1, pady=5)

    def spotify_sign_in(self):
        try:
            spotify_oauth()
            accessToken = databaseGet.get_from_database_validation('spotify_token', self.user_in_session, 'token',
                                                                   'username')
            print(accessToken)
            ttk.Label(self, text="Spotify Login is successful").grid(row=3, column=1, pady=(6, 0))
        except:
            ttk.Label(self, text="Unsuccessful attempt, Try Again!").grid(row=3, column=1, pady=(6, 0))

    # def soundcloud_sign_in(self):
    #     try:
    #         soundcloud_API()
    #         accessToken = databaseGet.get_from_database_validation('tokens', self.user_in_session, 'soundcloud_token', 'username')
    #         print(accessToken)
    #         ttk.Label(self, text="soundcloud Login is successful").grid(row=5, column=1, pady=(6, 0))
    #     except:
    #         ttk.Label(self, text="Unsuccessful attempt, Try Again!").grid(row=5, column=1, pady=(6, 0))


class step_2(ttk.Frame):
    def __init__(self, parent, go_next, go_back):
        super().__init__(parent)
        self.setup_layout(go_back, go_next)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

    def setup_layout(self,go_back, go_next):
        self.yt_to_spotify_tick = tk.IntVar()
        self.spotify_to_yt_tick = tk.IntVar()

        self.yt_to_spoify = ttk.Checkbutton(self, text='Youtube Music to Spotify', variable=self.yt_to_spotify_tick, onvalue=1, offvalue=0).grid(row=4, column=2)
        self.spotify_to_ytmusic = ttk.Checkbutton(self, text='Spotify to Youtube Music', variable=self.spotify_to_yt_tick, onvalue=1, offvalue=0).grid(row=5, column=2)
        ttk.Button(self, text='Back', command=go_back).grid(row=6, column=1)
        ttk.Button(self, text='Submit', command=self.submit).grid(row=6, column=2)
        ttk.Button(self, text='Next', command=go_next).grid(row=6, column=3)

    def submit(self):
        yt_to_spotify = self.yt_to_spotify_tick.get()
        if yt_to_spotify == 1:
            print('success')
        else:
            print('None')

class step_3(ttk.Frame):
    def __init__(self, parent, go_back):
        super().__init__(parent)
        self.setup_layout(go_back)

    def setup_layout(self, go_back):
        ttk.Label(self, text="Hello").pack(fill="both")
        ttk.Button(self, text='Back', command=go_back).pack(fill="both")


class music_shifter(tk.Frame):
    def __init__(self, windowRef: tk.Tk, user_in_session):
        super().__init__(windowRef)
        windowRef.geometry("600x300")
        self.user_in_session = user_in_session
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.go_to_step1()

    def clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def go_to_step1(self):
        self.clear()
        step_1(self.container, go_next=self.go_to_step2, user_in_session=self.user_in_session).pack(fill="both",
                                                                                                    expand=True)

    def go_to_step2(self):
        self.clear()
        step_2(self.container, go_back=self.go_to_step1, go_next=self.go_to_step3).pack(fill="both", expand=True)

    def go_to_step3(self):
        self.clear()
        step_3(self.container, go_back=self.go_to_step2).pack(fill="both", expand=True)
