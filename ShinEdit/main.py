import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import psycopg2

# Host with database from supabase
conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres.dawmfltwbrcjmlgmjoak",
    password = "!Mental241",
    host = "aws-0-ap-southeast-1.pooler.supabase.com",
    port = "5432"
)
cur = conn.cursor()

# Dropdown
from DropdownInfo.salesyear import get_salesyear
from DropdownInfo.salesperson import get_salesperson

salesyear = get_salesyear(cur)
salesperson = get_salesperson(cur)

# Get data
from GetData.salesdata import get_salesdata
from GetData.productdata import get_productdata
from GetData.salespersondata import get_salespersondata
from GetData.kpidata import get_kpidata
from GetData.debtordata import get_debtordata
from GetData.salesproductdata import get_salesproductdata
from GetData.usersdata import get_usersdata
from GetData.changehistorydata import get_changehistorydata

sales_data = get_salesdata(cur)
product_data = get_productdata(cur)
salesperson_data = get_salespersondata(cur)
kpi_data = get_kpidata(cur)
debtor_data = get_debtordata(cur)
salesproduct_data = get_salesproductdata(cur)
users_data = get_usersdata(cur)
changehistory_data = get_changehistorydata(cur)

# Main function
from Web_Page.login_page import login
from Web_Page.dashboard_page import dashboard
from Web_Page.CRUD_page import Sales_CRUD

# Main function set up Streamlit
def main():
    # SetUp wide mode
    st.set_page_config(layout="wide")

    # # Run login first
    # login(users_data)
    #
    # # If not logged in, stop everything
    # if not st.session_state.logged_in:
    #     st.stop()
    #
    # # Sidebar Logout button
    # if st.sidebar.button("Logout"):
    #     st.session_state.logged_in = False
    #     st.rerun()

    # Create tabs
    Sales_Dashboard_tab, Sales_CRUD_tab = st.tabs(["Sales Dashboard", "Sales CRUD"])

    with Sales_Dashboard_tab:
        dashboard(cur, conn, salesyear, salesperson, sales_data, product_data, salesperson_data, kpi_data, debtor_data, salesproduct_data)

    with Sales_CRUD_tab:
        Sales_CRUD(cur, conn, salesperson, sales_data)

# Run main function
if __name__ == "__main__": main()