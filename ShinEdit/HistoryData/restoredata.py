import pandas as pd
import streamlit as st
from HistoryData.changehistory_update import history_update

def get_primary(table):

    if table == 'KPI': pri = table + "_ID"
    elif table == 'Users': pri = "username"
    else: pri = table + "ID"

    return pri

def get_current_data(cur, table, loc, subloc):

    # Declare primary key for table
    pri = get_primary(table)

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT {subloc} FROM {table} WHERE {pri} = %s", (loc,))
    result = cur.fetchone()

    return result[0]

def restore_update(cur, conn, table, loc, subloc, current_value, new_value, changeid):

    # Declare primary key for table
    pri = get_primary(table)

    # Convert type to string
    new_value = str(new_value)
    loc = str(loc)

    # SQL part: Update data from the table in database
    cur.execute(f"UPDATE {table} SET {subloc} = %s WHERE {pri} = %s;", (new_value, loc))
    conn.commit()

    # Save change in history table
    history_update(cur, conn, table, changeid, subloc, "Restore", current_value, new_value)

# def restore_delete(cur, conn, table, loc, new_value):

#    # Declare primary key for table
#      pri = get_primary(table)
#
#    # SQL part: Update data from the table in database
#      cur.execute("INSERT INTO %s")

#    # Save change in history table
#      history_update(cur, conn, table, loc, "-", "Restore", "-", new_value)