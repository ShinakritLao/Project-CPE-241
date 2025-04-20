import pandas as pd

def get_changehistorydata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM History_Change ORDER BY ChangeID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    changehistorydata = pd.DataFrame(result, columns = ['ChangeID', 'Username', 'Table', 'Location', 'SubLocation',
                                                        'Action', 'OriginalData', 'UpdatedData', 'Date', 'Time'])

    return changehistorydata