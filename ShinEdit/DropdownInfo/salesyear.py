def get_salesyear(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT DISTINCT year FROM sales ORDER BY year;")
    result = cur.fetchall()

    salesyear = ["Year"]

    for record in result:
        salesyear.append(int(record[0]))
    return salesyear