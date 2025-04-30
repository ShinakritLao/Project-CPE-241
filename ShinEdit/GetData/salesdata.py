import pandas as pd

def get_salesdata_dash(cur, salesperson, salesyear):

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT * FROM Sales WHERE salespersonid = '{salesperson}' AND year = {salesyear};")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    salesdata = pd.DataFrame(result, columns = ['SalesID', 'SalesPersonID', 'Quantity', 'Year', 'Month', 'Sales'])

    # Convert into integer type
    salesdata['Quantity'] = salesdata['Quantity'].astype(int)
    salesdata['Year'] = salesdata['Year'].astype(int)
    salesdata['Sales'] = salesdata['Sales'].astype(int)

    return salesdata

def get_salesdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Sales ORDER BY SalesID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    salesdata = pd.DataFrame(result, columns = ['SalesID', 'SalesPersonID', 'Quantity', 'Year', 'Month', 'Sales'])

    # Convert into integer type
    salesdata['Quantity'] = salesdata['Quantity'].astype(int)
    salesdata['Year'] = salesdata['Year'].astype(int)
    salesdata['Sales'] = salesdata['Sales'].astype(int)

    return salesdata

def get_display_sales(cur):

    # SQL part: Get data from the table in database
    cur.execute("""
            SELECT SalesID, Sales.SalesPersonID, SalesName, Quantity, Year, Month, Sales FROM Sales
            JOIN SalesPerson ON Sales.SalesPersonID = SalesPerson.SalesPersonID ORDER BY SalesID;
            """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Sales ID', 'Sales Person ID', 'Sales Name', 'Quantity',
                                                      'Year', 'Month', 'Sales'])

    return display_data

def get_one_salesdata(cur, loc, subloc):

    # SQL part: Get data from the table in database
    cur.execute(f"""
                SELECT SalesID, Sales.SalesPersonID, SalesName, Quantity, Year, Month, Sales FROM Sales
                JOIN SalesPerson ON Sales.SalesPersonID = SalesPerson.SalesPersonID WHERE Sales.{loc} = '{subloc}' 
                ORDER BY SalesID;
                """, (subloc,))
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Sales ID', 'Sales Person ID', 'Sales Name', 'Quantity',
                                                      'Year', 'Month', 'Sales'])

    return display_data