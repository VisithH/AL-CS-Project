import sqlite3

def get_from_database(table_name, data_passed, data_requested, data_passed_field):
    # # ProjectLib
    # db = sqlite3.connect("../Databases/music_shifter.db")
    # # mainApps
    db = sqlite3.connect("Databases/music_shifter.db")

    data_requested = db.execute(f"SELECT {data_requested} "
                               f"FROM {table_name} "
                               f"WHERE {data_passed_field} = ?", [data_passed])
    result = data_requested.fetchone()
    db.close()
    try:
        return result[0]
    except:
        return 'None'


def get_from_database_keys(table_name, data_passed, data_requested, field):
    # # ProjectLib
    # db = sqlite3.connect("../Databases/music_shifter.db")
    # # mainApps
    db = sqlite3.connect("Databases/music_shifter.db")

    data_requested = db.execute(f"SELECT {data_requested} "
                               f"FROM {table_name} "
                               f"WHERE {field[0]} = ? AND {field[1]} = ?", [data_passed[0],data_passed[1]])
    result = data_requested.fetchone()
    db.close()
    try:
        return result[0]
    except:
        return 'None'

def get_from_database_all(table_name, data_passed, field):
    # # ProjectLib
    # db = sqlite3.connect("../Databases/music_shifter.db")
    # # mainApps
    db = sqlite3.connect("Databases/music_shifter.db")

    data_requested = db.execute(f"SELECT * "
                               f"FROM {table_name} "
                               f"WHERE {field} = ?", [data_passed])
    result = data_requested.fetchone()
    db.close()
    try:
        return result
    except:
        return 'None'
