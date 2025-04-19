import pandas as pd

def get_usersdata(cursor):
    cursor.execute("""
        SELECT * FROM Users;
    """)
    result = cursor.fetchall()
    usersdata = pd.DataFrame(result, columns = ['Username', 'Password', 'Name', 'Lastname', 'Position', 'PhoneNumber'])
    return usersdata