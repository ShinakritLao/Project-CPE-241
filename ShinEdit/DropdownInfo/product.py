def get_product(cur):
    cur.execute("SELECT DISTINCT productid FROM product ORDER BY productid;")
    result = cur.fetchall()

    product = ["Product ID"]

    for record in result:
        product.append(record[0])
    return product