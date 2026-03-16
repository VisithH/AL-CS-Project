import tkinter as tk
from tkinter import ttk, Button

from django.contrib.messages import success

from MS_Main import YtmusicToSpotify, SpotifyToYtmusic
# from MS_Main import test
from ProjectLibrary import databaseGet
from ProjectLibrary.Spotify_oauth import spotify_oauth
from ProjectLibrary.databaseGet import get_from_database, get_from_database_everyrow
from ProjectLibrary.passwordValidator import password_validator
from ProjectLibrary.youtubemusic_oauth import ytmusic_oauth





class step_1(ttk.Frame):
    def __init__(self, parent, go_next, user_id, globals):
        super().__init__(parent)
        self.user_id = user_id
        # self.configure(bg="#0d1b2a")
        self.globals = globals
        self.account_sign_in(go_next)
        # self.account_sign_in_oldtk(go_next)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

    def account_sign_in(self, go_next):
        username = get_from_database('users',self.user_id,'username','user_id')
        ttk.Label(self, text=f"Welcome, {username}").grid(row=0, column=1, pady=(6, 0))
        tk.Button(self, text="Spotify Login", command=lambda: self.spotify_sign_in(), font=["Century Gothic", 12],
                  width=20, bg="#b8fce2").grid(row=1, column=1, pady=5)
        tk.Button(self, text="YouTube Music Login", command=lambda: self.ytmusic_sign_in(), font=["Century Gothic", 12],
                  width=20, bg="#fcbeb8").grid(row=4, column=1, pady=5)
        ttk.Button(self, text="Next", command=go_next, width=15).grid(row=6, column=1, pady=5)

    def spotify_sign_in(self):
        try:
            self.globals.access_token_s = spotify_oauth()
            print(self.globals.access_token_s)
            ttk.Label(self, text="Spotify Login is successful").grid(row=3, column=1, pady=(6, 0))
        except:
            ttk.Label(self, text="Unsuccessful attempt, Try Again!").grid(row=3, column=1, pady=(6, 0))

    def ytmusic_sign_in(self):
        self.globals.access_token_yt = ytmusic_oauth()
        print(self.globals.access_token_yt)
        if self.globals.access_token_yt != None:
            ttk.Label(self, text="YouTube Music Login is successful").grid(row=5, column=1, pady=(6, 0))
        else:
            ttk.Label(self, text="Unsuccessful attempt, Try Again!").grid(row=5, column=1, pady=(6, 0))


