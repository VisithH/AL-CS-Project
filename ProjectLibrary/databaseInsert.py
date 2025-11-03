import os
import sqlite3

def insertIntoTable(tableName: str, data: list[any]) -> bool:
    dbC = sqlite3.connect("../Databases/"+tableName+".db") #projectLib
    # dbC = sqlite3.connect("Databases/"+tableName+".db") #mainApps
    try:
        qStr = "INSERT INTO " + tableName + " VALUES("
        for i in range(len(data)):
            qStr += "'" + str(data[i]) + "'"
            if i < len(data) - 1:
                qStr += ", "
        qStr += ")"
        dbC.execute(qStr)
        dbC.commit()
        dbC.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        dbC.close()
        return False

def modifyField(tableName: str, dataToInsert:str, fieldToModify:str,PrimaryKey, PrimaryKeyValue):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, '..', 'Databases', f"{tableName}.db")
        db_path = os.path.abspath(db_path)
        dbC = sqlite3.connect(db_path)
        # dbC = sqlite3.connect("../Databases/" + tableName + ".db")  # projectLib
        # dbC = sqlite3.connect("Databases/"+tableName+".db") #mainApps

        success = dbC.execute(f"UPDATE {tableName} SET {fieldToModify}=? WHERE {PrimaryKey} = ?", [dataToInsert,PrimaryKeyValue])
        print(success.rowcount)
        dbC.commit()
        dbC.close()
        if success.rowcount > 0:
            return True

    except Exception as e:
        print("Error updating the value:", e)
        return False

if __name__ == "__main__":
    # insertIntoTable('users', ['username', 'password', 'email', 'contactNo'])
    modifyField('spotifyDetails', 'Hello', 'userEmail','username','Visith')