import pandas as pd
import streamlit as st

from GetData.changehistorydata import get_deletedata
from GetData.changehistorydata import get_columns
from HistoryData.changehistory_update import history_update

def get_primary(table):

    if table == 'kpi' : pri = table + "_id"
    elif table == 'users' : pri = "username"
    elif table == 'salesproduct' : pri = "salesid"
    else: pri = table + "id"

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

def restore_delete(cur, conn, table, loc):

    # Get columns name & restore data
    columns = get_columns(cur, table)
    values = get_deletedata(cur, table, loc)

    # Convert into SQL friendly
    columns_sql = ', '.join(columns)
    values_sql = ', '.join(['%s'] * len(values))

    # SQL part: Update data from the table in database
    cur.execute(f"INSERT INTO {table} ({columns_sql}) VALUES ({values_sql});", values)
    conn.commit()

    # Save change in history table
    for col, val in zip(columns, values):
        history_update(cur, conn, table, loc, col, "Restore", "-", val)

def clear_history(cur, conn):

    # SQL part: Update data from the table in database
    cur.execute(f"DELETE FROM history_change;")
    conn.commit()