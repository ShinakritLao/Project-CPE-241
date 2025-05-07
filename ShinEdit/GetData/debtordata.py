import pandas as pd


def get_debtordata_dash(cur, salesperson, salesyear):

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT * FROM Debtor WHERE salespersonid = '{salesperson}' AND EXTRACT(YEAR FROM date) = {salesyear};")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    debtordata = pd.DataFrame(result, columns = ['DebtorID', 'CompanyName', 'SalesPersonID', 'ProductID', 'Price',
                                                 'Debt', 'Paid', 'Date', 'Status'])

    # Convert into integer type
    debtordata['Price'] = debtordata['Price'].astype(int)

    return debtordata

def get_debtordata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Debtor ORDER BY DebtorID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    debtordata = pd.DataFrame(result, columns = ['DebtorID', 'CompanyName', 'SalesPersonID', 'ProductID', 'Price',
                                                 'Debt', 'Paid', 'Date', 'Status'])

    # Convert into integer type
    debtordata['Price'] = debtordata['Price'].astype(int)

    return debtordata

def get_display_debtor(cur):

    # SQL part: Get data from the table in database
    cur.execute("""
            SELECT DebtorID, CompanyName, Debtor.SalesPersonID, SalesName, Debtor.ProductID, ProductName,
            Price, Debt, Paid, Debtor.Date, Debtor.Status FROM Debtor 
            JOIN SalesPerson ON Debtor.SalesPersonID = SalesPerson.SalesPersonID
            JOIN Product ON Debtor.ProductID = Product.ProductID
            ORDER BY DebtorID;
            """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Debtor ID', 'Company Name', 'Sales Person ID', 'Sales Name',
                                                        'Product ID', 'Product Name', 'Price', 'Debt', 'Paid', 'Date', 'Status'])

    return display_data

def get_one_debtordata(cur, loc, subloc):

    # SQL part: Get data from the table in database
    cur.execute(f"""
                SELECT DebtorID, CompanyName, Debtor.SalesPersonID, SalesName, Debtor.ProductID, ProductName, Price, Debt, 
                Paid, Debtor.Date, Debtor.Status FROM Debtor JOIN SalesPerson ON Debtor.SalesPersonID = SalesPerson.SalesPersonID
                JOIN Product ON Debtor.ProductID = Product.ProductID 
                WHERE Debtor.{loc} = '{subloc}' ORDER BY DebtorID;
                """, (subloc,))
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Debtor ID', 'Company Name', 'Sales Person ID', 'Sales Name',
                                                        'Product ID', 'Product Name', 'Price', 'Debt', 'Paid', 'Date', 'Status'])

    return display_data