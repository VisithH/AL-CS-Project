import os
import sqlite3

def get_from_database_validation(table_name, data_passed, data_requested, field):
    # # ProjectLib
    # db = sqlite3.connect(f"../Databases/{tableName}.db")
    # # mainApps
    # db = sqlite3.connect(f"Databases/{tableName}.db")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'Databases', f"{table_name}.db")
    db_path = os.path.abspath(db_path)
    db = sqlite3.connect(db_path)
    data_requested = db.execute(f"SELECT {data_requested} "
                               f"FROM {table_name} "
                               f"WHERE {field} = ?", [data_passed])
    result = data_requested.fetchone()
    db.close()
    try:
        return result[0]
    except:
        return 'None'

def get_from_database_all(table_name, data_passed, field):
    # # ProjectLib
    # db = sqlite3.connect(f"../Databases/{tableName}.db")
    # # mainApps
    # db = sqlite3.connect(f"Databases/{tableName}.db")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'Databases', f"{table_name}.db")
    db_path = os.path.abspath(db_path)
    db = sqlite3.connect(db_path)
    data_requested = db.execute(f"SELECT * "
                               f"FROM {table_name} "
                               f"WHERE {field} = ?", [data_passed])
    result = data_requested.fetchone()
    db.close()
    try:
        return result
    except:
        return 'None'


get_from_database_all('youtubemusic_token', 'Visith', 'username')