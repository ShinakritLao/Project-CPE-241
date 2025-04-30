def get_details(cur, table, filter):

    if filter != 'Month':
        # SQL part: Get data from the table in database
        cur.execute(f"SELECT DISTINCT {filter} FROM {table} ORDER BY {filter}")
        result = cur.fetchall()

        # Convert the result to a Series
        filterdata = []

        for record in result:
            filterdata.append(record[0])
        return filterdata
    else:
        monthdata = ["January", "February", "March", "April", "May", "June", "July",
                     "August", "September", "October", "November", "December"]
        return monthdata