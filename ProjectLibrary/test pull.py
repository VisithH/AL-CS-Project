from googleapiclient.discovery import build

API_KEY = "AIzaSyAjAni8t-CJOEHBLwen28iDzTXDprHoOfQ"
PLAYLIST_ID = "PLACDKnlx5ifC65kxPaABKpB9W4Cty3Uzy"

youtube = build("youtube", "v3", developerKey=API_KEY)

def get_playlist_items(playlist_id):
    items = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            snippet = item["snippet"]

            video_id = snippet["resourceId"]["videoId"]

            items.append({
                "title": snippet["title"],
                "channel": snippet["videoOwnerChannelTitle"],
                "thumbnail": snippet["thumbnails"]["medium"]["url"],
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return items


songs = get_playlist_items(PLAYLIST_ID)

for s in songs:
    print(s["title"])
    print(s["url"])
    print(s["thumbnail"])
    print()