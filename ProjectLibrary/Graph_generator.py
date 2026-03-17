import sqlite3
import matplotlib.pyplot as plot


def graph_artist_analysis(data):
    print(data)
    artist_data = {}
    for row in data:
        print(row)
        artist = row[0]
        popularity = row[1]
        views = row[2]

        if artist not in artist_data:
            artist_data[artist] = {"tracks": 0, "popularity": 0, "views": 0}

        artist_data[artist]["tracks"] += 1
        artist_data[artist]["popularity"] += popularity
        artist_data[artist]["views"] += int(views)

    artists = []
    track_counts = []
    avg_popularity = []
    bubble_sizes = []

    for artist in artist_data:
        print(artist)
        tracks = artist_data[artist]["tracks"]
        mean_population = artist_data[artist]["popularity"] / tracks
        views = artist_data[artist]["views"]

        artists.append(artist)
        track_counts.append(tracks)
        avg_popularity.append(mean_population)
        bubble_sizes.append(views / 500000)

    plot.scatter(track_counts, avg_popularity, s=bubble_sizes)

    plot.xlabel("Number of Tracks")
    plot.ylabel("Average Spotify Popularity")
    plot.title("Artist Popularity")

    for i in range(len(artists)):
        plot.text(track_counts[i], avg_popularity[i], artists[i], fontsize=8)

    plot.savefig("ProjectLibrary/Graphs/graph.png")
    plot.show()

    plot.close()