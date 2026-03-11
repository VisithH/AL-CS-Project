import os
import sqlite3

def insert_into_table(table_name, data):
    # db = sqlite3.connect("../Databases/" + table_name + ".db") #projectLib
    db = sqlite3.connect("Databases/"+table_name+".db") #mainApps
    try:
        qStr = "INSERT INTO " + table_name + " VALUES("
        for i in range(len(data)):
            qStr += "'" + str(data[i]) + "'"
            if i < len(data) - 1:
                qStr += ", "
        qStr += ")"
        db.execute(qStr)
        db.commit()
        db.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        db.close()
        return False

def modify_field(table_name, data_to_insert, field_to_modify, data, data_inthere):
    try:
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # db_path = os.path.join(base_dir, '..', 'Databases', f"{table_name}.db")
        # db_path = os.path.abspath(db_path)
        # db = sqlite3.connect(db_path)
        # db = sqlite3.connect("../Databases/" + tableName + ".db")  # projectLib
        db = sqlite3.connect("Databases/"+table_name+".db") #mainApps

        success = db.execute(f"UPDATE {table_name} SET {field_to_modify}=? WHERE {data} = ?", [data_to_insert, data_inthere])
        print(success.rowcount)
        db.commit()
        db.close()
        if success.rowcount > 0:
            return True

    except Exception as e:
        print("Error updating the value:", e)
        return False

if __name__ == "__main__":
    # insertIntoTable('users', ['username', 'password', 'email', 'contactNo'])
    # modifyField('spotifyDetails', 'Hello', 'userEmail','username','Visith')
    insert_into_table('users', ['visith', 'Visith@1233'])