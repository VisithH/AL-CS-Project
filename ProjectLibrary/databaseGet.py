import sqlite3


def getFromDatabaseValidation(tableName, dataPassed,dataRequested, field):
    db = sqlite3.connect(f"./{tableName}.db")
    dataRequested = db.execute(f"SELECT {dataRequested} "
                        f"FROM {tableName} "
                        f"WHERE {field} = ?", [dataPassed])
    result = dataRequested.fetchone()
    db.close()
    try:
        return result[0]
    except:
        return 'None'

# getFromDatabaseValidation("users", "42f749ade7f9e195bf475f37a44cafcb", "password")

