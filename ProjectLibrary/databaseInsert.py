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

if __name__ == "__main__":
    insertIntoTable('users', ['username', 'password', 'email', 'contactNo'])
