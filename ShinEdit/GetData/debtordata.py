import pandas as pd

def get_debtordata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Debtor ORDER BY DebtorID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    debtordata = pd.DataFrame(result, columns = ['DebtorID', 'CompanyName', 'SalesPersonID', 'ProductID', 'Price', 'Debt', 'Paid', 'Date', 'Status'])

    # Convert into integer type
    debtordata['Price'] = debtordata['Price'].astype(int)

    return debtordata