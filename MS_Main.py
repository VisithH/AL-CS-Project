import json
import os
import pickle
from datetime import datetime

import isoduration
import spotipy
from django.contrib.messages.api import success
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from ProjectLibrary.Spotify_oauth import spotify_oauth
from ProjectLibrary.databaseGet import get_from_database, get_from_database_keys
from ProjectLibrary.databaseInsert import insert_into_table, modify_field


# https://googleapis.github.io/google-api-python-client/ - main reference

class SpotifyToYtmusic:
    def __init__(self, user_id):
        self.user_playlists = None
        self.user_id = user_id
        self.access_token_spotify = None
        self.sp = None
        self.access_token_ytmusic = None
        self.main()

    def main(self):
        self.sp = spotify_oauth()

    def spotify_liked_tracks_get(self):
        tracks = self.sp.current_user_saved_tracks()
        print(tracks)

    def spotify_playlist_get(self,sp):
        playlists = sp.current_user_playlists()
        playlist_names = []
        for playlist in playlists['items']:
            playlist_names.append([playlist['name'],playlist['id']])
            print(playlist['name'])
            # print(playlist['id'])
        return playlist_names
        # return self.playlist_track_get(playlist_names[0][1])

    def playlist_track_get(self,sp,playlist):
        tracks = []
        result = sp.playlist_tracks(playlist)
        number_of_tracks=0
        self.playlist_id = insert_into_table('playlists',[self.user_id,None,'Spotify','Youtube Music',number_of_tracks,None])
        for track in result['items']:
            number_of_tracks = number_of_tracks + 1
            # The whole thing and the with ['track'] it only gives the data relating to the track and removes the date added and info
            # print(track)
            # print('FOLLOWING')
            # print(track['track']['name'])
            # print(track['track']['artists'])
            artists_data = track['track']['artists']
            track_id=insert_into_table('tracks',[self.playlist_id,track['track']['name'], None ,track['track']['popularity'],track['track']['explicit'],track['track']['duration_ms'],None,None,None,None])
            print(f'statusfortrackupdate:{track_id}')
            artists = []
            for artist in artists_data:
                print(artist['name'])
                artists.append(artist['name'])
                status = modify_field('tracks', artist['name'], 'artists', 'track_id',track_id)
                print(f'artistinsert:{status}')

            # print(track['track']['duration_ms'])
            # print(track['track']['explicit'])
            # print(track['track']['popularity'])
            # print('END')
            tracks.append({"name": track['track']['name'], "artists": artists,"duration_ms": track['track']['duration_ms'], "explicit": track['track']['explicit'], "popularity": track['track']['popularity']})

        # print(f"TEST{tracks[1]['name']}")
        # status = insert_into_table('playlists',[self.user_id,None,'Spotify','Youtube Music',number_of_tracks,None])

        status = modify_field('playlists',number_of_tracks,'number_of_tracks','playlist_id',self.playlist_id)
        print(f'insertdatabasestatus: {status}')
        return tracks

    def track_transfer(self, credentials, playlist_selected, tracks_given):
        try:
            self.credentials = credentials
            youtube = build("youtube", "v3", credentials=self.credentials)
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
                        'privacyStatus': 'public'
                    }
                }
            )

            playlist_new = playlist_new.execute()
            print(playlist_new)
            print('track given')
            print(tracks_given)
            failed_tracks = []
            success_score = 0
            for track in tracks_given:
                try:
                    track_id = get_from_database_keys('tracks', [track['track_title'], self.playlist_id], 'track_id',
                                                      ['track_name', 'playlist_id'])
                    print(f'trackid: {track_id}')
                    print('printing track')
                    print(track)
                    artist_line = " ".join(track['artists'])
                    track_search = f"{track['name']} {artist_line}"
                    search = youtube.search().list(
                        part='snippet',
                        q=track_search,
                        type='video',
                    )
                    video_id = search.execute()
                    stats = youtube.videos().list(
                        part='statistics,contentDetails',
                        id=video_id
                    )
                    stats = stats.execute()
                    print('testing')
                    print(video_id['items'][0]['id']['videoId'])

                    add = youtube.playlistItems().insert(
                        part='snippet',
                        body={
                            'snippet': {
                                'playlistId': playlist_new['id'],
                                'resourceId': {
                                    'kind': 'youtube#video',
                                    'videoId': video_id['items'][0]['id']['videoId']
                                }
                            }
                        }
                    )
                    add.execute()
                    # print(f'testviewcount: {stats['items'][0]['statistics']['viewCount']}')

                    status = modify_field('tracks', stats['items'][0]['statistics']['viewCount'], 'ytmusic_views', 'track_id', track_id)
                    status = modify_field('tracks', stats['items'][0]['statistics']['likeCount'], 'ytmusic_likes','track_id' , track_id)
                    status = modify_field('tracks', stats['items'][0]['contentDetails']['duration'], 'ytmusic_duration','track_id' , track_id)
                    success_score = success_score+1

                except:
                    failed_tracks.append(f'track_name: {track['name']}, artist: {track['artists']}')
            status = modify_field('playlists', success_score, 'success_score', 'playlist_id', self.playlist_id)
            # status = insert_into_table('playlists',[self.user_id, playlist_selected, None, None, None, success_score])
            return failed_tracks
        except Exception as e:
            print(f'Error on song transfer: {e}')
            return False


