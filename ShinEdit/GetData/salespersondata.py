import pandas as pd

def get_salespersondata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM SalesPerson;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    salespersondata = pd.DataFrame(result, columns = ['SalesPersonID', 'SalesName'])

    return salespersondata