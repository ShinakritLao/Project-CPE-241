import streamlit as st
import pandas as pd
import numpy as np

from GetData.kpidata import get_one_kpidata
from DropdownInfo.filtersearch import get_details
from HistoryData.query_data import updatedata
from HistoryData.changehistory_update import history_update

year = [2022, 2023, 2024, 2025]
month = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]

def KPI_CRUD(cur, conn, salesperson, all_data, display_data):
    st.header("KPI Record")

    # # ------------------ FILTER SEARCH ------------------
    col1, col2 = st.columns(2)

    with col1:
        filopt = ["Default", "Sales Person ID", "Year"]
        filters = st.selectbox("Filter Search", filopt, index = 0)

        if filters == 'Sales Person ID':
            filters = "SalesPersonID"

    with col2:
        if filters == 'Default':
            st.selectbox("Select Details", options=[], disabled=True, key="default_disabled_select")
            displaying = display_data
        else:
            details = get_details(cur, 'KPI', filters)
            selected_details = st.selectbox("Select Details", details, index=0, key="filter_details_select")
            displaying = get_one_kpidata(cur, filters, selected_details)

    # ------------------ DISPLAY DATA & SET UP ------------------
    st.dataframe(displaying)
    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # ------------------ ADD RECORD ------------------
    with add_record:
        if len(all_data) == 0:
            new_value = "K001"
        else:
            last_value = all_data['KPI_ID'].iloc[-1]
            prefix = ''.join(filter(str.isalpha, last_value))
            number = ''.join(filter(str.isdigit, last_value))
            new_number = str(int(number) + 1).zfill(len(number))
            new_value = prefix + new_number

        st.subheader("Add New KPI Record")

        with st.form("Add KPI Record"):
            new_id = st.text_input("KPI ID", value = new_value, disabled = True)
            insert_salesperson = st.selectbox("Sales Person ID", salesperson)
            new_year = st.selectbox("Year", year, index = 3)
            new_targetq = st.number_input("Target Quotation", min_value = 0)
            new_quotation = st.number_input("Quotation", min_value=0)
            new_targetso = st.number_input("Target Sales Order", min_value=0)
            new_salesorder = st.number_input("Sales Order", min_value=0)
            new_allcustomer = st.number_input("All Customer", min_value=0)
            new_customerinhand = st.number_input("Customer in Hand", min_value=0)
            submitted = st.form_submit_button("Add KPI")

            if submitted:
                st.session_state["new_kpi_data"] = {
                    "id": new_id,
                    "salesperson": insert_salesperson,
                    "year": new_year,
                    "targetq": new_targetq,
                    "quotation": new_quotation,
                    "targetso": new_targetso,
                    "salesorder": new_salesorder,
                    "allcustomer": new_allcustomer,
                    "customerinhand": new_customerinhand
                }
                st.session_state["confirm_add"] = True

        if st.session_state.get("confirm_add", False):
            st.warning("⚡ **Confirm Adding New KPI Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Add", use_container_width = True, key = "confirm_kpi_add_btn"):
                    try:
                        data = st.session_state["new_kpi_data"]
                        cur.execute(
                            "INSERT INTO kpi (kpi_id, salespersonid, year, targetq, quotation, targetso, salesorder, allcustomer, customerinhand) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (data["id"], data["salesperson"], data["year"], data["targetq"], data["quotation"], data["targetso"], data["salesorder"], data["allcustomer"], data["customerinhand"])
                        )
                        conn.commit()

                        history_update(cur, conn, "kpi", data["id"], "kpi_id", "Insert", "-", data["id"])
                        history_update(cur, conn, "kpi", data["id"], "salespersonid", "Insert", "-", data["salesperson"])
                        history_update(cur, conn, "kpi", data["id"], "year", "Insert", "-", data["year"])
                        history_update(cur, conn, "kpi", data["id"], "targetq", "Insert", "-", data["targetq"])
                        history_update(cur, conn, "kpi", data["id"], "quotation", "Insert", "-", data["quotation"])
                        history_update(cur, conn, "kpi", data["id"], "targetso", "Insert", "-", data["targetso"])
                        history_update(cur, conn, "kpi", data["id"], "salesorder", "Insert", "-", data["salesorder"])
                        history_update(cur, conn, "kpi", data["id"], "allcustomer", "Insert", "-", data["allcustomer"])
                        history_update(cur, conn, "kpi", data["id"], "customerinhand", "Insert", "-", data["customerinhand"])

                        st.success("✅ New KPI record added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_add"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width = True, key = "cancel_kpi_add_btn"):
                    st.session_state["confirm_add"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update KPI Record")

        selected_update = st.selectbox("Select KPI to Update", all_data["KPI_ID"].tolist(), key = "update_kpi")
        update_data = get_one_kpidata(cur, 'KPI_ID', selected_update)
        st.dataframe(update_data)

        with st.form("Update KPI Record"):
            update_salesperson = st.selectbox("Sales Person ID", salesperson,
                                              index = salesperson.index(update_data['Sales Person ID'][0]))
            update_year = st.selectbox("Year", year, index = year.index(update_data['Year'][0]))
            update_targetq = st.number_input("Target Quotation", value = update_data['Target Quotation'][0], min_value = 0)
            update_quotation = st.number_input("Quotation", value=update_data['Quotation'][0], min_value=0)
            update_targetso = st.number_input("Target Sales Order", value=update_data['Target Sales Order'][0], min_value=0)
            update_salesorder = st.number_input("Sales Order", value=update_data['Sales Order'][0], min_value=0)
            update_allcustomer = st.number_input("All Customer", value=update_data['All Customer'][0], min_value=0)
            update_customerinhand = st.number_input("Customer in Hand", value=update_data['Customer in Hand'][0], min_value=0)

            update_submitted = st.form_submit_button("Update Record")

            if update_submitted:
                st.session_state["update_kpi_data"] = {
                    "kpi_id": selected_update,
                    "salesperson": update_salesperson,
                    "year": update_year,
                    "targetq": update_targetq,
                    "quotation": update_quotation,
                    "targetso": update_targetso,
                    "salesorder": update_salesorder,
                    "allcustomer": update_allcustomer,
                    "customerinhand": update_customerinhand,
                    "current": update_data.iloc[0]
                }
                st.session_state["confirm_update"] = True

        if st.session_state.get("confirm_update", False):
            st.warning("⚡ **Confirm Updating KPI Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Update", use_container_width = True, key = "confirm_kpi_update_btn"):
                    try:
                        data = st.session_state["update_kpi_data"]
                        current = data["current"]

                        if data["salesperson"] != current['Sales Person ID']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'salespersonid', current['Sales Person ID'], data["salesperson"])

                        if data["year"] != current['Year']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'year', current['Year'], data["year"])

                        if data["targetq"] != current['Target Quotation']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'targetq', current['Target Quotation'], data["targetq"])

                        if data["quotation"] != current['Quotation']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'quotation', current['Quotation'], data["quotation"])
                        if data["targetso"] != current['Target Sales Order']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'targetso', current['Target Sales Order'], data["targetso"])

                        if data["salesorder"] != current['Sales Order']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'salesorder', current['Sales Order'], data["salesorder"])

                        if data["allcustomer"] != current['All Customer']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'allcustomer', current['All Customer'], data["allcustomer"])

                        if data["customerinhand"] != current['Customer in Hand']:
                            updatedata(cur, conn, 'kpi', data["kpi_id"], 'customerinhand', current['Customer in Hand'], data["customerinhand"])

                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_update"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width = True, key = "cancel_kpi_update_btn"):
                    st.session_state["confirm_update"] = False
                    st.rerun()

    # ------------------ DELETE RECORD ------------------
    with delete_record:
        st.subheader("Delete KPI Record")

        selected_delete = st.selectbox("Select KPI to Delete", all_data["KPI_ID"].tolist(), key="delete_kpi")
        delete_data = get_one_kpidata(cur, 'KPI_ID', selected_delete)
        st.dataframe(delete_data)

        if st.button("Delete Record", key = "delete_kpi_btn"):
            st.session_state["delete_kpi_data"] = {
                "id": selected_delete,
                "salesperson": delete_data['Sales Person ID'][0],
                "year": delete_data['Year'][0],
                "targetq": delete_data['Target Quotation'][0],
                "quotation": delete_data['Quotation'][0],
                "targetso": delete_data['Target Sales Order'][0],
                "salesorder": delete_data['Sales Order'][0],
                "allcustomer": delete_data['All Customer'][0],
                "customerinhand": delete_data['Customer in Hand'][0]
            }
            st.session_state["confirm_delete"] = True

        if st.session_state.get("confirm_delete", False):
            st.warning("⚡ **Confirm Deleting KPI Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Delete", use_container_width = True, key = "confirm_kpi_delete_btn"):
                    try:
                        data = st.session_state["delete_kpi_data"]

                        cur.execute("DELETE FROM kpi WHERE kpi_id = %s", (data["id"],))
                        conn.commit()

                        history_update(cur, conn, "kpi", data["id"], "kpi_id", "Delete", data["id"], "-")
                        history_update(cur, conn, "kpi", data["id"], "salespersonid", "Delete", data["salesperson"], "-")
                        history_update(cur, conn, "kpi", data["id"], "year", "Delete", data["year"], "-")
                        history_update(cur, conn, "kpi", data["id"], "targetq", "Delete", data["targetq"], "-")
                        history_update(cur, conn, "kpi", data["id"], "quotation", "Delete", data["quotation"], "-")
                        history_update(cur, conn, "kpi", data["id"], "targetso", "Delete",
                                       data["targetso"], "-")
                        history_update(cur, conn, "kpi", data["id"], "salesorder", "Delete", data["salesorder"], "-")
                        history_update(cur, conn, "kpi", data["id"], "allcustomer", "Delete", data["allcustomer"], "-")
                        history_update(cur, conn, "kpi", data["id"], "customerinhand", "Delete",
                                       data["customerinhand"], "-")

                        st.success("✅ Record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_delete"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Delete", use_container_width = True, key = "cancel_kpi_delete_btn"):
                    st.session_state["confirm_delete"] = False
                    st.rerun()