import pandas as pd

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