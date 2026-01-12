def bubble_graph_return():
    import matplotlib.pyplot as plt
    from MS_Main import spotify_to_soundcloud

    x: spotify_to_soundcloud = spotify_to_soundcloud('Visith')
    playlist_name = x.spotify_playlist_get()
    track_data = x.playlist_track_get(playlist_name[0][1])

    tracks = []
    for i in range(len(track_data) - 1):
        print(i)
        i = i + 1
        tracks.append({'name': track_data[i]['name'], 'popularity': track_data[i]['popularity'],
                       'duration_ms': track_data[i]['duration_ms']})

    # Extract data for plotting
    names = [t['name'] for t in tracks]
    x = [t['popularity'] for t in tracks]  # x-axis: popularity
    y = [t['duration_ms'] / 1000 for t in tracks]  # y-axis: duration in seconds
    sizes = [t['popularity'] * 2 for t in tracks]  # bubble size (scale up for visibility)

    plt.figure(figsize=(10, 8))
    plt.scatter(x, y, s=sizes, alpha=0.6)

    # Label each bubble with the track name
    for i, name in enumerate(names):
        plt.text(x[i], y[i] + 2, name, ha='center', fontsize=9)

    plt.xlabel('Popularity')
    plt.ylabel('Duration (s)')
    plt.title('Spotify Playlist Tracks Bubble Chart')
    plt.show()
    plt.tight_layout()
    plt.savefig("bubble_chart.png", dpi=300)
    plt.close()