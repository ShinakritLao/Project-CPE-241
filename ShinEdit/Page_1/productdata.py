import pandas as pd

def get_productdata(cursor, salename, year):
    # Execute the SQL query with proper formatting and parameters
    (cursor.execute
    (f"""
        sql
    """))

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Convert the result to a pandas DataFrame
    productdata = pd.DataFrame(result, columns=['ProductID', 'Product Name', 'Number Of Product', 'Total Sales', 'Total Costs', 'Status'])

    return productdata