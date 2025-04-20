import streamlit as st
import pandas as pd
import numpy as np
from Web_Page.changehistory_update import history_update

year = [2022, 2023, 2024, 2025]
month = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]

def Sales_CRUD(cur, conn, salesperson, all_sales_data):
    st.header("Sales Record")

    cur.execute("""
        SELECT SalesID, Sales.SalesPersonID, SalesName, Quantity, Year, Month, Sales FROM Sales
        JOIN SalesPerson ON Sales.SalesPersonID = SalesPerson.SalesPersonID ORDER BY SalesID;
        """)
    display_sql = cur.fetchall()
    display_data = pd.DataFrame(display_sql, columns = ['Sales ID', 'Sales Person ID', 'Sales Name', 'Quantity',
                                                        'Year', 'Month', 'Sales'])

    # Load existing sales data
    st.dataframe(display_data)

    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # Add record
    with add_record:
        # Increase sales id
        if len(all_sales_data) == 0:
            new_value = "S001"
        else:
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
            new_year = st.selectbox("Year", year, index = 3)
            new_month = st.selectbox("Month", month, index = 3)
            new_amount = st.number_input("Sales Amount", min_value=0)
            submitted = st.form_submit_button("Add Sale")

            if submitted:
                try:
                    cur.execute(
                        "INSERT INTO sales (salesid, salespersonid, quantity, year, month, sales) VALUES (%s, %s, %s, %s, %s, %s)",
                        (new_sale_id, insert_salesperson, new_quantity, new_year, new_month, new_amount)
                    )
                    conn.commit()

                    # Update history change
                    history_update(cur, conn, "Sales", new_sale_id, "SalesID", "Insert", "-", new_sale_id)
                    history_update(cur, conn, "Sales", new_sale_id, "SalesPersonID", "Insert", "-", insert_salesperson)
                    history_update(cur, conn, "Sales", new_sale_id, "Quantity", "Insert", "-", new_quantity)
                    history_update(cur, conn, "Sales", new_sale_id, "Year", "Insert", "-", new_year)
                    history_update(cur, conn, "Sales", new_sale_id, "Month", "Insert", "-", new_month)
                    history_update(cur, conn, "Sales", new_sale_id, "Sales", "Insert", "-", new_amount)

                    st.success("New sale record added successfully!")
                except Exception as e:
                    st.error(f"Failed to insert record: {e}")

    # Update record
    with update_record:
        st.subheader("Update Sale Record")

        selected_update_data = st.selectbox("Select Sale", all_sales_data["SalesID"].tolist(), key="update_selectbox")
        current_data = all_sales_data.loc[all_sales_data['SalesID'] == selected_update_data]
        st.dataframe(display_data.loc[display_data['Sales ID'] == current_data['SalesID'].values[0]])

        with st.form("Update Record"):

            # Update form
            update_salesperson = st.selectbox("Sales Person ID", salesperson, index = salesperson.index(current_data['SalesPersonID'].values[0]))
            update_quantity = st.number_input("Number of product", value = current_data['Quantity'].values[0])
            update_year = st.selectbox("Year", year, index = year.index(current_data['Year'].values[0]))
            update_month = st.selectbox("Month", month, index = month.index(current_data['Month'].values[0]))
            new_amount = st.number_input("Sales Amount", value = current_data['Sales'].values[0], min_value = 0)

            if st.form_submit_button("Update Record"):
                try:
                    if update_salesperson != current_data['SalesPersonID'].values[0]:
                        cur.execute("UPDATE sales SET salespersonid = %s WHERE salesid = %s",
                                    (update_salesperson, selected_update_data))
                        history_update(cur, conn, "Sales", selected_update_data, "SalesPersonID",
                                       "Update", current_data['SalesPersonID'].values[0], update_salesperson)
                    if update_quantity != current_data['Quantity'].values[0]:
                        cur.execute("UPDATE sales SET quantity = %s WHERE salesid = %s",
                                    (update_quantity, selected_update_data))
                        history_update(cur, conn, "Sales", selected_update_data, "Quantity",
                                       "Update", current_data['Quantity'].values[0], update_quantity)
                    if update_year != current_data['Year'].values[0]:
                        cur.execute("UPDATE sales SET year = %s WHERE salesid = %s",
                                    (update_year, selected_update_data))
                        history_update(cur, conn, "Sales", selected_update_data, "Year",
                                       "Update", current_data['Year'].values[0], update_year)
                    if update_month != current_data['Month'].values[0]:
                        cur.execute("UPDATE sales SET month = %s WHERE salesid = %s",
                                    (update_month, selected_update_data))
                        history_update(cur, conn, "Sales", selected_update_data, "Month",
                                       "Update", current_data['Month'].values[0], update_month)
                    if new_amount != current_data['SalesPersonID'].values[0]:
                        cur.execute("UPDATE sales SET sales = %s WHERE salesid = %s",
                                    (new_amount, selected_update_data))
                        history_update(cur, conn, "Sales", selected_update_data, "Sales",
                                       "Update", current_data['Sales'].values[0], new_amount)
                    conn.commit()
                    st.success("Record updated successfully!")
                except Exception as e:
                    st.error(f"Update failed: {e}")

    # Delete record
    with delete_record:
        st.subheader("Delete Sale Record")

        selected_delete_data = st.selectbox("Select Sale", all_sales_data["SalesID"].tolist(), key="delete_selectbox")
        st.dataframe(display_data.loc[display_data['Sales ID'] == selected_delete_data])

        if st.button("Delete Record"):
            try:
                cur.execute("DELETE FROM sales WHERE salesid = %s", (selected_delete_data,))
                history_update(cur, conn, "Sales", selected_delete_data, "-", "Delete", "-", "-")
                conn.commit()
                st.warning("Record deleted successfully!")
            except Exception as e:
                st.error(f"Delete failed: {e}")