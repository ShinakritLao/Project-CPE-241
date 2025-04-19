import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def Sales_CRUD(cur, conn, salesperson, all_sales_data):
    st.header("Sales CRUD")
    st.subheader("Manage Sales Records")

    # Load existing sales data
    st.dataframe(all_sales_data)

    st.markdown("---")

    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # Add record
    with add_record:
        # Increase sales id
        last_value = all_sales_data['SalesID'].iloc[-1]

        prefix = ''.join(filter(str.isalpha, last_value))
        number = ''.join(filter(str.isdigit, last_value))

        new_number = str(int(number) + 1).zfill(len(number))
        new_value = prefix + new_number

        # Form to add new record
        st.subheader("Add New Sale Record")
        with st.form("Add Record"):
            new_sale_id = st.text_input("Sales ID", value = new_value, disabled = True)
            insert_salesperson = st.selectbox("Sales Person ID", salesperson)
            new_quantity = st.number_input("Number of product")
            new_year = st.selectbox("Year", [2023, 2024, 2025])  # Remove 'Years'
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

    # Update record
    with update_record:
        st.subheader("Update Sale Record")

        selected_update_data = st.selectbox("Select Sale", all_sales_data["SalesID"].tolist(), key="update_selectbox")
        st.dataframe(all_sales_data[all_sales_data['SalesID'] == selected_update_data])

        with st.form("Update Record"):

            update_salesperson = st.selectbox("Sales Person ID", salesperson)
            update_quantity = st.number_input("Number of product")
            update_year = st.selectbox("Year", [2023, 2024, 2025])
            update_month = st.selectbox("Month", [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ])
            new_amount = st.number_input("Sales Amount", min_value = 0)

            if st.form_submit_button("Update Record"):
                try:
                    cur.execute("UPDATE sales SET sales = %s WHERE salesid = %s", (new_amount, selected_update_data))
                    conn.commit()
                    st.success("Record updated successfully!")
                except Exception as e:
                    st.error(f"Update failed: {e}")

    # Delete record
    with delete_record:
        st.subheader("Delete Sale Record")

        selected_delete_data = st.selectbox("Select Sale", all_sales_data["SalesID"].tolist(), key="delete_selectbox")
        st.dataframe(all_sales_data.loc[all_sales_data['SalesID'] == selected_delete_data])

        if st.button("Delete Record"):
            try:
                cur.execute("DELETE FROM sales WHERE salesid = %s", (selected_delete_data,))
                conn.commit()
                st.warning("Record deleted successfully!")
            except Exception as e:
                st.error(f"Delete failed: {e}")