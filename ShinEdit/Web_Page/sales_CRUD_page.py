import streamlit as st
import pandas as pd
import numpy as np

from GetData.salesdata import get_one_salesdata
from DropdownInfo.filtersearch import get_details
from HistoryData.query_data import updatedata
from HistoryData.changehistory_update import history_update

year = [2022, 2023, 2024, 2025]
month = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]

def Sales_CRUD(cur, conn, salesperson, all_data, display_data):
    st.header("Sales Record")

    # ------------------ FILTER SEARCH ------------------
    col1, col2 = st.columns(2)

    with col1:
        filopt = ["Default", "SalesPersonID", "Year", "Month"]
        filters = st.selectbox("Filter Search", filopt, index = 0)

    with col2:
        if filters == 'Default':
            st.selectbox("", options = [], disabled = True)
            displaying = display_data
        else:
            details = get_details(cur, 'Sales', filters)
            selected_details = st.selectbox("", details, index = 0)
            displaying = get_one_salesdata(cur, filters, selected_details)

    # ------------------ DISPLAY DATA & SET UP ------------------
    st.dataframe(displaying)
    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # ------------------ ADD RECORD ------------------
    with add_record:
        if len(all_data) == 0:
            new_value = "S001"
        else:
            last_value = all_data['SalesID'].iloc[-1]
            prefix = ''.join(filter(str.isalpha, last_value))
            number = ''.join(filter(str.isdigit, last_value))
            new_number = str(int(number) + 1).zfill(len(number))
            new_value = prefix + new_number

        st.subheader("Add New Sale Record")

        with st.form("Add Record"):
            new_id = st.text_input("Sales ID", value = new_value, disabled = True)
            insert_salesperson = st.selectbox("Sales Person ID", salesperson)
            new_quantity = st.number_input("Number of product")
            new_year = st.selectbox("Year", year, index = 3)
            new_month = st.selectbox("Month", month, index = 4)
            new_sales = st.number_input("Sales Amount", min_value = 0)
            submitted = st.form_submit_button("Add Sale")

            if submitted:
                st.session_state["new_sale_data"] = {
                    "id": new_id,
                    "salesperson": insert_salesperson,
                    "quantity": new_quantity,
                    "year": new_year,
                    "month": new_month,
                    "sales": new_sales
                }
                st.session_state["confirm_add"] = True

        if st.session_state.get("confirm_add", False):
            st.warning("⚡ **Confirm Adding New Sales Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Add", use_container_width = True, key = "confirm_add_btn"):
                    try:
                        data = st.session_state["new_sale_data"]
                        cur.execute(
                            "INSERT INTO sales (salesid, salespersonid, quantity, year, month, sales) VALUES (%s, %s, %s, %s, %s, %s)",
                            (data["id"], data["salesperson"], data["quantity"], data["year"], data["month"], data["sales"])
                        )
                        conn.commit()

                        history_update(cur, conn, "Sales", data["id"], "SalesID", "Insert", "-", data["id"])
                        history_update(cur, conn, "Sales", data["id"], "SalesPersonID", "Insert", "-", data["salesperson"])
                        history_update(cur, conn, "Sales", data["id"], "Quantity", "Insert", "-", data["quantity"])
                        history_update(cur, conn, "Sales", data["id"], "Year", "Insert", "-", data["year"])
                        history_update(cur, conn, "Sales", data["id"], "Month", "Insert", "-", data["month"])
                        history_update(cur, conn, "Sales", data["id"], "Sales", "Insert", "-", data["sales"])

                        st.success("✅ New sale record added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_add"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width = True, key = "cancel_add_btn"):
                    st.session_state["confirm_add"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update Sale Record")

        selected_update = st.selectbox("Select Sale to Update", all_data["SalesID"].tolist(), key = "update_sales")
        update_data = get_one_salesdata(cur, 'SalesID', selected_update)
        st.dataframe(update_data)

        with st.form("Update Record"):
            update_salesperson = st.selectbox("Sales Person ID", salesperson,
                                              index = salesperson.index(update_data['Sales Person ID'].values[0]))
            update_quantity = st.number_input("Number of product", value = update_data['Quantity'].values[0])
            update_year = st.selectbox("Year", year, index = year.index(update_data['Year'].values[0]))
            update_month = st.selectbox("Month", month, index = month.index(update_data['Month'].values[0]))
            update_amount = st.number_input("Sales Amount", value = update_data['Sales'].values[0], min_value = 0)

            update_submitted = st.form_submit_button("Update Record")

            if update_submitted:
                st.session_state["update_sale_data"] = {
                    "salesid": selected_update,
                    "salesperson": update_salesperson,
                    "quantity": update_quantity,
                    "year": update_year,
                    "month": update_month,
                    "sales": update_amount,
                    "current": update_data.iloc[0]
                }
                st.session_state["confirm_update"] = True

        if st.session_state.get("confirm_update", False):
            st.warning("⚡ **Confirm Updating Sale Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Update", use_container_width = True, key = "confirm_update_btn"):
                    try:
                        data = st.session_state["update_sale_data"]
                        current = data["current"]

                        if data["salesperson"] != current['Sales Person ID']:
                            updatedata(cur, conn, 'Sales', data["salesid"], 'SalesPersonID', current['Sales Person ID'], data["salesperson"])

                        if data["quantity"] != current['Quantity']:
                            updatedata(cur, conn, 'Sales', data["salesid"], 'Quantity', current['Quantity'], data["quantity"])

                        if data["year"] != current['Year']:
                            updatedata(cur, conn, 'Sales', data["salesid"], 'Year', current['Year'], data["year"])

                        if data["month"] != current['Month']:
                            updatedata(cur, conn, 'Sales', data["salesid"], 'Month', current['Month'], data["month"])

                        if data["sales"] != current['Sales']:
                            updatedata(cur, conn, 'Sales', data["salesid"], 'Sales', current['Sales'], data["sales"])

                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_update"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width = True, key = "cancel_update_btn"):
                    st.session_state["confirm_update"] = False
                    st.rerun()

    # ------------------ DELETE RECORD ------------------
    with delete_record:
        st.subheader("Delete Sale Record")

        selected_delete = st.selectbox("Select Sale to Delete", all_data["SalesID"].tolist(), key="delete_sales")
        delete_data = get_one_salesdata(cur, 'SalesID', selected_delete)
        st.dataframe(delete_data)

        if st.button("Delete Record", key = "delete_sales_btn"):
            st.session_state["delete_sale_data"] = {
                "id": selected_delete,
                "salesperson": delete_data['Sales Person ID'].values[0],
                "quantity": delete_data['Quantity'].values[0],
                "year": delete_data['Year'].values[0],
                "month": delete_data['Month'].values[0],
                "sales": delete_data['Sales'].values[0]
            }
            st.session_state["confirm_delete"] = True

        if st.session_state.get("confirm_delete", False):
            st.warning("⚡ **Confirm Deleting Sale Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Delete", use_container_width = True, key = "confirm_delete_btn"):
                    try:
                        data = st.session_state["delete_sale_data"]

                        cur.execute("DELETE FROM sales WHERE salesid = %s", (data["id"],))
                        conn.commit()

                        history_update(cur, conn, "Sales", data["id"], "SalesID", "Delete", data["id"], "-")
                        history_update(cur, conn, "Sales", data["id"], "SalesPersonID", "Delete", data["salesperson"], "-")
                        history_update(cur, conn, "Sales", data["id"], "Quantity", "Delete", data["quantity"], "-")
                        history_update(cur, conn, "Sales", data["id"], "Year", "Delete", data["year"], "-")
                        history_update(cur, conn, "Sales", data["id"], "Month", "Delete", data["month"], "-")
                        history_update(cur, conn, "Sales", data["id"], "Sales", "Delete", data["sales"], "-")

                        st.success("✅ Record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_delete"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Delete", use_container_width = True, key = "cancel_delete_btn"):
                    st.session_state["confirm_delete"] = False
                    st.rerun()