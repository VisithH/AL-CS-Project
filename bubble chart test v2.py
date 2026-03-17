import sqlite3
import matplotlib.pyplot as plt

from ProjectLibrary.databaseGet import get_from_database_everyrow, get_from_database_everyrow_3


def graph_spotify_vs_yt_likes():

    conn = sqlite3.connect("Databases/music_shifter.db")
    cursor = conn.cursor()

    cursor.execute("SELECT spotify_popularity, ytmusic_likes FROM tracks")
    data = cursor.fetchall()

    conn.close()

    spotify = []
    yt_likes = []
    bubble_size = []

    for row in data:
        if row[0] != None and row[1] != None:
            spotify.append(row[0])
            yt_likes.append(int(row[1]))
            bubble_size.append(int(row[1]) / 1000)

    plt.scatter(spotify, yt_likes, s=bubble_size)

    plt.xlabel("Spotify Popularity")
    plt.ylabel("YouTube Music Likes")
    plt.title("Spotify Popularity vs YouTube Music Likes")

    plt.show()

# graph_spotify_vs_yt_likes()

import sqlite3
import matplotlib.pyplot as plt

def graph_spotify_vs_yt_views():

    conn = sqlite3.connect("Databases/music_shifter.db")
    cursor = conn.cursor()

    cursor.execute("SELECT track_name, spotify_popularity, ytmusic_views FROM tracks")
    data = cursor.fetchall()

    conn.close()

    spotify = []
    yt_views = []
    bubble_size = []
    track_names = []

    for row in data:
        name = row[0]
        popularity = row[1]
        views = row[2]

        if popularity != None and views != None:
            spotify.append(popularity)
            yt_views.append(int(views))
            bubble_size.append(int(views) / 100000)  # controls bubble size
            track_names.append(name)

    plt.scatter(spotify, yt_views, s=bubble_size)

    plt.xlabel("Spotify Popularity")
    plt.ylabel("YouTube Music Views")
    plt.title("Spotify Popularity vs YouTube Music Views")

    # add track names next to each point
    for i in range(len(track_names)):
        plt.text(spotify[i], yt_views[i], track_names[i], fontsize=8)

    plt.show()
# graph_spotify_vs_yt_views()

import sqlite3
import matplotlib.pyplot as plt

def graph_artist_analysis():
    data = get_from_database_everyrow_3('tracks','artists','spotify_popularity','ytmusic_views')

    artist_data = {}

    for row in data:
        artist = row[0]
        popularity = row[1]
        views = row[2]

        if artist not in artist_data:
            artist_data[artist] = {"tracks":0, "popularity":0, "views":0}

        artist_data[artist]["tracks"] += 1
        artist_data[artist]["popularity"] += popularity
        artist_data[artist]["views"] += int(views)

    artists = []
    track_counts = []
    avg_popularity = []
    bubble_sizes = []

    for artist in artist_data:

        tracks = artist_data[artist]["tracks"]
        avg_pop = artist_data[artist]["popularity"] / tracks
        views = artist_data[artist]["views"]

        artists.append(artist)
        track_counts.append(tracks)
        avg_popularity.append(avg_pop)
        bubble_sizes.append(views / 5000000)

    plt.scatter(track_counts, avg_popularity, s=bubble_sizes)

    plt.xlabel("Number of Tracks")
    plt.ylabel("Average Spotify Popularity")
    plt.title("Artist Popularity")

    for i in range(len(artists)):
        plt.text(track_counts[i], avg_popularity[i], artists[i], fontsize=8)

    plt.show()
graph_artist_analysis()