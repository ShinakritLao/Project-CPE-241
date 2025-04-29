import streamlit as st
import pandas as pd
import numpy as np
from HistoryData.restoredata import get_current_data
from HistoryData.restoredata import restore_update
from HistoryData.restoredata import clear_history

def restoredata_CRUD(cur, conn, changehistory_data):
    st.header("Change History")

    st.dataframe(changehistory_data)
    change_id = changehistory_data[changehistory_data['Action'].isin(['Update', 'Delete'])]

    # --- CLEAR HISTORY ---
    st.subheader("Clear History")

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

    selected_restore = st.selectbox("Select Change History Record", change_id['ChangeID'].tolist())
    selected_data = changehistory_data.loc[changehistory_data['ChangeID'] == selected_restore]
    st.dataframe(selected_data)

    if st.button("Restore", key="restore_button"):
        if len(selected_data) != 0:
            st.session_state["restore_data"] = {
                "table": selected_data['Table'].values[0],
                "loc": selected_data['Location'].values[0],
                "subloc": selected_data['SubLocation'].values[0],
                "ori_data": selected_data['OriginalData'].values[0],
                "changeid": selected_data['ChangeID'].values[0],
                "action": selected_data['Action'].values[0]
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