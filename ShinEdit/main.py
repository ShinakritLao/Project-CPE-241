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
from DropdownInfo.sales import get_salesyear
from DropdownInfo.salesperson import get_salesperson
from DropdownInfo.product import get_product

salesyear = get_salesyear(cur)
salesperson = get_salesperson(cur)
product = get_product(cur)

# Get data
from GetData.salesdata import get_salesdata
from GetData.productdata import get_productdata
from GetData.salespersondata import get_salespersondata
from GetData.kpidata import get_kpidata
from GetData.debtordata import get_debtordata
from GetData.salesproductdata import get_salesproductdata
from GetData.usersdata import get_usersdata
from GetData.changehistorydata import get_changehistorydata
from GetData.newproductdata import get_newproductdata

sales_data = get_salesdata(cur)
product_data = get_productdata(cur)
salesperson_data = get_salespersondata(cur)
kpi_data = get_kpidata(cur)
debtor_data = get_debtordata(cur)
salesproduct_data = get_salesproductdata(cur)
users_data = get_usersdata(cur)
changehistory_data = get_changehistorydata(cur)
newproduct_data = get_newproductdata(cur)

# Get display function
from GetData.debtordata import get_display_debtor
from GetData.kpidata import get_display_kpi
from GetData.salesdata import get_display_sales
from GetData.debtordata import get_display_debtor
from GetData.salespersondata import get_salespersondata
from GetData.salesproductdata import get_display_salesproduct
from GetData.usersdata import get_display_users
from GetData.newproductdata import get_display_newproduct

display_debtor = get_display_debtor(cur)
display_kpi = get_display_kpi(cur)
display_sales = get_display_sales(cur)
display_salespersondata = get_salespersondata(cur)
display_salesproduct = get_display_salesproduct(cur)
display_users = get_display_users(cur)
display_product = get_display_newproduct(cur)

# Main function
from Web_Page.login_page import login
from Web_Page.dashboard_page import dashboard
from Web_Page.sales_CRUD_page import Sales_CRUD
from Web_Page.kpi_CRUD_page import KPI_CRUD
from Web_Page.debtor_CRUD_page import Debtor_CRUD
from Web_Page.salesproduct_CRUD_page import SalesProduct_CRUD
from Web_Page.salesperson_CRUD_page import SalesPerson_CRUD
from Web_Page.restoredata_page import restoredata_CRUD
from Web_Page.users_page import show_user_sidebar
from Web_Page.users_page import edit_user_page
from Web_Page.users_all_page import users_all_page
from Web_Page.product_CRUD_page import Product_CRUD

# Main function set up Streamlit
def main():
    # SetUp wide mode
    st.set_page_config(layout="wide")

    # Run login first
    login(users_data,salesperson_data,conn)

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
    Sales_Dashboard_tab, Sales_CRUD_tab, KPI_CRUD_tab, Debtor_CRUD_tab, SalesProduct_CRUD_tab, SalesPerson_CRUD_tab, Product_CRUD_tab,  Users_tab, Restore_CRUD_tab = (
        st.tabs(["Sales Dashboard", "Sales", "KPI", "Debtor", "Sales Product", "Sales Person" , "Product", "Users", "History"]))

    with Sales_Dashboard_tab:
        dashboard(salesyear, salesperson, cur)

    with Sales_CRUD_tab:
        Sales_CRUD(cur, conn, salesperson, sales_data, display_sales)

    with KPI_CRUD_tab:
        KPI_CRUD(cur, conn, salesperson, kpi_data, display_kpi)

    with Debtor_CRUD_tab:
        Debtor_CRUD(cur, conn, salesperson, product, debtor_data, display_debtor)

    with SalesProduct_CRUD_tab:
        SalesProduct_CRUD(cur, conn, salesperson, salesproduct_data, display_salesproduct)

    with SalesPerson_CRUD_tab:
        SalesPerson_CRUD(cur, conn, salesperson_data, display_salespersondata)

    with Users_tab:
        users_all_page(cur, conn, users_data, display_users)

    with Restore_CRUD_tab:
        restoredata_CRUD(cur, conn, changehistory_data)

# Run main function
if __name__ == "__main__": main()