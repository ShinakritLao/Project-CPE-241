import streamlit as st
import pandas as pd
import numpy as np

from GetData.salesproductdata import get_one_salesproductdata
from DropdownInfo.filtersearch import get_details
from HistoryData.query_data import updatedata
from HistoryData.changehistory_update import history_update

def SalesProduct_CRUD(cur, conn, salesperson, all_data, display_data):
    st.header("Sales Product Record")

    # ------------------ FILTER SEARCH ------------------
    col1, col2 = st.columns(2)

    with col1:
        filopt = ["Default", "Status"]
        filters = st.selectbox("Filter Search", filopt, index=0, key='Filter_SalesProduct')

    with col2:
        if filters == 'Default':
            st.selectbox("Select Details", options=[], disabled=True, key='Details_SalesProduct')
            displaying = display_data
        else:
            details = get_details(cur, 'SalesProduct', filters)
            selected_details = st.selectbox("Select Details", details, index=0)
            displaying = get_one_salesproductdata(cur, filters, selected_details)

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

        st.subheader("Add New Sales Product Record")

        with st.form("Add Sales Product Record"):
            new_id = st.text_input("Sales ID", value=new_value, disabled=True)
            product_id = st.selectbox("Product ID", salesperson)
            total_sales = st.number_input("Total Sales", min_value=0)
            total_cost = st.number_input("Total Cost", min_value=0)
            status = st.selectbox("Status", ["cancelled", "completed", "pending"])
            submitted = st.form_submit_button("Add Sales Product")

            if submitted:
                st.session_state["new_salesproduct_data"] = {
                    "id": new_id,
                    "product_id": product_id,
                    "total_sales": total_sales,
                    "total_cost": total_cost,
                    "status": status
                }
                st.session_state["confirm_add_sp"] = True

        if st.session_state.get("confirm_add_sp", False):
            st.warning("⚡ **Confirm Adding New Sales Product Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Add", use_container_width=True, key="confirm_spo_add_btn"):
                    try:
                        data = st.session_state["new_salesproduct_data"]
                        cur.execute(
                            "INSERT INTO salesproduct (salesid, productid, totalsales, totalcost, status) VALUES (%s, %s, %s, %s, %s)",
                            (data["id"], data["product_id"], data["total_sales"], data["total_cost"], data["status"])
                        )
                        conn.commit()

                        history_update(cur, conn, "salesproduct", data["id"], "salesid", "Insert", "-", data["id"])
                        history_update(cur, conn, "salesproduct", data["id"], "productid", "Insert", "-", data["product_id"])
                        history_update(cur, conn, "salesproduct", data["id"], "totalsales", "Insert", "-", data["total_sales"])
                        history_update(cur, conn, "salesproduct", data["id"], "totalcost", "Insert", "-", data["total_cost"])
                        history_update(cur, conn, "salesproduct", data["id"], "status", "Insert", "-", data["status"])

                        st.success("✅ New sales product record added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_add_sp"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width=True, key="cancel_spo_add_btn"):
                    st.session_state["confirm_add_sp"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update Sales Product Record")

        selected_update = st.selectbox("Select Sales Product to Update", all_data["SalesID"].tolist(),
                                       key="update_salesproduct")
        update_data = get_one_salesproductdata(cur, 'SalesID', selected_update)
        st.dataframe(update_data)

        with st.form("Update Sales Product Record"):
            product_id = update_data['Product ID'][0]

            if product_id not in salesperson:
                product_id = salesperson[0]

            product_id = st.selectbox("Product ID", salesperson, index=salesperson.index(product_id))
            total_sales = st.number_input("Total Sales", value=update_data['Total Sales'][0])
            total_cost = st.number_input("Total Cost", value=update_data['Total Cost'][0])
            status = st.selectbox("Status", ["cancelled", "pending", "completed"],
                                  index=["cancelled", "pending", "completed"].index(update_data['Status'][0]))

            update_submitted = st.form_submit_button("Update Sales Product Record")

            if update_submitted:
                st.session_state["update_salesproduct_data"] = {
                    "salesid": selected_update,
                    "product_id": product_id,
                    "total_sales": total_sales,
                    "total_cost": total_cost,
                    "status": status,
                    "current": update_data.iloc[0]
                }
                st.session_state["confirm_update_sp"] = True

        if st.session_state.get("confirm_update_sp", False):
            st.warning("⚡ **Confirm Updating Sales Product Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Update", use_container_width=True, key="confirm_sp_update_btn"):
                    try:
                        data = st.session_state["update_salesproduct_data"]
                        current = data["current"]

                        if data["product_id"] != current['Product ID']:
                            updatedata(cur, conn, 'salesproduct', data["salesid"], 'productid', current['Product ID'], data["product_id"])
                        if data["total_sales"] != current['Total Sales']:
                            updatedata(cur, conn, 'salesproduct', data["salesid"], 'totalsales', current['Total Sales'], data["total_sales"])
                        if data["total_cost"] != current['Total Cost']:
                            updatedata(cur, conn, 'salesproduct', data["salesid"], 'totalcost', current['Total Cost'], data["total_cost"])
                        if data["status"] != current['Status']:
                            updatedata(cur, conn, 'salesproduct', data["salesid"], 'status', current['Status'], data["status"])

                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_update_sp"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width=True, key="cancel_sp_update_btn"):
                    st.session_state["confirm_update_sp"] = False
                    st.rerun()

    # ------------------ DELETE RECORD ------------------
    with delete_record:
        st.subheader("Delete Sales Product Record")

        selected_delete = st.selectbox("Select Sales Product to Delete", all_data["SalesID"].tolist(), key="delete_salesproduct")
        delete_data = get_one_salesproductdata(cur, 'SalesID', selected_delete)
        st.dataframe(delete_data)

        if st.button("Delete Record", key="delete_sp_btn"):
            st.session_state["delete_salesproduct_data"] = {
                "id": selected_delete,
                "product_id": delete_data['Product ID'][0],
                "total_sales": delete_data['Total Sales'][0],
                "total_cost": delete_data['Total Cost'][0],
                "status": delete_data['Status'][0]
            }
            st.session_state["confirm_delete_sp"] = True

        if st.session_state.get("confirm_delete_sp", False):
            st.warning("⚡ **Confirm Deleting Sales Product Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Delete", use_container_width=True, key="confirm_sp_delete_btn"):
                    try:
                        data = st.session_state["delete_salesproduct_data"]

                        cur.execute("DELETE FROM salesproduct WHERE salesid = %s", (data["id"],))
                        conn.commit()

                        history_update(cur, conn, "salesproduct", data["id"], "salesid", "Delete", data["id"], "-")
                        history_update(cur, conn, "salesproduct", data["id"], "productid", "Delete", data["product_id"], "-")
                        history_update(cur, conn, "salesproduct", data["id"], "totalsales", "Delete", data["total_sales"], "-")
                        history_update(cur, conn, "salesproduct", data["id"], "totalcost", "Delete", data["total_cost"], "-")
                        history_update(cur, conn, "salesproduct", data["id"], "status", "Delete", data["status"], "-")

                        st.success("✅ Record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_delete_sp"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_sp_delete_btn"):
                    st.session_state["confirm_delete_sp"] = False
                    st.rerun()
