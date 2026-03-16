import sqlite3

def create_user_table():
    db = sqlite3.connect("Databases/music_shifter.db")
    # db = sqlite3.connect("../Databases/music_shifter.db")
    db.execute("CREATE TABLE IF NOT EXISTS users("
               "user_id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "username TEXT UNIQUE NOT NULL, "
               "password TEXT NOT NULL)")

    db.commit()
    db.close()

create_user_table()

def create_playlists_table():
    db = sqlite3.connect("Databases/music_shifter.db")
    # db = sqlite3.connect("../Databases/music_shifter.db")
    db.execute("CREATE TABLE IF NOT EXISTS playlists("
               "playlist_id TEXT PRIMARY KEY UNIQUE NOT NULL, "
               "user_id INTEGER NOT NULL, " #Linked w user table
               "playlist_name TEXT NOT NULL, "
               "source_platform TEXT, "
               "destination_platform TEXT, "
               "number_of_tracks INTEGER, "
               "success_score INTEGER, "
               "FOREIGN KEY(user_id) REFERENCES users(user_id))")

    db.commit()
    db.close()

create_playlists_table()

def create_tracks_table():
    db = sqlite3.connect("Databases/music_shifter.db")
    # db = sqlite3.connect("../Databases/music_shifter.db")
    db.execute("CREATE TABLE IF NOT EXISTS tracks("
               "track_id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "playlist_id INTEGER NOT NULL, " #Linked w user table
               "track_name TEXT NOT NULL, "
               "artists TEXT, "
               "spotify_popularity INTEGER, "
               "spotify_explicit INTEGER, "
               "spotify_duration INTEGER, "
               "ytmusic_views INTEGER, "
               "ytmusic_likes INTEGER, "
               "ytmusic_duration INTEGER, "
               "transfer_status INTEGER, "
               "FOREIGN KEY(playlist_id) REFERENCES playlists(playlist_id) ON DELETE CASCADE)")

    db.commit()
    db.close()

create_tracks_table()