import pandas as pd

def get_kpidata_dash(cur, salesperson, salesyear):

    # SQL part: Get data from the table in database
    cur.execute(f"SELECT * FROM KPI WHERE salespersonid = '{salesperson}' AND year = {salesyear};")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    kpidata = pd.DataFrame(result, columns = ['KPI_ID','SalesPersonID', 'Year', 'TargetQ', 'Quotation', 'TargetSO',
                                              'SaleOrder', 'AllCustomer', 'CustomerHand'])

    # Convert into integer type
    kpidata['Year'] = kpidata['Year'].astype(int)
    kpidata['TargetQ'] = kpidata['TargetQ'].astype(int)
    kpidata['Quotation'] = kpidata['Quotation'].astype(int)
    kpidata['TargetSO'] = kpidata['TargetSO'].astype(int)
    kpidata['SaleOrder'] = kpidata['SaleOrder'].astype(int)
    kpidata['AllCustomer'] = kpidata['AllCustomer'].astype(int)
    kpidata['CustomerHand'] = kpidata['CustomerHand'].astype(int)

    return kpidata

def get_kpidata(cur):

    # SQL part: Get data from the table in database
    cur.execute("SELECT * FROM KPI ORDER BY KPI_ID;")
    result = cur.fetchall()

    # Convert the result to a pandas DataFrame
    kpidata = pd.DataFrame(result, columns = ['KPI_ID','SalesPersonID', 'Year', 'TargetQ', 'Quotation', 'TargetSO',
                                              'SaleOrder', 'AllCustomer', 'CustomerHand'])

    # Convert into integer type
    kpidata['Year'] = kpidata['Year'].astype(int)
    kpidata['TargetQ'] = kpidata['TargetQ'].astype(int)
    kpidata['Quotation'] = kpidata['Quotation'].astype(int)
    kpidata['TargetSO'] = kpidata['TargetSO'].astype(int)
    kpidata['SaleOrder'] = kpidata['SaleOrder'].astype(int)
    kpidata['AllCustomer'] = kpidata['AllCustomer'].astype(int)
    kpidata['CustomerHand'] = kpidata['CustomerHand'].astype(int)

    return kpidata

def get_display_kpi(cur):

    # SQL part: Get data from the table in database
    cur.execute("""
            SELECT KPI_ID, KPI.SalesPersonID, SalesName, Year, TargetQ, Quotation, TargetSO, SalesOrder,
            AllCustomer, CustomerInHand FROM KPI 
            JOIN SalesPerson ON KPI.SalesPersonID = SalesPerson.SalesPersonID ORDER BY KPI_ID;
            """)
    display_sql = cur.fetchall()

    # Convert the result to a pandas DataFrame
    display_data = pd.DataFrame(display_sql, columns = ['KPI ID','Sales Person ID', 'Sales Name', 'Year',
                                                        'Target Quotation', 'Quotation', 'Target Sales Order',
                                                        'Sale Order', 'All Customer', 'Customer in Hand'])

    return display_data