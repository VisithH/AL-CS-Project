import databaseGenerator
import databaseInsert
from spotipy.oauth2 import SpotifyOAuth

databaseGenerator.createTable("spotifyDetails", {"username": "TEXT", "userEmail": "TEXT", "accessToken": "TEXT"})

# Define your credentials and scope

spotify_oauth = SpotifyOAuth(
    client_id="a0467560a9c34ade9e6f1552ba363297",
    client_secret="c1f77d193bf748d2bb26b5d7955bed54",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-private user-read-email"
)

tokenInfo = spotify_oauth.get_access_token(as_dict=False)
accessToken = tokenInfo
print("Access Token:", accessToken)


print("Access Token:", accessToken)
# insertData('user', 'user@gmail.com', accessToken)
databaseInsert.insertIntoTable('spotifyDetails', ['user', 'user@gmail.com', accessToken])
