import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ProjectLibrary.databaseGet import get_from_database_validation
from ProjectLibrary.Spotify_oauth import spotify_oauth

class spotify_to_soundcloud:
    def __init__(self, user):
        self.user_playlists = None
        self.user = user
        self.access_token_spotify = None
        self.sp = None
        self.access_token_soundcloud = None
        self.main()

    def main(self):
        self.sp = spotify_oauth()
        self.spotify_playlist_get()

    def display_name(self):
        me = self.sp.current_user()
        return me["display_name"]

    def spotify_liked_tracks_get(self):
        tracks = self.sp.current_user_saved_tracks()
        print(tracks)

    def spotify_playlist_get(self):
        playlists = self.sp.current_user_playlists()
        playlist_names = []
        for playlist in playlists['items']:
            playlist_names.append([playlist['name'],playlist['id']])
            # print(playlist['name'])
            # print(playlist['id'])
        return playlist_names
        # return self.playlist_track_get(playlist_names[0][1])

    def playlist_track_get(self, playlist):
        tracks = []
        result = self.sp.playlist_tracks(playlist)
        for track in result['items']:
            # The whole thing and the with ['track'] it only gives the data relating to the track and removes the date added and info
            # print(track)
            print(track['track']['name'])
            tracks.append(track['track'])

        # print(tracks[1]['name'])
        return tracks

    def matchTracks(self, tracks):
        for track in tracks:
            score = 0

x: spotify_to_soundcloud = spotify_to_soundcloud('Visith')