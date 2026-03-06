import json
import os
import pickle
from datetime import datetime

import spotipy
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.helpers import credentials_from_session
from spotipy.oauth2 import SpotifyOAuth
from google.oauth2.credentials import Credentials

from ProjectLibrary import databaseGet
from ProjectLibrary.Spotify_oauth import spotify_oauth
from ProjectLibrary.databaseInsert import insert_into_table


class SpotifyToYtmusic:
    def __init__(self, user):
        self.user_playlists = None
        self.user = user
        self.access_token_spotify = None
        self.sp = None
        self.access_token_ytmusic = None
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
            print(playlist['id'])
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

    def match_tracks(self, tracks):
        for track in tracks:
            score = 0

class YtmusicToSpotify:
    def __init__(self,user):
        self.user = user
        self.authenticate()

    def authenticate(self):
        scope = 'https://www.googleapis.com/auth/youtube'
        file_name = 'ProjectLibrary/token.pickle'
        credentials = None
        username_exists = databaseGet.get_from_database_validation('youtubemusic_token', self.user, 'username',
                                                                   'username')

        if username_exists!= None:
            data = databaseGet.get_from_database_all('youtubemusic_token', self.user, 'username')
            credentials = Credentials(
                token = data[0],
                refresh_token=data[1],
                token_uri=data[2],
                client_id=data[3],
                client_secret=data[4],
                scopes=json.loads(data[5])
            )

            credentials.expiry = datetime.fromisoformat(data[6])

        

        if not file_there:
            flow = InstalledAppFlow.from_client_secrets_file(
                'ProjectLibrary/client_secret.json', scope
            )

            credentials = flow.run_local_server(port=52736,
                                                access_type='offline',
                                                prompt='consent')
            insert_into_table('youtubemusic_token',[self.user,credentials.token,credentials.refresh_token,credentials.token_uri,credentials.client_id,
                                                    credentials.client_secret, json.dumps(credentials.scopes),credentials.expiry.isoformat()])
            print('Done')
# x: SpotifyToYtmusic = SpotifyToYtmusic('Visith')
y: YtmusicToSpotify = YtmusicToSpotify('Visith')