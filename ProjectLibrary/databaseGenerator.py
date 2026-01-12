import sqlite3

def create_user_table():
    db = sqlite3.connect("Databases/users.db")
    # db = sqlite3.connect("../Databases/users.db")
    db.execute("CREATE TABLE IF NOT EXISTS users ("
               "username TEXT UNIQUE,"
               "password TEXT)")

    db.commit()
    db.close()

create_user_table()

def create_access_token_table():
    db = sqlite3.connect("Databases/tokens.db")
    # db = sqlite3.connect("../Databases/tokens.db")
    db.execute("CREATE TABLE IF NOT EXISTS tokens ("
               "username TEXT UNIQUE, " #Linked w user table
               "spotify_token TEXT, "
               "soundcloud_token TEXT, "
               "FOREIGN KEY(username) REFERENCES users(username))")

    db.commit()
    db.close()

create_access_token_table()