class YtmusicToSpotify:
    def __init__(self, user_id):
        self.user_id = user_id
        self.sp = spotify_oauth()
        self.credentials = None
        self.api_key = "AIzaSyAjAni8t-CJOEHBLwen28iDzTXDprHoOfQ"  # this will be removed later on
        # self.songs = self.song_get('PLACDKnlx5ifC65kxPaABKpB9W4Cty3Uzy')

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

    def track_get(self, playlist_id):
        try:
            api_key = "AIzaSyAjAni8t-CJOEHBLwen28iDzTXDprHoOfQ" # will be removed later
            youtube = build("youtube", "v3", developerKey=self.api_key)

            track_list = youtube.playlistItems().list(
                part = 'snippet',
                playlistId = playlist_id
            )
            track_list = track_list.execute()
            print(track_list)
            self.playlist_idget = insert_into_table('playlists',[self.user_id, playlist_id, 'Youtube Music', 'Spotify', None,None])

            tracks = []
            number_of_tracks = []
            for track in track_list['items']:
                track_id = insert_into_table('tracks', [self.playlist_idget, track['snippet']['title'], None,
                                                        None, None,
                                                        None, None, None, None,None])

                print(track)
                title = track['snippet']['title']
                video_id = track['snippet']['resourceId']['videoId']
                artist_part = track['snippet']['description'].splitlines()[2]
                print(artist_part)
                artist = []
                for word in artist_part.split(' · ')[1: ]:
                    # print(f'word: {word}')
                    status = modify_field('tracks', word, 'artists', 'track_id', track_id)
                    print(f'artistinsert:{status}')
                    artist.append(word)
                # print(artist)

                stats = youtube.videos().list(
                    part='statistics,contentDetails',
                    id = video_id
                )

                stats = stats.execute()
                # duration_ms = isodate.format_duration(f'{stats['items'][0]['contentDetails']['duration']}')
                # print(duration_ms)
                print(f'printing{stats}')
                # print(view_count)
                status = modify_field('tracks', stats['items'][0]['statistics']['viewCount'], 'ytmusic_views',
                                      'track_id', track_id)
                print(f'statsinsert:{status}')

                status = modify_field('tracks', stats['items'][0]['statistics']['likeCount'], 'ytmusic_likes',
                                      'track_id', track_id)
                print(f'statsinsert:{status}')

                status = modify_field('tracks', stats['items'][0]['contentDetails']['duration'], 'ytmusic_duration',
                                      'track_id', track_id)
                print(f'statsinsert:{status}')
                status = modify_field('tracks', 0, 'transfer_status',
                                      'track_id', track_id)
                print(f'transfer_status: {status}')


                tracks.append({'track_title': title, 'artist': artist, 'view_count': stats['items'][0]['statistics']['viewCount'], 'like_count':stats['items'][0]['statistics']['likeCount']})
            status = modify_field('playlists', number_of_tracks, 'number_of_tracks','playlist_id', self.playlist_idget)
            print(f'modifystatusno{status}')
            print(tracks)
            if not tracks:
                return None
            else:
                return tracks
        except:
            return False

    def song_transfer(self, tracks, sp):
        try:

            user = sp.current_user()
            new_playlist = sp.user_playlist_create(
                user = user["id"],
                name = 'TEST',
                public = True,
                collaborative = False,
                description = ""
            )

            print(new_playlist['id'])
            failed = []
            success_score = 0
            for track in tracks:
                track_id = get_from_database_keys('tracks', [track['track_title'],self.playlist_idget], 'track_id', ['track_name','playlist_id'])
                search_string = f"track:{track['track_title']} artist:{track['artist']}"
                result = sp.search(q=f"track:{track['track_title']} artist:{track['artist']}", type='track')
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
                    failed.append({"track":track['track_title'], "artist":track['artist']})
            status = modify_field('playlists', success_score, 'success_score', 'playlist_id', self.playlist_idget)
            print(f'success_scoreinput{status}')
            return failed
        except Exception as e:
            print(f'your error was {e}')
            return False


if __name__ == '__main__':
    from ProjectLibrary.youtubemusic_oauth import ytmusic_oauth
    # x: SpotifyToYtmusic = SpotifyToYtmusic('Visith')
    y: YtmusicToSpotify = YtmusicToSpotify('Visith')
    access_token_yt = ytmusic_oauth()
    y.playlists_get(access_token_yt)