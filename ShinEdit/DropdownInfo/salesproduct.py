def get_salesproduct_pd(cur, loc):
    cur.execute("SELECT DISTINCT productid FROM salesproduct WHERE salesid = %s ORDER BY productid;" , (loc,))
    result = cur.fetchall()

    product = ["Product ID"]

    for record in result:
        product.append(record[0])
    return product

def get_salesproduct_s(cur):
    cur.execute("SELECT DISTINCT salesid FROM salesproduct ORDER BY salesid;")
    result = cur.fetchall()

    product = ["Sales ID"]

    for record in result:
        product.append(record[0])
    return product