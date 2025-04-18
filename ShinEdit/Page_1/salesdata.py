import pandas as pd
def get_salesdata(cursor, salename, year):
    # Execute the SQL query
    (cursor.execute
    (f"""
        SELECT * FROM Sales;
    """))

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Convert the result to a pandas DataFrame
    salesdata = pd.DataFrame(result, columns=['SalesID', 'SalesPersonID', 'Quantity', 'Year', 'Month', 'Sales'])

    # Convert the 'year' column to integer type
    salesdata['Quantity'] = salesdata['Quantity'].astype(int)
    salesdata['Year'] = salesdata['Year'].astype(int)
    salesdata['Sales'] = salesdata['Sales'].astype(int)

    return salesdata