class step_2(ttk.Frame):
    def __init__(self, parent, go_next, go_back,user_id, globals):
        super().__init__(parent)
        self.error_confirmation = None
        self.go_next = go_next
        self.label = None
        self.user_id= user_id
        self.globals=globals
        self.setup_layout(go_back, go_next)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

    def setup_layout(self,go_back, go_next):
        self.yt_to_spotify_tick = tk.IntVar()
        self.spotify_to_yt_tick = tk.IntVar()

        ttk.Label(self, text="Select one of the following transfer-way").grid(row=0, column=2, pady=(6, 0))
        ttk.Label(self, text="After that select the playlist that you wish to transfer and click confirm").grid(row=1, column=2, pady=(2, 0))
        # ttk.Label(self, text="Paste the Id represented by xxx").grid(row=2, column=2, pady=(2, 0))

        # self.playlist_id_entry = tk.Entry(self, font=["Century Gothic", 10], width=40)
        # self.playlist_id_entry.grid(row=3, column=2, pady=(2, 2))

        self.yt_to_spoify = ttk.Checkbutton(self, text='Youtube Music to Spotify', variable=self.yt_to_spotify_tick, onvalue=1, offvalue=0).grid(row=4, column=2, pady=(2, 0))
        self.spotify_to_ytmusic = ttk.Checkbutton(self, text='Spotify to Youtube Music', variable=self.spotify_to_yt_tick, onvalue=1, offvalue=0).grid(row=5, column=2, pady=(2, 0))
        ttk.Button(self, text='Back', command=go_back).grid(row=6, column=1, pady=(2, 0))
        self.submit_button = ttk.Button(self, text='Submit', command=self.submit)
        self.submit_button.grid(row=6, column=2, pady=(2, 0))
        ttk.Button(self, text='Next', command=self.error).grid(row=6, column=3, pady=(2, 0))

        self.label = ttk.Label(self,text="")
        self.label.grid(row=7, column=1, columnspan=3, pady=(5, 0))

    def error(self):
        self.label.config(text="Follow through the steps after submit to continue")
    def submit(self):
        self.label.config(text='')
        yt_to_spotify = self.yt_to_spotify_tick.get()
        spotify_to_yt_tick = self.spotify_to_yt_tick.get()
        # self.playlist_id: str = self.playlist_id_entry.get()
        if spotify_to_yt_tick == 1 and yt_to_spotify == 1:
            self.label.config(text='')
            self.label.config(text="Select only one of the options above")

        elif yt_to_spotify == 1:
            self.yt_to_spotify_tk()
        elif spotify_to_yt_tick == 1:
            self.submit_button.grid_forget()
            self.spotify_to_yt_tk()
        else:
            self.label.config(text='')
            self.label.config(text="Select one of the options above")
            print('None')

    def yt_to_spotify_tk(self):
        YtmusicToSpotify.playlists_get(self, credentials=self.globals.access_token_yt)
        print(self.playlists)
        playlists = get_from_database_everyrow('playlists','playlist_name','playlist_id')

        self.x = 9
        self.selected_option_id = []

        for playlist in playlists:
            self.select_bool = tk.IntVar()
            self.spoify_to_yt= ttk.Checkbutton(self, text=f'{playlist[0]}', onvalue=1, variable=self.select_bool,
                                                offvalue=0)
            self.spoify_to_yt.grid(row=self.x, column=2, pady=(2, 0))
            print((playlist, self.select_bool))
            print(f'{playlist},{self.select_bool}')
            self.selected_option_id.append((playlist[1], self.select_bool))
            self.x = self.x + 1

        # ttk.Button(self, text='Confirm', command=self.confirm).grid(row=self.x, column=2, pady=(5, 0))
        # self.songs = YtmusicToSpotify.track_get(self, playlist_id=playlist_id)
        # if self.songs not in (None, False):
        #     print('YAAAAYYY')
        #     self.label.config(text='')
        #     self.label.config(text="Songs have been successfully retrieved!")
        #     state = YtmusicToSpotify.song_transfer(self, tracks=self.songs, sp=self.globals.access_token_s)
        #     if state != False:
        #         self.submit_button.grid_forget()
        #         ttk.Label(self, text="Songs have been transferred!").grid(row=8, column=2)
        #         ttk.Button(self, text='Next', command=self.go_next).grid(row=6, column=3, pady=(2, 0))
        #
        #         ttk.Label(self, text="You can click next to see your insight").grid(row=9, column=2)

        if self.songs == None:
            self.label.config(text='')
            self.label.config(text='Playlist does not contain any songs')
            # ttk.Label(self, text="Playlist doesnt contain any songs").grid(row=7, column=2, pady=(10,0))

        if self.songs == False:
            self.label.config(text='')
            self.label.config(text='Enter a valid playlist ID')
    def spotify_to_yt_tk(self):
        playlists_exist = SpotifyToYtmusic.spotify_playlist_get(self,sp=self.globals.access_token_s)
        if playlists_exist == None:
            self.label.config(text='No playlists were found in your spotify account')
        self.playlists = get_from_database_everyrow('playlists','playlist_name','playlist_id','source_platform','Spotify')
        print(self.playlists)

        self.x = 9
        self.selected_option = []

        for playlist in self.playlists:
            self.select_bool = tk.IntVar()
            self.yt_to_spoify = ttk.Checkbutton(self, text=f'{playlist[0]}', onvalue=1, variable=self.select_bool, offvalue=0)
            self.yt_to_spoify.grid(row=self.x, column=2, pady=(2, 0))
            print((playlist,self.select_bool))
            print(f'{playlist},{self.select_bool}')
            self.selected_option.append((playlist,self.select_bool))
            self.x = self.x+1

        ttk.Button(self, text='Confirm', command=self.confirm).grid(row=self.x, column=2, pady=(5, 0))

    def confirm(self):
        selection = []
        self.error_confirmation = ttk.Label(self, text="")
        self.error_confirmation.grid(row=self.x+1, column=2, pady=(5, 0))
        for select in self.selected_option:
            if select[1].get() == 1:
                selection.append(select[0])

        if len(selection) >= 2:
            self.error_confirmation.config(text="")
            self.error_confirmation.config(text="More than one playlist have been selected")
        elif len(selection) == 1:
            self.error_confirmation.config(text="")
            print(selection)  # -> selection[0] is name and 1 is id
            self.selected_playlist_id = selection[0][1]
            self.selected_playlist_name = selection[0][0]
            SpotifyToYtmusic.playlist_track_get(self, sp=self.globals.access_token_s, playlist=self.selected_playlist_id)
            tracks = get_from_database_everyrow('tracks','track_name','track_id','playlist_id',self.selected_playlist_id)
            print('tracks')
            print(tracks)
            transfer = SpotifyToYtmusic.track_transfer(self, credentials=self.globals.access_token_yt,
                                                       playlist_selected=self.selected_playlist_name,
                                                       tracks_given=tracks)
            print(f"testing status{transfer}")
            if transfer != False:
                self.error_confirmation.config(text="Songs have been transferred, click next to continue")
                # ttk.Label(self, text="Songs have been transferred!").grid(row=self.x+2, column=2)
                ttk.Button(self, text='Next', command=self.go_next).grid(row=6, column=3, pady=(2, 0))

            else:
                self.error_confirmation.config(text="Error! Proceed back and try again")

                # ttk.Label(self, text="").grid(row=self.x+1, column=2)
        elif len(selection) == 0:
            self.error_confirmation.config(text="")
            self.error_confirmation.config(text="No playlists have been selected")




class step_3(ttk.Frame):
    def __init__(self, parent, go_back,user_id, globals):
        super().__init__(parent)
        self.user_id= user_id
        self.globals = globals
        self.setup_layout(go_back)


    def setup_layout(self, go_back):
        ttk.Label(self, text="Hello").pack(fill="both")
        # ttk.Button(self, text='Back', command=go_back).pack(fill="both")


class music_shifter(tk.Frame):
    def __init__(self, windowRef: tk.Tk, user_id):
        super().__init__(windowRef)
        self.config(width=600,height=600)
        self.pack_propagate(False)
        self.access_token_s = None
        self.access_token_yt = None
        self.user_id = user_id
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.go_to_step1()
        self.update()

    def clear(self):
        widgets = self.container.winfo_children()
        for widget in widgets:
            widget.destroy()

    def go_to_step1(self):
        self.clear()
        step_1(self.container, go_next=self.go_to_step2, user_id=self.user_id, globals=self).pack(fill="both", expand=True)

    def go_to_step2(self):
        self.clear()
        step_2(self.container, go_back=self.go_to_step1, go_next=self.go_to_step3, user_id=self.user_id, globals = self).pack(fill="both", expand=True)

    def go_to_step3(self):
        self.clear()
        step_3(self.container, go_back=self.go_to_step2, user_id=self.user_id, globals=self).pack(fill="both", expand=True)
