import pandas as pd

# from HistoryData.restoredata import get_primary

def get_changehistorydata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM History_Change ORDER BY ChangeID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    changehistorydata = pd.DataFrame(result, columns = ['ChangeID', 'Username', 'Table', 'Location', 'SubLocation',
                                                        'Action', 'OriginalData', 'UpdatedData', 'Date', 'Time'])

    return changehistorydata

def get_one_historydata(cur, loc, subloc):

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT * FROM History_Change WHERE {loc} = '{subloc}' ORDER BY ChangeID;")
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['ChangeID', 'Username', 'Table', 'Location', 'SubLocation',
                                                        'Action', 'OriginalData', 'UpdatedData', 'Date', 'Time'])

    return display_data

def get_columns(cur, table):

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}';")
    result = cur.fetchall()

    columnsdata = []

    for record in result:
        columnsdata.append(record[0])
    return columnsdata

def increase_pri(value):
    prefix = ''.join(filter(str.isalpha, value))
    number = ''.join(filter(str.isdigit, value))
    new_number = str(int(number) + 1).zfill(len(number))
    return prefix + new_number

def get_deletedata(cur, table, loc):

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}';")
    result = cur.fetchone()

    deletedata = []

    for _ in range(int(result[0])):
        cur.execute(f"SELECT Original_Data FROM History_Change WHERE ChangeID = '{loc}';")
        loc = increase_pri(loc)

        result = cur.fetchone()
        deletedata.append(result[0])

    return deletedata