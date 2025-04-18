import pandas as pd

def get_productdata(cursor, salename, year):
    # Execute the SQL query with proper formatting and parameters
    (cursor.execute
    (f"""
        SELECT * FROM SalesProduct;
    """))

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Convert the result to a pandas DataFrame
    productdata = pd.DataFrame(result, columns=['SalesID', 'ProductID', 'Total Sales', 'Total Costs', 'Status'])
    productdata['Total Sales'] = productdata['Total Sales'].astype(int)
    productdata['Total Costs'] = productdata['Total Costs'].astype(int)

    return productdata