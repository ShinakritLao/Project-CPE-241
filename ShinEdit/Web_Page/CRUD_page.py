import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def Sales_CRUD(cur, conn, salesperson):
    st.header("Sales CRUD")
    # test
    st.subheader("Manage Sales Records")

    # Load existing sales data
    all_sales_data = pd.read_sql("SELECT * FROM sales", conn)
    st.dataframe(all_sales_data)

    st.markdown("---")

    # Form to add new record
    st.subheader("Add New Sale Record")
    with st.form("Add Record"):
        new_sale_id = st.text_input("Sale ID")
        insert_salesperson = st.selectbox("Sales Person ID", salesperson)
        new_quantity = st.number_input("Number of product")
        new_year = st.selectbox("Year", [2020, 2021, 2022, 2023, 2024, 2025])  # Remove 'Years'
        new_month = st.selectbox("Month", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        new_amount = st.number_input("Sales Amount", min_value=0)
        submitted = st.form_submit_button("Add Sale")

        if submitted:
            try:
                cur.execute(
                    "INSERT INTO sales (salesid, salespersonid, quantity, year, month, sales) VALUES (%s, %s, %s, %s, %s, %s)",
                    (new_sale_id, insert_salesperson, new_quantity, new_year, new_month, new_amount)
                )
                conn.commit()
                st.success("New sale record added successfully!")
            except Exception as e:
                st.error(f"Failed to insert record: {e}")

    st.markdown("---")

    # Select a row to update or delete
    st.subheader("Update / Delete Sale Record")
    selected_data = st.selectbox("Select Sale", all_sales_data["salesid"].tolist())
    new_amount = st.number_input("New Sales Amount", min_value=0)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Record"):
            try:
                cur.execute("UPDATE sales SET sales = %s WHERE salesid = %s", (new_amount, selected_data))
                conn.commit()
                st.success("Record updated successfully!")
            except Exception as e:
                st.error(f"Update failed: {e}")

    with col2:
        if st.button("Delete Record"):
            try:
                cur.execute("DELETE FROM sales WHERE salesid = %s", (selected_data,))
                conn.commit()
                st.warning("Record deleted successfully!")
            except Exception as e:
                st.error(f"Delete failed: {e}")