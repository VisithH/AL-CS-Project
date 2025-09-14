import ProjectLibrary.databaseGenerator as databaseGenerator
import ProjectLibrary.databaseInsert as databaseInsert
from spotipy.oauth2 import SpotifyOAuth

def spotifyOauth(username,email):
    databaseGenerator.createTable("spotifyDetails", {"username": "TEXT", "userEmail": "TEXT", "accessToken": "TEXT"})

    # Define your credentials and scope

    spotify_oauth = SpotifyOAuth(
        client_id="4f8f7fd752074a3fa583f0fadccdbaf8",
        client_secret="df3f113d04804f4bb27247fa92b307ae",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-private user-read-email",
        # cache_path=f".cache-{username}" #uncomment this!!
        cache_path="None", #RemoveLater!!!!
    )

    tokenInfo = spotify_oauth.get_access_token(as_dict=False)
    accessToken = tokenInfo
    print("Access Token:", accessToken)

    # insertData('user', 'user@gmail.com', accessToken)
    databaseInsert.insertIntoTable('spotifyDetails', [username, email, accessToken])
    return accessToken
