import sqlite3


def getFromDatabaseValidation(tableName, data, field):
    db = sqlite3.connect(f"./{tableName}.db")
    data = db.execute(f"SELECT * "
                        f"FROM {tableName} "
                        f"WHERE {field} = ?", [data])
    result = data.fetchone()
    db.close()
    return result[0]

# getFromDatabaseValidation("users", "42f749ade7f9e195bf475f37a44cafcb", "password")

