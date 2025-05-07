import pandas as pd

def get_salespersondata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM SalesPerson ORDER BY SalesPersonID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    salespersondata = pd.DataFrame(result, columns = ['SalesPersonID', 'SalesName', 'DOB', 'Gender', 'Position', 'PhoneNumber'])

    return salespersondata


def get_one_salespersondata(cur, loc, subloc):
    cur.execute(f"""
        SELECT SalesPersonID, SalesName, DOB, Gender, Position, PhoneNumber 
        FROM SalesPerson
        WHERE {loc} = %s OR {loc} LIKE '%%{subloc}%%'
        ORDER BY SalesPersonID;
    """, (subloc,))

    display_sql = cur.fetchall()

    display_data = pd.DataFrame(display_sql,
                                columns=['SalesPersonID', 'SalesName', 'DOB', 'Gender', 'Position', 'PhoneNumber'])
    return display_data

