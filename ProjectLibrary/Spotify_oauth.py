import spotipy
from spotipy.oauth2 import SpotifyOAuth

def spotify_oauth():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="4f8f7fd752074a3fa583f0fadccdbaf8",
                                                   client_secret="df3f113d04804f4bb27247fa92b307ae",
                                                   redirect_uri="http://127.0.0.1:8888/callback",
                                                   scope="playlist-modify-private playlist-modify-public user-library-read playlist-read-private"))
    return sp

if __name__ == '__main__':
    # print(spotify_oauth('Visith'))
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_APP_CLIENT_ID",
                                                   client_secret="YOUR_APP_CLIENT_SECRET",
                                                   redirect_uri="YOUR_APP_REDIRECT_URI",
                                                   scope="user-library-read"))
    print(sp)
