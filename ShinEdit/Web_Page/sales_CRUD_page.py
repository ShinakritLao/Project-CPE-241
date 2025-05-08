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
        filopt = ["Default", "Sales Person ID", "Month", "Year"]
        filters = st.selectbox("Filter Search", filopt, index = 0, key = 'Filter_Sales')

        if filters == 'Sales Person ID':
            filters = "SalesPersonID"

    with col2:
        if filters == 'Default':
            st.selectbox("Select Details", options = [], disabled = True, key = 'Details_Sales')
            displaying = display_data
        else:
            details = get_details(cur, 'Sales', filters)
            selected_details = st.selectbox("Select Details", details, index = 0)
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

        with st.form("Add Sales Record"):
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
                if st.button("✅ Confirm Add", use_container_width = True, key = "confirm_sales_add_btn"):
                    try:
                        data = st.session_state["new_sale_data"]
                        cur.execute(
                            "INSERT INTO sales (salesid, salespersonid, quantity, year, month, sales) VALUES (%s, %s, %s, %s, %s, %s)",
                            (data["id"], data["salesperson"], data["quantity"], data["year"], data["month"], data["sales"])
                        )
                        conn.commit()

                        history_update(cur, conn, "sales", data["id"], "salesid", "Insert", "-", data["id"])
                        history_update(cur, conn, "sales", data["id"], "salespersonid", "Insert", "-", data["salesperson"])
                        history_update(cur, conn, "sales", data["id"], "quantity", "Insert", "-", data["quantity"])
                        history_update(cur, conn, "sales", data["id"], "year", "Insert", "-", data["year"])
                        history_update(cur, conn, "sales", data["id"], "month", "Insert", "-", data["month"])
                        history_update(cur, conn, "sales", data["id"], "sales", "Insert", "-", data["sales"])

                        st.success("✅ New sale record added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_add"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width = True, key = "cancel_sales_add_btn"):
                    st.session_state["confirm_add"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update Sale Record")

        selected_update = st.selectbox("Select Sale to Update", all_data["SalesID"].tolist(), key = "update_sales")
        update_data = get_one_salesdata(cur, 'SalesID', selected_update)
        st.dataframe(update_data)

        with st.form("Update Sales Record"):
            update_salesperson = st.selectbox("Sales Person ID", salesperson,index = salesperson.index(update_data['Sales Person ID'][0]))
            update_quantity = st.number_input("Number of product", value = update_data['Quantity'][0])
            update_year = st.selectbox("Year", year, index = year.index(update_data['Year'][0]))
            update_month = st.selectbox("Month", month, index = month.index(update_data['Month'][0]))
            update_amount = st.number_input("Sales Amount", value = update_data['Sales'][0], min_value = 0)

            update_submitted = st.form_submit_button("Update Sales Record")

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
                if st.button("✅ Confirm Update", use_container_width = True, key = "confirm_sales_update_btn"):
                    try:
                        data = st.session_state["update_sale_data"]
                        current = data["current"]

                        if data["salesperson"] != current['Sales Person ID']:
                            updatedata(cur, conn, 'sales', data["salesid"], 'salespersonid', current['Sales Person ID'], data["salesperson"])

                        if data["quantity"] != current['Quantity']:
                            updatedata(cur, conn, 'sales', data["salesid"], 'quantity', current['Quantity'], data["quantity"])

                        if data["year"] != current['Year']:
                            updatedata(cur, conn, 'sales', data["salesid"], 'year', current['Year'], data["year"])

                        if data["month"] != current['Month']:
                            updatedata(cur, conn, 'sales', data["salesid"], 'month', current['Month'], data["month"])

                        if data["sales"] != current['Sales']:
                            updatedata(cur, conn, 'sales', data["salesid"], 'sales', current['Sales'], data["sales"])

                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_update"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width = True, key = "cancel_sales_update_btn"):
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
                "salesperson": delete_data['Sales Person ID'][0],
                "quantity": delete_data['Quantity'][0],
                "year": delete_data['Year'][0],
                "month": delete_data['Month'][0],
                "sales": delete_data['Sales'][0]
            }
            st.session_state["confirm_delete"] = True

        if st.session_state.get("confirm_delete", False):
            st.warning("⚡ **Confirm Deleting Sale Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Delete", use_container_width = True, key = "confirm_sales_delete_btn"):
                    try:
                        data = st.session_state["delete_sale_data"]

                        cur.execute("DELETE FROM sales WHERE salesid = %s", (data["id"],))
                        conn.commit()

                        history_update(cur, conn, "sales", data["id"], "salesid", "Delete", data["id"], "-")
                        history_update(cur, conn, "sales", data["id"], "salespersonid", "Delete", data["salesperson"], "-")
                        history_update(cur, conn, "sales", data["id"], "quantity", "Delete", data["quantity"], "-")
                        history_update(cur, conn, "sales", data["id"], "year", "Delete", data["year"], "-")
                        history_update(cur, conn, "sales", data["id"], "month", "Delete", data["month"], "-")
                        history_update(cur, conn, "sales", data["id"], "sales", "Delete", data["sales"], "-")

                        st.success("✅ Record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_delete"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Delete", use_container_width = True, key = "cancel_sales_delete_btn"):
                    st.session_state["confirm_delete"] = False
                    st.rerun()