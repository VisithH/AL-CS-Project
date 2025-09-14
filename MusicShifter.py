import tkinter as tk

from ProjectLibrary import databaseGet
from ProjectLibrary.SpotifyOauth import spotifyOauth


class musicShifter(tk.Frame):
    def __init__(self, windowRef: tk.Tk, userInSession):
        super().__init__(windowRef)
        windowRef.geometry("600x300")
        self.userInSession = userInSession
        self.configure(bg="#0d1b2a")
        self.accountSignIn()
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(3,weight=1)

    def accountSignIn(self):
        tk.Label(self, text=f"Welcome, {self.userInSession}").grid(row=0,column=1,pady=(6,0))
        tk.Button(self, text="Spotify Login", command=lambda: self.spotify_sign_in(), font=["Century Gothic", 12],
                  width=15,bg="#b8fce2").grid(row=1, column=1,pady=5)
        tk.Button(self, text="Deezer Login", command=lambda: self.deezer_sign_in(), font=["Century Gothic", 12],
                  width=15,bg="#fcbeb8").grid(row=2, column=1,pady=5)

    def spotify_sign_in(self):
        email = databaseGet.getFromDatabaseValidation('users', self.userInSession, 'email', 'username')
        spotifyOauth(self.userInSession, email)
        accessToken = databaseGet.getFromDatabaseValidation('spotifyDetails', email, 'accessToken', 'userEmail')
        print(accessToken)

    def deezer_sign_in(self):
        pass