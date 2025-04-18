import pandas as pd
def get_debtordata(cursor, salename, year):
    # Execute the SQL query with swapped columns
    (cursor.execute
    (f"""
        SELECT * FROM debtor;
    """))

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Convert the result to a pandas DataFrame
    debtordata = pd.DataFrame(result, columns=['DebtorID', 'Company Name', 'SalesID', 'ProductID', 'Price', 'Debt', 'Paid', 'Date', 'Status'])

    # Convert the 'Year' column to integer type
    debtordata['Price'] = debtordata['Price'].astype(int)

    return debtordata