import os
import sqlite3
def createTable(name, rowList):
    # # For Main apps
    # # db = sqlite3.connect("Databases/"+name+".db")
    #
    # # For ProjectLib Files
    # db = sqlite3.connect("../Databases/"+name+".db")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'Databases', f"{name}.db")
    db_path = os.path.abspath(db_path)
    db = sqlite3.connect(db_path)
    db.execute(f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(rowList)})")
    return True

if __name__ == '__main__':
    createTable('users',{"username": "TEXT", "password": "TEXT", "email": "TEXT", "contactNo": "TEXT"})
    # createTable("spotifyDetails", {"username": "TEXT", "userEmail": "TEXT", "accessToken": "TEXT"})

