import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ProjectLibrary.databaseGet import getFromDatabaseValidation
from ProjectLibrary.Spotify_oauth import spotify_oauth

class spotifyToDeezer:
    def __init__(self, user):
        self.user = user
        self.accessTokenSpotify = None
        self.sp = None
        self.accessTokenDeezer = None
        self.shifter()

    def shifter(self):
        self.accessTokenSpotify = getFromDatabaseValidation('spotifyDetails', self.user,'accessToken','username')
        spotify_oauth(self.user,'Visith@gmail.com')

        me = self.sp.current_user()
        print(me["display_name"])




x: spotifyToDeezer = spotifyToDeezer('Visith')