import streamlit as st
import pandas as pd
import numpy as np
from HistoryData.changehistory_update import history_update

year = [2022, 2023, 2024, 2025]
month = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]

def Sales_CRUD(cur, conn, salesperson, all_sales_data, display_data):
    st.header("Sales Record")

    st.dataframe(display_data)

    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # ------------------ ADD RECORD ------------------
    with add_record:
        if len(all_sales_data) == 0:
            new_value = "S001"
        else:
            last_value = all_sales_data['SalesID'].iloc[-1]
            prefix = ''.join(filter(str.isalpha, last_value))
            number = ''.join(filter(str.isdigit, last_value))
            new_number = str(int(number) + 1).zfill(len(number))
            new_value = prefix + new_number

        st.subheader("Add New Sale Record")

        with st.form("Add Record"):
            new_sale_id = st.text_input("Sales ID", value=new_value, disabled=True)
            insert_salesperson = st.selectbox("Sales Person ID", salesperson)
            new_quantity = st.number_input("Number of product")
            new_year = st.selectbox("Year", year, index=3)
            new_month = st.selectbox("Month", month, index=3)
            new_amount = st.number_input("Sales Amount", min_value=0)
            submitted = st.form_submit_button("Add Sale")

            if submitted:
                st.session_state["new_sale_data"] = {
                    "id": new_sale_id,
                    "salesperson": insert_salesperson,
                    "quantity": new_quantity,
                    "year": new_year,
                    "month": new_month,
                    "amount": new_amount
                }
                st.session_state["confirm_add"] = True

        if st.session_state.get("confirm_add", False):
            st.warning("⚡ **Confirm Adding New Sale Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Add", use_container_width=True, key="confirm_add_btn"):
                    try:
                        data = st.session_state["new_sale_data"]
                        cur.execute(
                            "INSERT INTO sales (salesid, salespersonid, quantity, year, month, sales) VALUES (%s, %s, %s, %s, %s, %s)",
                            (data["id"], data["salesperson"], data["quantity"], data["year"], data["month"], data["amount"])
                        )
                        conn.commit()

                        history_update(cur, conn, "Sales", data["id"], "SalesID", "Insert", "-", data["id"])
                        history_update(cur, conn, "Sales", data["id"], "SalesPersonID", "Insert", "-", data["salesperson"])
                        history_update(cur, conn, "Sales", data["id"], "Quantity", "Insert", "-", data["quantity"])
                        history_update(cur, conn, "Sales", data["id"], "Year", "Insert", "-", data["year"])
                        history_update(cur, conn, "Sales", data["id"], "Month", "Insert", "-", data["month"])
                        history_update(cur, conn, "Sales", data["id"], "Sales", "Insert", "-", data["amount"])

                        st.success("✅ New sale record added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                    finally:
                        st.session_state["confirm_add"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width=True, key="cancel_add_btn"):
                    st.session_state["confirm_add"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update Sale Record")

        selected_update_data = st.selectbox("Select Sale to Update", all_sales_data["SalesID"].tolist(), key="update_selectbox")
        current_data = all_sales_data.loc[all_sales_data['SalesID'] == selected_update_data]
        st.dataframe(display_data.loc[display_data['Sales ID'] == selected_update_data])

        with st.form("Update Record"):
            update_salesperson = st.selectbox("Sales Person ID", salesperson, index=salesperson.index(current_data['SalesPersonID'].values[0]))
            update_quantity = st.number_input("Number of product", value=current_data['Quantity'].values[0])
            update_year = st.selectbox("Year", year, index=year.index(current_data['Year'].values[0]))
            update_month = st.selectbox("Month", month, index=month.index(current_data['Month'].values[0]))
            update_amount = st.number_input("Sales Amount", value=current_data['Sales'].values[0], min_value=0)

            update_submitted = st.form_submit_button("Update Record")

            if update_submitted:
                st.session_state["update_sale_data"] = {
                    "salesid": selected_update_data,
                    "salesperson": update_salesperson,
                    "quantity": update_quantity,
                    "year": update_year,
                    "month": update_month,
                    "sales": update_amount,
                    "current": current_data.iloc[0]
                }
                st.session_state["confirm_update"] = True

        if st.session_state.get("confirm_update", False):
            st.warning("⚡ **Confirm Updating Sale Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Update", use_container_width=True, key="confirm_update_btn"):
                    try:
                        data = st.session_state["update_sale_data"]
                        current = data["current"]

                        if data["salesperson"] != current['SalesPersonID']:
                            cur.execute("UPDATE sales SET salespersonid = %s WHERE salesid = %s", (data["salesperson"], data["salesid"]))
                            history_update(cur, conn, "Sales", data["salesid"], "SalesPersonID", "Update", current['SalesPersonID'], data["salesperson"])

                        if data["quantity"] != current['Quantity']:
                            cur.execute("UPDATE sales SET quantity = %s WHERE salesid = %s", (data["quantity"], data["salesid"]))
                            history_update(cur, conn, "Sales", data["salesid"], "Quantity", "Update", current['Quantity'], data["quantity"])

                        if data["year"] != current['Year']:
                            cur.execute("UPDATE sales SET year = %s WHERE salesid = %s", (data["year"], data["salesid"]))
                            history_update(cur, conn, "Sales", data["salesid"], "Year", "Update", current['Year'], data["year"])

                        if data["month"] != current['Month']:
                            cur.execute("UPDATE sales SET month = %s WHERE salesid = %s", (data["month"], data["salesid"]))
                            history_update(cur, conn, "Sales", data["salesid"], "Month", "Update", current['Month'], data["month"])

                        if data["sales"] != current['Sales']:
                            cur.execute("UPDATE sales SET sales = %s WHERE salesid = %s", (data["sales"], data["salesid"]))
                            history_update(cur, conn, "Sales", data["salesid"], "Sales", "Update", current['Sales'], data["sales"])

                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                    finally:
                        st.session_state["confirm_update"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width=True, key="cancel_update_btn"):
                    st.session_state["confirm_update"] = False
                    st.rerun()

    # ------------------ DELETE RECORD ------------------
    with delete_record:
        st.subheader("Delete Sale Record")

        selected_delete_data = st.selectbox("Select Sale to Delete", all_sales_data["SalesID"].tolist(), key="delete_selectbox")
        st.dataframe(display_data.loc[display_data['Sales ID'] == selected_delete_data])

        if st.button("Delete Record", key="delete_btn"):
            st.session_state["delete_sale_id"] = selected_delete_data
            st.session_state["confirm_delete"] = True

        if st.session_state.get("confirm_delete", False):
            st.warning("⚡ **Confirm Deleting Sale Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Delete", use_container_width=True, key="confirm_delete_btn"):
                    try:
                        cur.execute("DELETE FROM sales WHERE salesid = %s", (st.session_state["delete_sale_id"],))
                        history_update(cur, conn, "Sales", st.session_state["delete_sale_id"], "-", "Delete", "-", "-")
                        conn.commit()
                        st.warning("✅ Record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                    finally:
                        st.session_state["confirm_delete"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_delete_btn"):
                    st.session_state["confirm_delete"] = False
                    st.rerun()
