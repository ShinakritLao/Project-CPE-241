import pandas as pd

def get_productdata_dash(cur, salesperson, salesyear):

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT s.salespersonid, sp.productid, sp.totalsales, sp.totalcost, sp.status FROM SalesProduct sp  JOIN Sales s ON sp.salesid = s.salesid  WHERE s.salespersonid = '{salesperson}';")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    productdata = pd.DataFrame(result, columns = ['SalesID', 'ProductID', 'Total Sales', 'Total Costs', 'Status'])

    # Convert into integer type
    productdata['Total Sales'] = productdata['Total Sales'].astype(int)
    productdata['Total Costs'] = productdata['Total Costs'].astype(int)

    return productdata

def get_productdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM SalesProduct ORDER BY SalesID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    productdata = pd.DataFrame(result, columns = ['SalesID', 'ProductID', 'Total Sales', 'Total Costs', 'Status'])

    # Convert into integer type
    productdata['Total Sales'] = productdata['Total Sales'].astype(int)
    productdata['Total Costs'] = productdata['Total Costs'].astype(int)

    return productdata