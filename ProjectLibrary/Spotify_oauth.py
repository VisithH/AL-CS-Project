import spotipy
from spotipy import Spotify

import ProjectLibrary.databaseGenerator as databaseGenerator
import ProjectLibrary.databaseInsert as databaseInsert
from spotipy.oauth2 import SpotifyOAuth
from ProjectLibrary.databaseGet import getFromDatabaseValidation

def spotify_oauth(username,email):
    databaseGenerator.createTable("spotifyDetails", {"username": "TEXT", "userEmail": "TEXT", "accessToken": "TEXT"})

    # Define your credentials and scope

    auth_manager = SpotifyOAuth(
        client_id="4f8f7fd752074a3fa583f0fadccdbaf8",
        client_secret="df3f113d04804f4bb27247fa92b307ae",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-library-read playlist-read-private  ",
        cache_path=f".cache-{username}" #uncomment this!!
    )

    token_info = auth_manager.get_cached_token()

    if not token_info:
        print("No Cache Token found. Get Cache token")
        token_info = auth_manager.get_access_token(as_dict=True)
        print("Token Retrieved")
        if not token_info:
            print("Failed to get the Access Token")
            raise Exception("Failed to get the Access Token")

    # Extract token
    accessToken = token_info["access_token"]
    print("Access Token:", accessToken)

    # insertData('user', 'user@gmail.com', accessToken)
    user_exist = getFromDatabaseValidation('spotifyDetails',username,'username','username')
    if user_exist != 'None':
        databaseInsert.modifyField('spotifyDetails',accessToken,'accessToken','username',username)
        return accessToken
    else:
        databaseInsert.insertIntoTable('spotifyDetails', [username, email, accessToken])
        return accessToken


if __name__ == '__main__':
    print(spotify_oauth('Visith','Visith@gmail.com'))
