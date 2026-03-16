import sqlite3

def get_from_database(table_name, data_passed, data_requested, data_passed_field):
    try:
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
        except Exception as e:
            print(f'Error retrieving data: {e}')
            return 'None'
    except Exception as e:
        print(f'Error retrieving data: {e}')
        return False


def get_from_database_keys(table_name, data_passed, data_requested, field):
    try:
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
        except Exception as e:
            print(f'Error from retrieving data: {e}')
            return 'None'
    except Exception as e:
        print(f'Error from retrieving data: {e}')
        return False

def get_from_database_all(table_name, data_passed, field):
    try:
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
        except Exception as e:
            print(f'Error from retrieving data: {e}')
            return 'None'
    except Exception as e:
        print(f'Error from retrieving data: {e}')
        return False

def get_from_database_everyrow(table_name,data_name,data_id,field,data_passed):
    try:
        # # ProjectLib
        # db = sqlite3.connect("../Databases/music_shifter.db")
        # # mainApps
        db = sqlite3.connect("Databases/music_shifter.db")

        data_requested = db.execute(f"SELECT {data_name},{data_id} "
                                    f"FROM {table_name} "
                                    f"WHERE {field} = ?", [data_passed])
        result = data_requested.fetchall()
        db.close()
        try:
            return result
        except Exception as e:
            print(f'coudnt get all the data: {e}')
            return 'None'
    except Exception as e:
        print(f'coudnt get all the data: {e}')
        return False

if __name__ == '__main__':
    # print(get_from_database_all('user','user1','username'))
    print(get_from_database_everyrow('playlists','playlist_name','playlist_id','source_platform','spotify'))