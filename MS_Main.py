import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ProjectLibrary.databaseGet import getFromDatabaseValidation
from ProjectLibrary.Spotify_oauth import spotify_oauth

class spotifyToDeezer:
    def __init__(self, user):
        self.userPlaylists = None
        self.user = user
        self.accessTokenSpotify = None
        self.sp = None
        self.accessTokenDeezer = None
        self.main()

    def main(self):
        self.accessTokenSpotify = getFromDatabaseValidation('spotifyDetails', self.user,'accessToken','username')
        spotify_oauth(self.user,'Visith@gmail.com')
        self.sp = spotipy.Spotify(auth=f"{self.accessTokenSpotify}")


    def displayName(self):
        me = self.sp.current_user()
        return me["display_name"]

    def userPlaylistNames(self):
        self.userPlaylists = []
        userTrackNames = self.sp.current_user_playlists(50, 0)
        for userTrackName in userTrackNames["items"]:
            self.userPlaylists.append([userTrackName['name'],userTrackName['id']])

        print(self.userPlaylists)

    def shifterSpotifyToDeezer(self,selectedPlaylist):
        self.userTracks = self.sp.playlist_items()
        print(self.userTracks)
        spotify_tracks = []
        for item in self.userTracks["items"]:
            track = item["track"]
            name = track["name"]
            artist = track["artists"][0]["name"]
            spotify_tracks.append([name, artist])

x: spotifyToDeezer = spotifyToDeezer('Visith')