from MS_Main import YtmusicToSpotify


def bubble_graph_return(songs_given):
    import matplotlib.pyplot as plt
    # track_data = songs_given
    #
    # tracks = []
    # for i in range(len(track_data) - 1):
    #     print(i)
    #     i = i + 1
    #     tracks.append({'name': track_data[i]['name'], 'popularity': track_data[i]['popularity'],
    #                    'duration_ms': track_data[i]['duration_ms']})

    # Extract data for plotting
    names = [t['track_title'] for t in songs_given]
    x = [t['view_count'] for t in songs_given]  # x-axis: popularity
    y = [t['like_count'] / 1000 for t in songs_given]  # y-axis: duration in seconds
    sizes = [t['view_count'] * 2 for t in songs_given]  # bubble size (scale up for visibility)

    plt.figure(figsize=(10, 8))
    plt.scatter(x, y, s=sizes, alpha=0.6)

    # Label each bubble with the track name
    for i, name in enumerate(names):
        plt.text(x[i], y[i] + 2, name, ha='center', fontsize=9)

    plt.xlabel('view_count')
    plt.ylabel('like_count (s)')
    plt.title('Spotify Playlist Tracks Bubble Chart')
    plt.show()
    plt.tight_layout()
    plt.savefig("bubble_chart.png", dpi=300)
    plt.close()

y: YtmusicToSpotify = YtmusicToSpotify('Visith')
songs_given = y.track_get('PLACDKnlx5ifC65kxPaABKpB9W4Cty3Uzy')
bubble_graph_return(songs_given)