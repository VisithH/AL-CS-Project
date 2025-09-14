import sqlite3


def createTable(name, rowList):
    db = sqlite3.connect(f"./{name}.db")
    USERNAME = "username"
    db.execute(f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(rowList)})")
    return True

if __name__ == '__main__':
    createTable('users',{"username": "TEXT", "password": "TEXT", "email": "TEXT", "contactNo": "TEXT"})
