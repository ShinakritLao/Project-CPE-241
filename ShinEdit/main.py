# Dont Delete Kao Jai Mai LingLing
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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

# Get display function
from GetData.debtordata import get_display_debtor
from GetData.kpidata import get_display_kpi
from GetData.salesdata import get_display_sales
from GetData.salespersondata import get_salespersondata
from GetData.salesproductdata import get_display_salesproduct
from GetData.usersdata import get_display_users

display_debtor = get_display_debtor(cur)
display_kpi = get_display_kpi(cur)
display_sales = get_display_sales(cur)
display_salespersondata = get_salespersondata(cur)
display_salesproduct = get_display_salesproduct(cur)
display_users = get_display_users(cur)

# Main function
from Web_Page.login_page import login
from Web_Page.dashboard_page import dashboard
from Web_Page.sales_CRUD_page import Sales_CRUD
from Web_Page.restoredata_page import restoredata_CRUD
from Web_Page.users_page import show_user_sidebar
from Web_Page.users_page import edit_user_page

# Main function set up Streamlit
def main():
    # SetUp wide mode
    st.set_page_config(layout="wide")

    # Run login first
    login(users_data,conn)

    # If not logged in, stop everything
    if not st.session_state.logged_in:
        st.stop()

    #show sidebar
    show_user_sidebar(users_data, display_salespersondata, st.session_state.username,conn)

    #check modify button
    if "modify_page" not in st.session_state:
        st.session_state.modify_page = False

    if st.session_state.modify_page:
        edit_user_page(users_data, display_salespersondata, st.session_state.username,conn)
        st.stop()

    # Create tabs
    Sales_Dashboard_tab, Sales_CRUD_tab, Restore_CRUD_tab = st.tabs(["Sales Dashboard", "Sales", "Restore Data"])

    with Sales_Dashboard_tab:
        dashboard(salesyear, salesperson, cur)

    with Sales_CRUD_tab:
        Sales_CRUD(cur, conn, salesperson, sales_data, display_sales)

    with Restore_CRUD_tab:
        restoredata_CRUD(cur, conn, changehistory_data)

        # # Based on user position (role), show specific pages
        # if st.session_state.position == "???":
        #     Sales_Dashboard_tab, Sales_CRUD_tab, Restore_CRUD_tab = st.tabs(
        #         ["Sales Dashboard", "Sales", "Restore Data"])
        #     with Sales_Dashboard_tab:
        #         dashboard(salesyear, salesperson, cur)
        #     with Sales_CRUD_tab:
        #         Sales_CRUD(cur, conn, salesperson, sales_data, display_sales)
        #     with Restore_CRUD_tab:
        #         restoredata_CRUD(cur, conn, changehistory_data)
        #
        # elif st.session_state.position == "????":
        #     Sales_Dashboard_tab, Sales_CRUD_tab = st.tabs(["Sales Dashboard", "Sales"])
        #     with Sales_Dashboard_tab:
        #         dashboard(salesyear, salesperson, cur)
        #     with Sales_CRUD_tab:
        #         Sales_CRUD(cur, conn, salesperson, sales_data, display_sales)

# Run main function
if __name__ == "__main__": main()