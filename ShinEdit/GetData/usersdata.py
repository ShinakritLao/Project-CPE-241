import pandas as pd

def get_usersdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Users ORDER BY Username;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    usersdata = pd.DataFrame(result, columns = ['Username', 'SalesPersonID', 'Password', 'DOB', 'Gender', 'Position', 'PhoneNumber'])

    return usersdata

def get_display_users(cur):

    # SQL part: Get data from the table in database
    cur.execute("""
            SELECT Username, SalesPerson.SalesPersonID, SalesName, DOB, Gender, Position, PhoneNumber FROM Users
            JOIN SalesPerson ON Users.SalesPersonID = SalesPerson.SalesPersonID ORDER BY Username;
            """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Username', 'Sales Person ID', 'Sales Name', 'Date of Birth',
                                                        'Gender', 'Position', 'Phone Number'])

    return display_data