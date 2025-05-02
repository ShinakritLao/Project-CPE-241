import streamlit as st
import pandas as pd
import numpy as np

from GetData.debtordata import get_one_debtordata
from DropdownInfo.filtersearch import get_details
from HistoryData.query_data import updatedata
from HistoryData.changehistory_update import history_update

def Debtor_CRUD(cur, conn, salesperson, product_list, all_data, display_data):
    st.header("Debtor Record")

    # ------------------ FILTER SEARCH ------------------
    col1, col2 = st.columns(2)

    with col1:
        filopt = ["Default", "CompanyName", "Status"]
        filters = st.selectbox("Filter Search", filopt, index = 0)

    with col2:
        if filters == 'Default':
            st.selectbox("Select Details", options=[], disabled=True, key="Detail_debt")
            displaying = display_data
        else:
            details = get_details(cur, 'Debtor', filters)
            selected_details = st.selectbox("Select Details", details, index=0, key="filter_details_select")
            displaying = get_one_debtordata(cur, filters, selected_details)

    # ------------------ DISPLAY DATA & SET UP ------------------
    st.dataframe(displaying)
    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # ------------------ ADD RECORD ------------------
    with add_record:
        if len(all_data) == 0:
            new_value = "D001"
        else:
            last_value = all_data['DebtorID'].iloc[-1]
            prefix = ''.join(filter(str.isalpha, last_value))
            number = ''.join(filter(str.isdigit, last_value))
            new_number = str(int(number) + 1).zfill(len(number))
            new_value = prefix + new_number

        st.subheader("Add New Debtor Record")

        with st.form("Add Debtor Record"):
            new_id = st.text_input("Debtor ID", value = new_value, disabled = True)
            new_companyname = st.text_input("Company Name")
            new_salespersonid = st.selectbox("Salesperson ID", salesperson)
            new_productid = st.selectbox("Product ID", product_list)
            new_price = st.number_input("Price", min_value = 0.0)
            new_debt = st.number_input("Debt", min_value = 0.0)
            new_paid = st.number_input("Paid", min_value = 0.0)
            new_date = st.date_input("Date")
            new_status = st.selectbox("Status", ["Paid", "Unpaid", "Partially Paid"])

            submitted = st.form_submit_button("Add Debtor")

            if submitted:
                st.session_state["new_debtor_data"] = {
                    "id": new_id,
                    "companyname": new_companyname,
                    "salespersonid": new_salespersonid,
                    "productid": new_productid,
                    "price": new_price,
                    "debt": new_debt,
                    "paid": new_paid,
                    "date": new_date,
                    "status": new_status
                }
                st.session_state["confirm_add"] = True

        if st.session_state.get("confirm_add", False):
            st.warning("⚡ **Confirm Adding New Debtor Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Add", use_container_width = True, key = "confirm_debtor_add_btn"):
                    try:
                        data = st.session_state["new_debtor_data"]
                        cur.execute(
                            "INSERT INTO debtor (debtorid, companyname, salespersonid, productid, price, debt, paid, date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (data["id"], data["companyname"], data["salespersonid"], data["productid"], data["price"], data["debt"], data["paid"], data["date"], data["status"])
                        )
                        conn.commit()

                        history_update(cur, conn, "debtor", data["id"], "debtorid", "Insert", "-", data["id"])
                        history_update(cur, conn, "debtor", data["id"], "companyname", "Insert", "-", data["companyname"])
                        history_update(cur, conn, "debtor", data["id"], "salespersonid", "Insert", "-", data["salespersonid"])
                        history_update(cur, conn, "debtor", data["id"], "productid", "Insert", "-", data["productid"])
                        history_update(cur, conn, "debtor", data["id"], "price", "Insert", "-", data["price"])
                        history_update(cur, conn, "debtor", data["id"], "debt", "Insert", "-", data["debt"])
                        history_update(cur, conn, "debtor", data["id"], "paid", "Insert", "-", data["paid"])
                        history_update(cur, conn, "debtor", data["id"], "date", "Insert", "-", data["date"])
                        history_update(cur, conn, "debtor", data["id"], "status", "Insert", "-", data["status"])

                        st.success("✅ New Debtor record added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_add"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width = True, key = "cancel_debtor_add_btn"):
                    st.session_state["confirm_add"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update Debtor Record")

        selected_update = st.selectbox("Select Debtor to Update", all_data["DebtorID"].tolist(), key = "update_debtor")
        update_data = get_one_debtordata(cur, 'DebtorID', selected_update)
        st.dataframe(update_data)

        with st.form("Update Debtor Record"):
            update_companyname = st.text_input("Company Name", value=update_data['Company Name'][0])
            update_salesperson = st.selectbox("Sales Person ID", salesperson,index=salesperson.index(update_data['Sales Person ID'][0]))
            update_productid = st.selectbox("Product ID", product_list,index = product_list.index(update_data['Product ID'][0]))
            update_price = st.number_input("Price", value=update_data['Price'][0], min_value = 0)
            update_debt = st.number_input("Debt", value=update_data['Debt'][0], min_value=0)
            update_paid = st.number_input("Paid", value=update_data['Paid'][0], min_value=0)
            update_date = st.date_input("Date", value=update_data['Date'][0])
            update_status = st.selectbox("Status", ["Paid", "Unpaid", "Partially Paid"], index=["Paid", "Unpaid", "Partially Paid"].index(update_data['Status'][0]))

            update_submitted = st.form_submit_button("Update Record")

            if update_submitted:
                st.session_state["update_debtor_data"] = {
                    "debtorid": selected_update,
                    "companyname": update_companyname,
                    "salespersonid": update_salesperson,
                    "productid": update_productid,
                    "price": update_price,
                    "debt": update_debt,
                    "paid": update_paid,
                    "date": update_date,
                    "status": update_status,
                    "current": update_data.iloc[0]
                }
                st.session_state["confirm_update"] = True

        if st.session_state.get("confirm_update", False):
            st.warning("⚡ **Confirm Updating Debtor Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Update", use_container_width = True, key = "confirm_debtor_update_btn"):
                    try:
                        data = st.session_state["update_debtor_data"]
                        current = data["current"]

                        if data["companyname"] != current['Company Name']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'companyname', current['Company Name'], data["companyname"])

                        if data["salespersonid"] != current['Sales Person ID']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'salespersonid', current['Sales Person ID'], data["salespersonid"])

                        if data["productid"] != current['Product ID']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'productid', current['Product ID'], data["productid"])

                        if data["price"] != current['Price']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'price', current['Price'], data["price"])

                        if data["debt"] != current['Debt']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'debt', current['Debt'], data["debt"])

                        if data["paid"] != current['Paid']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'paid', current['Paid'], data["paid"])

                        if data["date"] != current['Date']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'date', current['Date'], data["date"])

                        if data["status"] != current['Status']:
                            updatedata(cur, conn, 'debtor', data["debtorid"], 'status', current['Status'], data["status"])

                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_update"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width = True, key = "cancel_debtor_update_btn"):
                    st.session_state["confirm_update"] = False
                    st.rerun()

    # ------------------ DELETE RECORD ------------------
    with delete_record:
        st.subheader("Delete Debtor Record")

        selected_delete = st.selectbox("Select Debtor to Delete", all_data["DebtorID"].tolist(), key="delete_debtor")
        delete_data = get_one_debtordata(cur, 'DebtorID', selected_delete)
        st.dataframe(delete_data)

        if st.button("Delete Record", key = "delete_debtor_btn"):
            st.session_state["delete_debtor_data"] = {
                "id": selected_delete,
                "companyname": delete_data['Company Name'][0],
                "salespersonid": delete_data['Sales Person ID'][0],
                "productid": delete_data['Product ID'][0],
                "price": delete_data['Price'][0],
                "debt": delete_data['Debt'][0],
                "paid": delete_data['Paid'][0],
                "date": delete_data['Date'][0],
                "status": delete_data['Status'][0]
            }
            st.session_state["confirm_delete"] = True

        if st.session_state.get("confirm_delete", False):
            st.warning("⚡ **Confirm Deleting Debtor Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Delete", use_container_width = True, key = "confirm_debtor_delete_btn"):
                    try:
                        data = st.session_state["delete_debtor_data"]

                        cur.execute("DELETE FROM debtor WHERE debtorid = %s", (data["id"],))
                        conn.commit()

                        history_update(cur, conn, "debtor", data["id"], "debtorid", "Delete",  data["id"], "-")
                        history_update(cur, conn, "debtor", data["id"], "companyname", "Delete",  data["companyname"], "-")
                        history_update(cur, conn, "debtor", data["id"], "salespersonid", "Delete",  data["salespersonid"], "-")
                        history_update(cur, conn, "debtor", data["id"], "productid", "Delete",  data["productid"], "-")
                        history_update(cur, conn, "debtor", data["id"], "price", "Delete",  data["price"], "-")
                        history_update(cur, conn, "debtor", data["id"], "debt", "Delete",  data["debt"], "-")
                        history_update(cur, conn, "debtor", data["id"], "paid", "Delete",  data["paid"], "-")
                        history_update(cur, conn, "debtor", data["id"], "date", "Delete",  data["date"], "-")
                        history_update(cur, conn, "debtor", data["id"], "status", "Delete", data["status"], "-")

                        st.success("✅ Debtor record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_delete"] = False
                        st.rerun()

            with col1:
                if st.button("❌ Cancel Delete", use_container_width = True, key = "cancel_debtor_delete_btn"):
                    st.session_state["confirm_delete"] = False
                    st.rerun()
