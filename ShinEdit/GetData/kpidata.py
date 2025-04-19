import pandas as pd

def get_kpidata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM KPI ORDER BY KPI_ID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    kpidata = pd.DataFrame(result, columns = ['KPI_ID','SalesPersonID', 'Year', 'TargetQ', 'Quotation', 'TargetSO', 'SaleOrder', 'AllCustomer', 'CustomerHand'])

    # Convert into integer type
    kpidata['Year'] = kpidata['Year'].astype(int)
    kpidata['TargetQ'] = kpidata['TargetQ'].astype(int)
    kpidata['Quotation'] = kpidata['Quotation'].astype(int)
    kpidata['TargetSO'] = kpidata['TargetSO'].astype(int)
    kpidata['SaleOrder'] = kpidata['SaleOrder'].astype(int)
    kpidata['AllCustomer'] = kpidata['AllCustomer'].astype(int)
    kpidata['CustomerHand'] = kpidata['CustomerHand'].astype(int)

    return kpidata