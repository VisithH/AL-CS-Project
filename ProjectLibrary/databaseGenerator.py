import sqlite3

def create_user_table():
    db = sqlite3.connect("Databases/users.db")
    # db = sqlite3.connect("../Databases/users.db")
    db.execute("CREATE TABLE IF NOT EXISTS users ("
               "username TEXT UNIQUE,"
               "password TEXT)")

    db.commit()
    db.close()

# create_user_table()

def create_access_spotify_token_table():
    db = sqlite3.connect("Databases/spotify_token.db")
    # db = sqlite3.connect("../Databases/spotify_tokens.db")
    db.execute("CREATE TABLE IF NOT EXISTS spotify_token ("
               "username TEXT UNIQUE, " #Linked w user table
               "token TEXT, "
               "FOREIGN KEY(username) REFERENCES users(username))")

    db.commit()
    db.close()

# create_access_spotify_token_table()

def create_access_youtubemusic_token_table():
    db = sqlite3.connect("Databases/spotify_token.db")
    # db = sqlite3.connect("../Databases/youtubemusic_token.db")
    db.execute("CREATE TABLE IF NOT EXISTS youtubemusic_token ("
               "username TEXT UNIQUE, " #Linked w user table
               "access_token TEXT, "
               "refresh_token TEXT, "
               "token_uri TEXT, "
               "client_id TEXT, "
               "client_secret TEXT, "
               "scopes TEXT, "
               "expiry TEXT, "
               "FOREIGN KEY(username) REFERENCES users(username))")

    db.commit()
    db.close()

create_access_youtubemusic_token_table()