import sqlite3

def getFromDatabaseValidation(tableName, dataPassed, dataRequested, field):
    # ProjectLib
    db = sqlite3.connect(f"../Databases/{tableName}.db")
    # mainApps
    # db = sqlite3.connect(f"Databases/{tableName}.db")
    dataRequested = db.execute(f"SELECT {dataRequested} "
                               f"FROM {tableName} "
                               f"WHERE {field} = ?", [dataPassed])
    result = dataRequested.fetchone()
    db.close()
    try:
        return result[0]
    except:
        return 'None'

