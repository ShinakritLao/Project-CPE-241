import streamlit as st
import pandas as pd
import numpy as np

from GetData.changehistorydata import get_one_historydata
from DropdownInfo.filtersearch import get_details
from DropdownInfo.filtersearch import get_restore
from HistoryData.query_data import updatedata

from HistoryData.restoredata import get_current_data
from HistoryData.restoredata import restore_update
from HistoryData.restoredata import clear_history

def restoredata_CRUD(cur, conn, changehistory_data):
    st.header("History")

    # ------------------ FILTER SEARCH ------------------
    col1, col2 = st.columns(2)

    with col1:
        filopt = ["Default", "Username", "Selected_Table", "Action"]
        filters = st.selectbox("Filter Search", filopt, index = 0)

    with col2:
        if filters == 'Default':
            st.selectbox("Select Details", options = [], disabled = True, key = 'filters_history')
            displaying = changehistory_data
        else:
            details = get_details(cur, 'History_Change', filters)
            selected_details = st.selectbox("", details, index = 0, key = 'details_history')
            displaying = get_one_historydata(cur, filters, selected_details)

    # ------------------ DISPLAY DATA ------------------
    st.dataframe(displaying)

    # ------------------ CLEAR HISTORY ------------------
    if st.button("Clear history", key="clear_history_button"):
        if len(changehistory_data) != 0:
            st.session_state["confirm_clear"] = True
        else:
            st.warning("⚡ History is already empty.")

    if st.session_state.get("confirm_clear", False):
        st.warning("⚡ **Confirm clearing all change history?**")
        col1, col2 = st.columns(2)
        with col2:
            if st.button("✅ Confirm Clear", use_container_width=True, key="confirm_clear_btn"):
                try:
                    clear_history(cur, conn)
                    st.success("✅ Change history cleared successfully!")
                except Exception as e:
                    st.error(f"❌ Clear history failed: {e}")
                finally:
                    st.session_state["confirm_clear"] = False
                    st.rerun()
        with col1:
            if st.button("❌ Cancel Clear", use_container_width=True, key="cancel_clear_btn"):
                st.session_state["confirm_clear"] = False
                st.rerun()

    st.markdown("---")

    # --- RESTORE DATA ---
    st.subheader("Restore Data")

    restoreopt = get_restore(cur)
    selected_restore = st.selectbox("Select History Record", restoreopt, key = 'restore_btn')
    restore_data = get_one_historydata(cur, 'ChangeID', selected_restore)
    st.dataframe(restore_data)

    if st.button("Restore", key="restore_button"):
        if len(restore_data) != 0:
            st.session_state["restore_data"] = {
                "table": restore_data['Table'][0],
                "loc": restore_data['Location'][0],
                "subloc": restore_data['SubLocation'][0],
                "ori_data": restore_data['OriginalData'][0],
                "changeid": restore_data['ChangeID'][0],
                "action": restore_data['Action'][0]
            }
            st.session_state["confirm_restore"] = True
        else:
            st.error("❌ No data selected for restore.")

    if st.session_state.get("confirm_restore", False):
        st.warning("⚡ **Confirm restoring the selected record?**")
        col1, col2 = st.columns(2)
        with col2:
            if st.button("✅ Confirm Restore", use_container_width=True, key="confirm_restore_btn"):
                try:
                    data = st.session_state["restore_data"]
                    current_value = get_current_data(cur, data["table"], data["loc"], data["subloc"])

                    if str(current_value) == str(data["ori_data"]):
                        st.warning("⚡ The original data is the same as the current value. No changes made.")
                    else:
                        restore_update(cur, conn, data["table"], data["loc"], data["subloc"], current_value, data["ori_data"], data["changeid"])
                        st.success("✅ Data restored successfully!")
                except Exception as e:
                    st.error(f"❌ Restore failed: {e}")
                finally:
                    st.session_state["confirm_restore"] = False
                    st.rerun()
        with col1:
            if st.button("❌ Cancel Restore", use_container_width=True, key="cancel_restore_btn"):
                st.session_state["confirm_restore"] = False
                st.rerun()