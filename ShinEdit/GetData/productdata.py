import pandas as pd

def get_productdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM SalesProduct;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    productdata = pd.DataFrame(result, columns = ['SalesID', 'ProductID', 'Total Sales', 'Total Costs', 'Status'])

    # Convert into integer type
    productdata['Total Sales'] = productdata['Total Sales'].astype(int)
    productdata['Total Costs'] = productdata['Total Costs'].astype(int)

    return productdata