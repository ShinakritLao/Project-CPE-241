def get_salesperson(cursor):
    (cursor.execute
    ("""
        SELECT DISTINCT salespersonid FROM salesperson;
    """))

    result = cursor.fetchall()
    salesperson = ["Sales Name"]
    for record in result:
        salesperson.append(record[0])
    return salesperson