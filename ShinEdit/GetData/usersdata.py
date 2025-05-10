import pandas as pd

def get_usersdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Users ORDER BY Username;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    usersdata = pd.DataFrame(result, columns = ['Username', 'SalesPersonID','Password', 'Nickname', 'Email', 'Status'])

    return usersdata

def get_display_users(cur):

    # SQL part: Get data from the table in database
    cur.execute("""
            SELECT Username, SalesPerson.SalesPersonID, SalesName, Nickname, Email FROM Users
            JOIN SalesPerson ON Users.SalesPersonID = SalesPerson.SalesPersonID ORDER BY SalesPerson.SalesPersonID;
            """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Username', 'Sales Person ID', 'Sales Name',
                                                        'Nickname', 'Email'])

    return display_data

def get_one_usersdata(cur, loc, subloc):

    # SQL part: Get data from the table in database
    cur.execute(f"""
                SELECT Username, SalesPerson.SalesPersonID, SalesName, Nickname, Email FROM Users
                JOIN SalesPerson ON Users.SalesPersonID = SalesPerson.SalesPersonID WHERE Users.{loc} = '{subloc}' 
                 ORDER BY SalesPerson.SalesPersonID;
                """, (subloc,))
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['Username', 'Sales Person ID', 'Sales Name',
                                                        'Nickname', 'Email'])

    return display_data