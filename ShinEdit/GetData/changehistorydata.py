import pandas as pd

def get_changehistorydata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM Change_History ORDER BY ChangeID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    changehistorydata = pd.DataFrame(result, columns = ['ChangeID', 'Location', 'SubLocation', 'Activity',
                                                        'OriginalData', 'UpdatedData', 'Username', 'Date', 'Time'])

    # Convert into integer type
    changehistorydata['Date'] = pd.to_datetime(changehistorydata['Date'], format = '%Y-%m-%d')
    changehistorydata['Time'] = pd.to_datetime(changehistorydata['Time'], format = '%H:%M:%S')

    return changehistorydata