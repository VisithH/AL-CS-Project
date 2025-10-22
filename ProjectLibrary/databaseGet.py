import os
import sqlite3

def getFromDatabaseValidation(tableName, dataPassed, dataRequested, field):
    # # ProjectLib
    # db = sqlite3.connect(f"../Databases/{tableName}.db")
    # # mainApps
    # # db = sqlite3.connect(f"Databases/{tableName}.db")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'Databases', f"{tableName}.db")
    db_path = os.path.abspath(db_path)
    db = sqlite3.connect(db_path)
    dataRequested = db.execute(f"SELECT {dataRequested} "
                               f"FROM {tableName} "
                               f"WHERE {field} = ?", [dataPassed])
    result = dataRequested.fetchone()
    db.close()
    try:
        return result[0]
    except:
        return 'None'

