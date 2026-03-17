import json
import os
import pickle
import time
from datetime import datetime

import isoduration
import spotipy
from django.contrib.messages.api import success
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from ProjectLibrary.youtubemusic_oauth import ytmusic_oauth
from ProjectLibrary.Spotify_oauth import spotify_oauth
from ProjectLibrary.databaseGet import get_from_database, get_from_database_keys, get_from_database_everyrow
from ProjectLibrary.databaseInsert import insert_into_table, modify_field

class SpotifyToYtmusic:
    def __init__(self, user_id):
        self.user_playlists = None
        self.user_id = user_id
        self.access_token_spotify = None
        self.sp = None
        self.access_token_ytmusic = None

    def spotify_playlist_get(self,sp):
        playlists = sp.current_user_playlists()
        playlist_id_return = None
        for playlist in playlists['items']:
            playlist_id_return = insert_into_table('playlists',[self.user_id, playlist['name'], 'Spotify', playlist['id'],'Youtube Music',playlist['tracks']['total'],None])
        return playlist_id_return

    def playlist_track_get(self,sp,playlist):
        self.playlist_id = playlist
        result = sp.playlist_tracks(playlist)
        number_of_tracks=0
        print(f'printing playlist id: {playlist}')
        for track in result['items']:
            number_of_tracks = number_of_tracks + 1
            artists_data = track['track']['artists']
            track_id=insert_into_table('tracks',[playlist,track['track']['name'], None ,track['track']['popularity'],track['track']['explicit'],track['track']['duration_ms'],None,None,None,None])
            print(f'statusfortrackupdate:{track_id}')
            artists_list = []
            for artist in artists_data:
                print(artist['name'])
                artists_list.append(artist['name'])

            artists = " ".join(artists_list)
            status = modify_field('tracks', artists, 'artists', 'track_id', track_id)
            print(f'artistinsert: {status}')

        status = modify_field('playlists',number_of_tracks,'number_of_tracks','playlist_id',playlist)
        print(f'insertdatabasestatus: {status}')
        return status

    def track_transfer(self, credentials, playlist_selected, tracks_given):
        try:
            youtube = build("youtube", "v3", credentials=credentials)
            print('selected pla')
            print(playlist_selected)
            playlist_new = youtube.playlists().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': playlist_selected,
                        'description': 'None',
                    },
                    'status': {
                        'privacyStatus': 'private'
                    }
                }
            )

            playlist_new = playlist_new.execute()
            print(playlist_new)
            print('track given')
            print(tracks_given)
            success_score = 0
            for track in tracks_given:
                try:
                    track_id = track[1]
                    self.track_data = get_from_database_everyrow('tracks', 'track_name', 'artists', 'track_id',track[1])
                    print(f'track name: {self.track_data[0][0]}')
                    print(f'track artists: {self.track_data[0][1]}')
                    # print('printing track')
                    # print(track)
                    # artist_line = track['artists']
                    track_search = f"{self.track_data[0][0]} {self.track_data[0][1]}"
                    search = youtube.search().list(
                        part='snippet',
                        q=track_search,
                        type='video',
                        maxResults = 1
                    )
                    video = search.execute()
                    stats = youtube.videos().list(
                        part='statistics,contentDetails',
                        id=video['items'][0]['id']['videoId']
                    )
                    stats = stats.execute()
                    print('testing')
                    print(video['items'][0]['id']['videoId'])

                    add = youtube.playlistItems().insert(
                        part='snippet',
                        body={
                            'snippet': {
                                'playlistId': playlist_new['id'],
                                'resourceId': {
                                    'kind': 'youtube#video',
                                    'videoId': video['items'][0]['id']['videoId']
                                }
                            }
                        }
                    )
                    add.execute()

                    status = modify_field('tracks', stats['items'][0]['statistics']['viewCount'], 'ytmusic_views', 'track_id', track_id)
                    status = modify_field('tracks', stats['items'][0]['statistics']['likeCount'], 'ytmusic_likes','track_id' , track_id)
                    status = modify_field('tracks', stats['items'][0]['contentDetails']['duration'], 'ytmusic_duration','track_id' , track_id)
                    success_score = success_score+1

                except:
                    print('did not transfer')
            status = modify_field('playlists', success_score, 'success_score', 'playlist_id', self.playlist_id)
            return status
        except Exception as e:
            print(f'Error on song transfer: {e}')
            return False

