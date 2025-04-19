import pandas as pd

def get_usersdata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Users;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    usersdata = pd.DataFrame(result, columns = ['Username', 'Password', 'Name', 'Lastname', 'Position', 'PhoneNumber'])

    return usersdata