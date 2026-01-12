import requests

CLIENT_ID = "SizAvt1dEsOrfaoUl0jxLs3ZCFDD1wdx"
CLIENT_SECRET = "KRQLZfTXWkEUGXDHskX9giBuN0l6YTlr"
REDIRECT_URI = "http://localhost:8888/callback"

# Step 1: Get authorization code
print("Go to:")
print(f"https://soundcloud.com/connect?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=non-expiring")

# Step 2: After logging in, SoundCloud redirects to REDIRECT_URI?code=XXXX
# Copy the code from URL

AUTH_CODE = "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiQTI1NktXIn0.ptC04a34FEG-5Nuy9KK_JmmVp6IzrFEbR9JsecPWDfTrEOa1Lv2bAA.0ZNTgjrVdx_goewkZ0oOdg.NqAUUOL5NzehkDT6NYuMapC2abPOvoaBSmDkkj-VW3EBofkgFXAP0xvK3V7I4MKJ3XzSt_cljHXKl2Yyuj1WsYhsFWViTpDd7LWd9g7dvaQxC3RZBlnYq7_nwj2s38AL83UB5D6hwaQJdit0ITkegLxybyGkNJf9H4sb4YDEIH6i-K5DkT9uTCljUUFnVJhy.3vrbSJ6qsEFtndFV1Zp6WA"

# Step 3: Exchange code for token
token_res = requests.post(
    "https://api.soundcloud.com/oauth2/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": AUTH_CODE
    }
)
token_data = token_res.json()
ACCESS_TOKEN = token_data["access_token"]
print("Access token:", ACCESS_TOKEN)

headers = {"Authorization": f"OAuth {ACCESS_TOKEN}"}

playlist_url = "https://soundcloud.com/visith-h-ilayperuma/sets/my-playlist"
res = requests.get(
    "https://api.soundcloud.com/resolve",
    params={"url": playlist_url},
    headers=headers
)
res.raise_for_status()
playlist = res.json()
print("Playlist title:", playlist["title"])
for t in playlist["tracks"]:
    print(t["title"])

