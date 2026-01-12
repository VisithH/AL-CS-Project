import spotipy
from spotipy import Spotify

import ProjectLibrary.databaseInsert as databaseInsert
from spotipy.oauth2 import SpotifyOAuth
from ProjectLibrary.databaseGet import get_from_database_validation

def spotify_oauth():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="4f8f7fd752074a3fa583f0fadccdbaf8",
                                                   client_secret="df3f113d04804f4bb27247fa92b307ae",
                                                   redirect_uri="http://127.0.0.1:8888/callback",
                                                   scope="playlist-modify-private playlist-modify-public user-library-read playlist-read-private"))
    return sp

# def spotify_oauth(username):
#
#     auth_manager = SpotifyOAuth(
#         client_id="4f8f7fd752074a3fa583f0fadccdbaf8",
#         client_secret="df3f113d04804f4bb27247fa92b307ae",
#         redirect_uri="http://127.0.0.1:8888/callback",
#         scope="playlist-modify-private playlist-modify-public user-library-read playlist-read-private",
#         cache_path=f".cache-{username}" #uncomment this!!
#     )
#
#     token_info = auth_manager.get_cached_token()
#
#     if not token_info:
#         print("No Cache Token found. Get Cache token")
#         token_info = auth_manager.get_access_token(as_dict=True)
#         print("Token Retrieved")
#         if not token_info:
#             print("Failed to get the Access Token")
#             raise Exception("Failed to get the Access Token")
#
#     # Extract token
#     accessToken = token_info["access_token"]
#     print("Access Token:", accessToken)
#
#     # insertData('user', 'user@gmail.com', accessToken)
#     user_exist = get_from_database_validation('tokens', username, 'username', 'username')
#     if user_exist != 'None':
#         databaseInsert.modify_field('tokens', accessToken, 'spotify_token', 'username', username)
#         return accessToken
#     else:
#         databaseInsert.insert_into_table('tokens', [username, accessToken, None])
#         return accessToken


if __name__ == '__main__':
    # print(spotify_oauth('Visith'))
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_APP_CLIENT_ID",
                                                   client_secret="YOUR_APP_CLIENT_SECRET",
                                                   redirect_uri="YOUR_APP_REDIRECT_URI",
                                                   scope="user-library-read"))
    print(sp)
