import streamlit as st
from HistoryData.changehistory_update import history_update
from HistoryData.restoredata import get_primary

def updatedata(cur, conn, table, loc, subloc, original_data, new_value):

    # Set primary key of the table
    pri = get_primary(table)

    # SQL part: Update new value
    if table != 'salesproduct':
        cur.execute(f"UPDATE {table} SET {subloc} = %s WHERE {pri} = '{loc}'", (new_value,))
    else:
        cur.execute(f"UPDATE SalesProduct SET {subloc} = %s WHERE SalesID = '{loc[0]}' AND ProductID = '{loc[1]}'", (new_value,))
    conn.commit()

    # Update history
    history_update(cur, conn, table, loc, subloc, 'Update', original_data, new_value)

def checkban(cur, conn):
    cur.execute("SELECT Status FROM Users WHERE Username = %s", (st.session_state.username,))
    result = cur.fetchone()

    if result[0] == 'Banned':
        st.warning("You have been banned. Logging out...")
        history_update(cur, conn, "users", st.session_state.username, "status", "Logout", "Active", "Banned")
        del st.session_state.username
        st.session_state.logged_in = False
        st.rerun()