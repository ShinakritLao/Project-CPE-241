def createuser(cursor, conn):

    cursor.execute("""INSERT INTO users (username, password, name, lastname, position, phonenumber) VALUES 
                   (%s %s %s %s %s %s)""", new_username, new_password, new_name, new_lastname, new_position, new_phone)
    conn.commit()

def modifyuser(cursor, conn):

    cursor.execute("UPDATE users SET %s = %s WHERE username = %s;", change_column, new_data, username)
    conn.commit()