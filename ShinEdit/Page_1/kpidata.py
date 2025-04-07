import pandas as pd
def get_kpidata(cursor, salename, year):
    # Execute the SQL query with swapped columns
    (cursor.execute
    (f"""
        sql
    """))

    # Fetch all results from the executed query
    result = cursor.fetchall()

    # Convert the result to a pandas DataFrame
    kpidata = pd.DataFrame(result, columns=['Sales Name', 'Year', 'TargetQ', 'Quotation', 'TargetSO', 'SaleOrder', 'AllCustomer', 'CustomerHand'])

    # Convert the 'Year' column to integer type
    kpidata['Year'] = kpidata['Year'].astype(int)
    kpidata['TargetQ'] = kpidata['TargetQ'].astype(int)
    kpidata['Quotation'] = kpidata['Quotation'].astype(int)
    kpidata['TargetSO'] = kpidata['TargetSO'].astype(int)
    kpidata['SaleOrder'] = kpidata['SaleOrder'].astype(int)
    kpidata['AllCustomer'] = kpidata['AllCustomer'].astype(int)
    kpidata['CustomerHand'] = kpidata['CustomerHand'].astype(int)

    return kpidata