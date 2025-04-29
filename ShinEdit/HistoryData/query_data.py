from HistoryData.changehistory_update import history_update

def updatedata(cur, conn, table, loc, subloc, original_data, new_value):

    # Set primary key of the table
    pri = table + 'ID'

    # SQL part: Update new value
    cur.execute(f"UPDATE {table} SET {subloc} = %s WHERE {pri} = '{loc}'", (new_value,))
    conn.commit()

    # Update history
    history_update(cur, conn, table, loc, subloc, 'Update', original_data, new_value)