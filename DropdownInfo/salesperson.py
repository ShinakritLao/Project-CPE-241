def get_salesperson(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT DISTINCT salespersonid FROM salesperson ORDER BY SalesPersonID;")
    result = cur.fetchall()

    salesperson = ["Sales ID"]

    for record in result:
        salesperson.append(record[0])
    return salesperson