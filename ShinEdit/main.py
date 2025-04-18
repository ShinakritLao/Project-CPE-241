import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import psycopg2

# Dropdown
from DropdownInfo.salesyear import get_salesyear
from DropdownInfo.salesperson import get_salesperson

# Page 1
from Page_1.salesdata import get_salesdata
from Page_1.kpidata import get_kpidata
from Page_1.debtordata import get_debtordata
from Page_1.productdata import get_productdata

# LocalHost need to check before use
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres.dawmfltwbrcjmlgmjoak",
    password="!Mental241",
    host="aws-0-ap-southeast-1.pooler.supabase.com",
    port="5432"
)

cur = conn.cursor()

# Login credentials
USER_CREDENTIALS = {
    "admin": "admin123",
    "salesuser": "sales2025"
}

# Function to format numbers with commas
def format_number(value):
    return f'{value:,}'

# Login page
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with st.form("Login Form"):
            st.subheader("Please log in")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

# Main function set up Streamlit
def main():
    # Set wide mode
    st.set_page_config(layout="wide")

    # Run login first
    login()

    # If not logged in, stop everything
    if not st.session_state.logged_in:
        st.stop()

    # Sidebar Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Load Dropdown
    salesperson = get_salesperson(cur)
    salesyear = get_salesyear(cur)

    # Create tabs
    Sales_Dashboard, Sales_CRUD = st.tabs(["Sales Dashboard", "Sales CRUD"])

    with Sales_Dashboard:
        # Create dropdowns for Sales Name and Year
        col1, col2 = st.columns([1, 1])
        with col1:
            DropdownSalesName = st.selectbox("Select Sales", salesperson)
        with col2:
            DropdownYears = st.selectbox("Select Years", salesyear)

        # Display header
        if DropdownSalesName != "Sales Name" and DropdownYears != "Years":
            st.header(f"({DropdownSalesName}, {DropdownYears})")
        else:
            st.header("SALES")

        # Create a 2x2 grid for the sales tab
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        # Filter sales data
        if DropdownSalesName != "Sales Name" and DropdownYears != "Years":
            sales_data = get_salesdata(cur, DropdownSalesName, DropdownYears)

            # Pie Chart
            base = alt.Chart(sales_data).encode(
                theta=alt.Theta("Sales", stack=True),
                radius=alt.Radius("Sales", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
                color=alt.Color("Month", scale=alt.Scale(scheme='category20')),
                tooltip=["Month", "Sales"]
            )

            circle_chart = base.mark_arc(
                innerRadius=20,
                outerRadius=120,
                opacity=0.8,
                strokeWidth=3,
                stroke='gray'
            ).configure_legend(
                title=None,
                labelFontSize=20,
                labelLimit=200,
            )

            with col1:
                st.subheader("Monthly Sales")
                st.altair_chart(circle_chart, use_container_width=True)

            # KPI Data
            kpi_data = get_kpidata(cur, DropdownSalesName, DropdownYears)

            with col2:
                st.subheader("Key Performance Indicators")
                kpi1, kpi2 = st.columns(2)
                kpi3, kpi4 = st.columns(2)

                def create_metric(label, value, delta):
                    formatted_delta = "{:,}".format(float(delta.replace(',', ''))) if delta else ""
                    st.markdown(
                        f"""
                            <div style="background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; padding: 10px;
                            margin-bottom: 10px; text-align: right;">
                                <div style="font-size:24px;">{label}</div>
                                <div style="font-size:30px;">{value}</div>
                                <div style="font-size:20px; color:green;">{formatted_delta}</div>
                            </div>
                            """,
                        unsafe_allow_html=True
                    )

                try:
                    quotation_rate = (kpi_data['Quotation'].values[0] / kpi_data['TargetQ'].values[0]) * 100
                    sale_order_rate = (kpi_data['SaleOrder'].values[0] / kpi_data['TargetSO'].values[0]) * 100
                    conversion_rate = (kpi_data['SaleOrder'].values[0] / kpi_data['Quotation'].values[0]) * 100
                    customers = f"{kpi_data['CustomerHand'].values[0]} / {kpi_data['AllCustomer'].values[0]}"

                    with kpi1:
                        create_metric("Quotation Rate", f"{quotation_rate:.2f}%", f"{kpi_data['Quotation'].values[0]}")
                    with kpi2:
                        create_metric("Sale Order Rate", f"{sale_order_rate:.2f}%", f"{kpi_data['SaleOrder'].values[0]}")
                    with kpi3:
                        create_metric("Conversion Rate", f"{conversion_rate:.2f}%", "")
                    with kpi4:
                        create_metric("Customers", customers, "")
                except Exception as error:
                    st.warning(f"Error in KPI calculations: {error}")

            # Debtor Data
            debtor_data = get_debtordata(cur, DropdownSalesName, DropdownYears)
            with col3:
                st.subheader("Debtors")
                st.dataframe(debtor_data.reset_index(drop=True))

            # Product Data
            product_data = get_productdata(cur, DropdownSalesName, DropdownYears)
            with col4:
                st.subheader("Product List")
                st.dataframe(product_data.reset_index(drop=True))

        else:
            st.warning("Please select a valid Sales and Year from the dropdowns.")

    with Sales_CRUD:
        st.header("Sales CRUD")
        st.subheader("Manage Sales Records")

        all_sales_data = pd.read_sql("SELECT * FROM sales", conn)
        st.dataframe(all_sales_data)

        st.markdown("---")

        st.subheader("Add New Sale Record")
        with st.form("Add Record"):
            new_sale_id = st.text_input("Sale ID")
            new_quantity = st.number_input("Number of product")
            new_year = st.selectbox("Year", [2020, 2021, 2022, 2023, 2024, 2025])
            new_month = st.selectbox("Month", [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ])
            new_amount = st.number_input("Sales Amount", min_value=0)
            submitted = st.form_submit_button("Add Sale")

            if submitted:
                try:
                    cur.execute(
                        "INSERT INTO sales (salesid, numberofproduct, year, month, sales) VALUES (%s, %s, %s, %s, %s)",
                        (new_sale_id, new_quantity, new_year, new_month, new_amount)
                    )
                    conn.commit()
                    st.success("New sale record added successfully!")
                except Exception as e:
                    st.error(f"Failed to insert record: {e}")

        st.markdown("---")

        st.subheader("Update / Delete Sale Record")
        selected_sale_id = st.selectbox("Select Sale ID", all_sales_data["salesid"].tolist())
        selected_data = all_sales_data[all_sales_data["salesid"] == selected_sale_id].iloc[0]
        new_amount = st.number_input("New Sales Amount", value=selected_data["sales"], min_value=0)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update Record"):
                try:
                    cur.execute("UPDATE sales SET sales = %s WHERE salesid = %s", (new_amount, selected_sale_id))
                    conn.commit()
                    st.success("Record updated successfully!")
                except Exception as e:
                    st.error(f"Update failed: {e}")

        with col2:
            if st.button("Delete Record"):
                try:
                    cur.execute("DELETE FROM sales WHERE salesid = %s", (selected_sale_id,))
                    conn.commit()
                    st.warning("Record deleted successfully!")
                except Exception as e:
                    st.error(f"Delete failed: {e}")

if __name__ == "__main__":
    main()
