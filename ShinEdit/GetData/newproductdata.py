import pandas as pd

def get_newproductdata(cur):
    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Product ORDER BY ProductID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    productdata = pd.DataFrame(result, columns=['ProductID', 'ProductName', 'InStock', 'Status', 'ImportLoc'])

    return productdata


def get_one_newproductdata(cur, loc, subloc):
    # Execute the filtered SQL query
    cur.execute(f"""
        SELECT ProductID, ProductName, InStock, Status, ImportLoc
        FROM Product
        WHERE {loc} = %s
        ORDER BY ProductID;
    """, (subloc,))

    # Fetch the results and convert to DataFrame
    display_sql = cur.fetchall()
    display_data = pd.DataFrame(display_sql, columns=['ProductID', 'ProductName', 'InStock', 'Status', 'ImportLoc'])

    return display_data


def get_display_newproduct(cur):
    # SQL part: Get data from the table in database
    cur.execute("""
        SELECT ProductID, ProductName, InStock, Status, ImportLoc
        FROM Product
        ORDER BY ProductID;
    """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns=['Product ID', 'Product Name', 'In Stock', 'Status', 'Import Location'])

    return display_data
