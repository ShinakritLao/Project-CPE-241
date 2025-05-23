import pandas as pd

def get_salesproductdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM SalesProduct ORDER BY SalesID, ProductID ASC;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    salesproduct = pd.DataFrame(result, columns = ['SalesID', 'ProductID', 'TotalSales', 'TotalCost', 'Status'])

    # Convert into integer type
    salesproduct['TotalSales'] = salesproduct['TotalSales'].astype(int)
    salesproduct['TotalCost'] = salesproduct['TotalCost'].astype(int)

    return salesproduct

def get_display_salesproduct(cur):

    # SQL part: Get data from the table in database
    cur.execute("""
            SELECT SalesID, Product.ProductID, ProductName, TotalSales, TotalCost, SalesProduct.Status FROM SalesProduct
            JOIN Product ON SalesProduct.ProductID = Product.ProductID ORDER BY SalesID, Product.ProductID ASC;
            """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Sales ID', 'Product ID', 'Product Name', 'Total Sales',
                                                        'Total Cost', 'Status'])

    return display_data

def get_one_salesproductdata(cur, loc, subloc, loc2, subloc2):

    # SQL part: Get data from the table in database
    cur.execute(f"""
                SELECT SalesID, Product.ProductID, ProductName, TotalSales, TotalCost, SalesProduct.Status FROM SalesProduct
                JOIN Product ON SalesProduct.ProductID = Product.ProductID WHERE SalesProduct.{loc} = '{subloc}' 
                AND SalesProduct.{loc2} = '{subloc2}' ORDER BY SalesID, Product.ProductID ASC;
                """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Sales ID', 'Product ID', 'Product Name', 'Total Sales',
                                                        'Total Cost', 'Status'])

    return display_data