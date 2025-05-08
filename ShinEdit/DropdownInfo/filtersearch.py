def get_details(cur, table, filter):

    if filter == 'Position':
        positiondata = ['Chief', 'Manager', 'Representative']
        return positiondata

    elif filter == 'Month':
        monthdata = ["January", "February", "March", "April", "May", "June", "July",
                     "August", "September", "October", "November", "December"]
        return monthdata
    else:
        # SQL part: Get data from the table in database
        cur.execute(f"SELECT DISTINCT {filter} FROM {table} ORDER BY {filter}")
        result = cur.fetchall()

        # Convert the result to a Series
        filterdata = []

        for record in result:
            filterdata.append(record[0])
        return filterdata

def get_restore(cur):

    # SQL part: Get data from the table in database
    cur.execute("""
            SELECT ChangeID FROM history_change WHERE (Action = 'Update' AND SubLocation != 'password') OR 
            (Action = 'Delete' AND Location = Original_Data AND Selected_Table != 'Users') ORDER BY ChangeID;
            """)
    result = cur.fetchall()

    # Convert the result to a Series
    filterdata = []

    for record in result:
        filterdata.append(record[0])
    return filterdata