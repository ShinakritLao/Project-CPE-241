def get_salesperson(cursor):
    (cursor.execute
    ("""
        sql
    """))

    result = cursor.fetchall()
    salesperson = ["Sales Name"]
    for record in result:
        salesperson.append(record[0])
    return salesperson