class YtmusicToSpotify:
    def __init__(self, user_id):
        self.user_id = user_id
        self.credentials = None
        self.api_key = "AIzaSyAjAni8t-CJOEHBLwen28iDzTXDprHoOfQ"  # this will be removed later on

    def playlists_get(self, credentials):
        self.credentials = credentials
        youtube = build("youtube", "v3", credentials=self.credentials)
        playlists = youtube.playlists().list(
            part = "snippet,contentDetails",
            maxResults = 25,
            mine = True
        )
        playlists = playlists.execute()
        print(playlists['items'])
        for playlist in playlists['items']:
            insert_into_table('playlists',[self.user_id, playlist['snippet']['title'], 'Youtube Music', playlist['id'],'Spotify',playlist['contentDetails']['itemCount'],None])
        print(playlists['items'][0]['id'])
        print(playlists['items'][0]['snippet']['title'])

    def track_get(self, playlist):
        try:
            self.playlist_id = playlist
            print(f'printing playlist id: {self.playlist_id}')
            api_key = "AIzaSyAjAni8t-CJOEHBLwen28iDzTXDprHoOfQ" # will be removed later
            youtube = build("youtube", "v3", developerKey=api_key)

            track_list = youtube.playlistItems().list(
                part = 'snippet',
                playlistId = self.playlist_id
            )
            track_list = track_list.execute()
            print('track_list')
            print(track_list)
            number_of_tracks = []
            for track in track_list['items']:


                print('track')
                print(track)
                title = track['snippet']['title']
                print(f'title {title}')
                video_id = track['snippet']['resourceId']['videoId']
                artist_part = track['snippet']['description'].splitlines()[2]
                description = track['snippet'].get('descriptions', '')
                print(description)
                description_part = description.splitlines()
                print('description_part')
                print(description_part)
                track_id = insert_into_table('tracks', [self.playlist_id, title, None,
                                                        None, None,
                                                        None, None, None, None, None])

                artists_list = []
                for name in artist_part.split(' · ')[1: ]:
                    # print(f'name: {name}')
                    artists_list.append(name)
                artists = " ".join(artists_list)
                status = modify_field('tracks', artists, 'artists', 'track_id', track_id)
                print(f'artists insert:{status}')

                stats = youtube.videos().list(
                    part='statistics,contentDetails',
                    id = video_id
                )

                stats = stats.execute()
                print(f'printing {stats}')
                status = modify_field('tracks', stats['items'][0]['statistics']['viewCount'], 'ytmusic_views',
                                      'track_id', track_id)
                print(f'stats insert:{status}')

                status = modify_field('tracks', stats['items'][0]['statistics']['likeCount'], 'ytmusic_likes',
                                      'track_id', track_id)
                print(f'stats insert:{status}')

                status = modify_field('tracks', stats['items'][0]['contentDetails']['duration'], 'ytmusic_duration',
                                      'track_id', track_id)
                print(f'stats insert:{status}')
                status = modify_field('tracks', 0, 'transfer_status',
                                      'track_id', track_id)
                print(f'transfer_status: {status}')


            status = modify_field('playlists', number_of_tracks, 'number_of_tracks','playlist_id', self.playlist_id)
            print(f'modifystatusno{status}')
            return status
        except:
            return False

    def song_transfer(self, playlist_selected, tracks, sp):
        try:

            user = sp.current_user()
            new_playlist = sp.user_playlist_create(
                user = user["id"],
                name = playlist_selected,
                public = True,
                collaborative = False,
                description = ""
            )

            print(new_playlist['id'])
            success_score = 0
            for track in tracks:
                track_id = track[1]
                self.track = get_from_database_everyrow('tracks', 'track_name', 'artists', 'track_id', track[1])
                print(f'track name: {self.track[0][0]}')
                print(f'track artists: {self.track[0][1]}')
                search_string = f"track:{self.track[0][0]} artist:{self.track[0][1]}"
                result = sp.search(q=search_string, type='track')
                print(result)
                track_data = result['tracks']['items']
                print(track_data)
                if track_data:
                    sp.playlist_add_items(
                        playlist_id=new_playlist['id'],
                        items=[track_data[0]['uri']],
                        position=None
                    )
                    print(track_data[0]['popularity'])
                    print(track_id)
                    status = modify_field('tracks', track_data[0]['popularity'], 'spotify_popularity',
                                          'track_id', track_id)
                    print(f'statuspopularity{status}')

                    status = modify_field('tracks', track_data[0]['explicit'], 'spotify_explicit',
                                          'track_id', track_id)
                    print(f'statusexplicit{status}')

                    status = modify_field('tracks', track_data[0]['duration_ms'], 'spotify_duration',
                                          'track_id', track_id)
                    print(f'statusduration{status}')
                    status = modify_field('tracks', 1, 'transfer_status',
                                          'track_id', track_id)
                    print(f'transfer_status: {status}')

                    success_score = success_score + 1
                else:
                    status = modify_field('tracks', 2, 'transfer_status',
                                          'track_id', track_id)
                    print(f'transfer_status: {status}')
            status = modify_field('playlists', success_score, 'success_score', 'playlist_id', self.playlist_id)
            print(f'success_scoreinput{status}')
            return status
        except Exception as e:
            print(f'your error was {e}')
            return False


if __name__ == '__main__':
    from ProjectLibrary.youtubemusic_oauth import ytmusic_oauth
    # x: SpotifyToYtmusic = SpotifyToYtmusic('Visith')
    # y: YtmusicToSpotify = YtmusicToSpotify('Visith')
    # access_token_yt = ytmusic_oauth()
    # y.playlists_get(access_token_yt)
    from googleapiclient.discovery import build
    credentials = ytmusic_oauth()

    def youtube_auth(credentials):
        youtube = build("youtube", "v3", credentials=credentials, cache_discovery=False)

        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": "Sample playlist created via API",
                    "description": "This is a sample playlist description.",
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = request.execute()

        print('response')
        print(response)
        track_search = 'Passion Fruit Drake'
        search = youtube.search().list(
            part='snippet',
            q=track_search,
            type='video',
            maxResults=1
        )
        search = search.execute()
        print(search)
        stats = youtube.videos().list(
            part='statistics,contentDetails',
            id=search['items'][0]['id']['videoId']
        )
        stats = stats.execute()
        print('testing')
        print(search['items'][0]['id']['videoId'])

        add = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': response['id'],
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': search['items'][0]['id']['videoId']
                    }
                }
            }
        )
        add.execute()
    youtube_auth(credentials)