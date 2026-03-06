# import requests
#
# CLIENT_ID = 'SizAvt1dEsOrfaoUl0jxLs3ZCFDD1wdx'
# CLIENT_SECRET = 'KRQLZfTXWkEUGXDHskX9giBuN0l6YTlr'
#
# url = 'https://api.soundcloud.com/oauth2/token'
#
# data = {
#     'client_id': CLIENT_ID,
#     'client_secret': CLIENT_SECRET,
#     'grant_type': 'client_credentials'
# }
#
# req = requests.post(url, data=data)
# token_data = req.json()
# print(token_data)
# access_token = token_data['access_token']
# print(access_token)
#
# username = 'visith-h-ilayperuma'
# url = f'https://api.soundcloud.com/users/{username}/playlists'
# headers = {'Authorization': f'OAuth {access_token}'}
#
# req = requests.get(url, headers=headers)
# print(req)
# user_playlists = req.json()
#
# if req.status_code == 200:
#     user_playlists = req.json()
#     for playlist in user_playlists:
#         print("Playlist:", playlist['title'])
#         print("Tracks:", len(playlist['tracks']))
#         for track in playlist['tracks']:
#             print("-", track['title'], "by", track['user']['username'])
#         print()

# import requests
#
# # Access token you just got
# access_token = "eyJraWQiOiJzYy13dVlRRjRjI..."  # truncated for clarity
#
# # User whose playlists you want
# username = "visith-h-ilayperuma"
#
# # API URL
# playlists_url = f"https://api.soundcloud.com/users/{username}/playlists"
#
# # Use Authorization header
# headers = {
#     "Authorization": f"OAuth {access_token}"
# }
#
# # Make the request
# response = requests.get(playlists_url, headers=headers)
#
# if response.status_code != 200:
#     print("Error fetching playlists:", response.status_code, response.text)
# else:
#     user_playlists = response.json()
#     for playlist in user_playlists:
#         print("Playlist:", playlist['title'])
#         print("Tracks:", len(playlist['tracks']))
#         for track in playlist['tracks']:
#             print("-", track['title'], "by", track['user']['username'])
#         print()
#
# import requests
#
# CLIENT_ID = "SizAvt1dEsOrfaoUl0jxLs3ZCFDD1wdx"
# CLIENT_SECRET = "KRQLZfTXWkEUGXDHskX9giBuN0l6YTlr"
# REDIRECT_URI = "http://localhost:8888/callback"
#
# # Step 1: Get authorization code
# print("Go to:")
# print(f"https://soundcloud.com/connect?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=non-expiring")
#
# # Step 2: After logging in, SoundCloud redirects to REDIRECT_URI?code=XXXX
# # Copy the code from URL
#
# AUTH_CODE = "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiQTI1NktXIn0.uejiZRyjwG0pR4-WceAbIyvA61_S70APWc3WBzhNUliM-AGe9ol_GQ.t71_Tkj-IBHpTUHfHHQjzg.3s1EP1jtHDg-Fh3hJ2w2KBy85tH0kF83Z4z2LgvO_WIbraIogapIGzjj0rJw1Nlbp3pMEufvdbfG9LjDfcTnM1CTkvLUu75LBGaX-hXT_EnoXke1kye7uw8_ypudPbiWdFNMTNrYk-TN9xq3Uekgxi-BPY_tsLR6rw0SqKSJ3GLncyYKukS3SyJwLMSf_wMd.rOxkRgJmaf9JUKcGhC_jKQ"
#
# # Step 3: Exchange code for token
# token_res = requests.post(
#     "https://api.soundcloud.com/oauth2/token",
#     data={
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "redirect_uri": REDIRECT_URI,
#         "grant_type": "authorization_code",
#         "code": AUTH_CODE
#     }
# )
# token_data = token_res.json()
# ACCESS_TOKEN = token_data["access_token"]
# print("Access token:", ACCESS_TOKEN)
#
# headers = {"Authorization": f"OAuth {ACCESS_TOKEN}"}
#
# playlist_url = "https://soundcloud.com/visith-h-ilayperuma/sets/my-playlist"
# res = requests.get(
#     "https://api.soundcloud.com/resolve",
#     params={"url": playlist_url},
#     headers=headers
# )
# res.raise_for_status()
# playlist = res.json()
# print("Playlist title:", playlist["title"])
# for t in playlist["tracks"]:
#     print(t["title"])

import requests
import re
import json

# Step 1: Grab a fresh client_id from the website (SoundCloud embeds it)
html = requests.get("https://soundcloud.com").text
match = re.search(r'"client_id":"([a-zA-Z0-9]{30,})"', html)
if not match:
    print("Couldn't find client_id — page format changed?")
    exit()
client_id = match.group(1)
print("Using client_id:", client_id)

# Step 2: Resolve the playlist URL
url = "https://soundcloud.com/visith-h-ilayperuma/sets/test"
resolve = requests.get(
    "https://api-v2.soundcloud.com/resolve",
    params={"url": url, "client_id": client_id},
    headers={"User-Agent": "Mozilla/5.0"}
)

if resolve.status_code != 200:
    print(f"Resolve failed: {resolve.status_code} - {resolve.text[:200]}")
    exit()

data = resolve.json()
print(f"Title: {data.get('title')}")
print(f"Track count reported: {data.get('track_count')}")

# Step 3: Get tracks
tracks_url = f"https://api-v2.soundcloud.com/playlists/{data['id']}/tracks?client_id={client_id}&limit=50"
tracks_resp = requests.get(tracks_url, headers={"User-Agent": "Mozilla/5.0"})

if tracks_resp.status_code == 200:
    tracks = tracks_resp.json().get("collection", [])
    print(f"\nFetched {len(tracks)} tracks:")
    for i, t in enumerate(tracks, 1):
        title = t.get("title", "N/A")
        artist = t.get("user", {}).get("username", "N/A")
        print(f"{i}. {title} – {artist}")
else:
    print(f"Tracks fetch failed: {tracks_resp.status_code}")