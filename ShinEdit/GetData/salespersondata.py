import pandas as pd

def get_salespersondata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM SalesPerson ORDER BY SalesPersonID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    salespersondata = pd.DataFrame(result, columns = ['SalesPersonID', 'SalesName', 'DOB', 'Gender', 'Position', 'PhoneNumber'])

    return salespersondata