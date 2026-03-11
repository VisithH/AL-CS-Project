import json
import os
import pickle
from datetime import datetime

import spotipy
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from ProjectLibrary.Spotify_oauth import spotify_oauth


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

    def song_transfer(self):
        youtube = build("youtube", "v3", developerKey=self.api_key)

class YtmusicToSpotify:
    def __init__(self,user):
        self.user = user
        self.sp = spotify_oauth()
        self.credentials = None
        self.api_key = "AIzaSyAjAni8t-CJOEHBLwen28iDzTXDprHoOfQ"  # this will be removed later on
        self.songs = self.song_get('PLACDKnlx5ifC65kxPaABKpB9W4Cty3Uzy')

        # state = self.authenticate()
        # if state == True:
        #     if self.songs != False:
        #         pass

    def authenticate(self): # some of these code is relied on google api webpage
        scope = 'https://www.googleapis.com/auth/youtube'
        credentials = None
        flow = InstalledAppFlow.from_client_secrets_file('ProjectLibrary/client_secret.json', scope)

        self.credentials = flow.run_local_server(port=52736, access_type='offline', prompt='consent')

        # expiry_in_format = credentials.expiry.isoformat()

        # insert_into_table('youtubemusic_token',[self.user, credentials.token, credentials.refresh_token, credentials. token_uri, credentials.client_id,
        #                                         credentials.client_secret, credentials.scopes, expiry_in_format])
        print('token is successfully retrieved')
        return True
        # songs = self.song_get()
        # print(songs)


    def song_get(self,playlist_id):
        # try:
            api_key = "AIzaSyAjAni8t-CJOEHBLwen28iDzTXDprHoOfQ" # will be removed later
            youtube = build("youtube", "v3", developerKey=api_key)

            request = youtube.playlistItems().list(
                part = 'snippet',
                playlistId = playlist_id,
                maxResults = 100
            )
            # print(response)
            response = request.execute()

            songs = []

            for song in response['items']:
                print(song)
                title = song['snippet']['title']
                video_id = song['snippet']['resourceId']['videoId']
                artist_part = song['snippet']['description'].splitlines()[2]
                print(artist_part)
                artist = []
                for word in artist_part.split(' · ')[1: ]:
                    print(f'word: {word}')
                    artist.append(word)
                print(artist)
                songs.append({'track_title': title, 'artist': artist, 'video_id':video_id})

            for song in songs:
                print(song['video_id'])

            print(songs)
            if not songs:
                return None
            else:
                return songs
        # except:
        #     return False

    def song_transfer(self, songs):
        for song in songs:
            search_string = f"track:{song['track_title']} artist:{song['artist']}"
            # results = self.sp.search(q=f"track:{song['track_title']} artist:{song['artist']}", type='track')
            # print(results)
            return True


# x: SpotifyToYtmusic = SpotifyToYtmusic('Visith')
y: YtmusicToSpotify = YtmusicToSpotify('Visith')