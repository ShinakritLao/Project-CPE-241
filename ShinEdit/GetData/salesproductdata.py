import pandas as pd

def get_salesproductdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM SalesProduct;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    salesproduct = pd.DataFrame(result, columns = ['SalesID', 'ProductID', 'TotalSales', 'TotalCost', 'Status'])

    # Convert into integer type
    salesproduct['TotalSales'] = salesproduct['TotalSales'].astype(int)
    salesproduct['TotalCost'] = salesproduct['TotalCost'].astype(int)
    salesproduct['Status'] = salesproduct['Status'].astype(int)

    return salesproduct