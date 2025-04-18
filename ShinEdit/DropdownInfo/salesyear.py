def get_salesyear(cursor):
    (cursor.execute
     ("""
        SELECT year FROM sales;
     """))

    result = cursor.fetchall()
    salesyear = ["Years"]
    for record in result:
        salesyear.append(int(record[0]))
    return salesyear