import os
import sqlite3

def insert_into_table(table_name, data): #Tom taught this in Year 1
    # db = sqlite3.connect("../Databases/music_shifter.db") #projectLib
    db = sqlite3.connect("Databases/music_shifter.db") #mainApps
    try:
        if table_name == 'users':
            db.execute(f"INSERT INTO users(username, password) VALUES(?,?)",[data[0],data[1]])
            db.commit()
            db.close()
        elif table_name == 'playlists':
            playlist = db.execute(f"INSERT INTO playlists(user_id, playlist_name, source_platform, playlist_id, destination_platform, number_of_tracks, success_score) "
                                  f"VALUES(?,?,?,?,?,?,?)",[data[0],data[1],data[2],data[3],data[4],data[5],data[6]])
            db.commit()
            db.close()
            return playlist.lastrowid
        elif table_name == 'tracks':
            track = db.execute(f"INSERT INTO tracks(playlist_id, track_name, artists, spotify_popularity, spotify_explicit, spotify_duration, ytmusic_views, ytmusic_likes, ytmusic_duration, transfer_status) "
                               f"VALUES(?,?,?,?,?,?,?,?,?,?)",[data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]])
            db.commit()
            db.close()
            return track.lastrowid
        else:
            return None
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        db.close()
        return False

def modify_field(table_name, data, field_name, filed_key, key):
    try:
        # db = sqlite3.connect("../Databases/music_shifter.db")  # projectLib
        db = sqlite3.connect("Databases/music_shifter.db") #mainApps

        success = db.execute(f"UPDATE {table_name} SET {field_name}=? WHERE {filed_key} = ?", [data, key])
        # print(success.rowcount)
        db.commit()
        db.close()
        if success.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        print("Error updating the value:", e)
        return False

if __name__ == "__main__":
    print(modify_field('users','password', 'password', 'username', 'user1'))