import sqlite3
from datetime import datetime

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    spotify_id TEXT,
    soundcloud_id TEXT
)
''')

# Tokens table
c.execute('''
CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    provider TEXT,
    access_token TEXT,
    refresh_token TEXT,
    expires_at DATETIME,
    scopes TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()


import sqlite3
from datetime import datetime

def add_user(username, email=None, spotify_id=None, soundcloud_id=None):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO users (username, email, spotify_id, soundcloud_id)
        VALUES (?, ?, ?, ?)
    ''', (
        username,
        email,
        spotify_id,
        soundcloud_id
    ))

    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

user_id = add_user("visith", "visith@example.com", spotify_id="123spotify", soundcloud_id="456sc")
print("New user ID:", user_id)
