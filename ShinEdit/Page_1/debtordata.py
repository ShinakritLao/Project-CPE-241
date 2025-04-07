import pandas as pd
def get_debtordata(cursor, salename, year):
    # Execute the SQL query with swapped columns
    (cursor.execute
    (f"""
        sql
    """))

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Convert the result to a pandas DataFrame
    debtordata = pd.DataFrame(result, columns=['Company Name', 'ProductID', 'Product Name', 'Price', 'Debt', 'Paid', 'Date', 'Status'])

    # Convert the 'Year' column to integer type
    debtordata['Amount'] = debtordata['Amount'].astype(int)

    return debtordata