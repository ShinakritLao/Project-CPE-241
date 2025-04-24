import streamlit as st
import pandas as pd
import numpy as np
from HistoryData.restoredata import get_current_data
from HistoryData.restoredata import restore_update
from HistoryData.restoredata import clear_history
# from HistoryData.restoredata import restore_delete

def restoredata_CRUD(cur, conn, changehistory_data):
    st.header("Change History")

    # Load existed data
    st.dataframe(changehistory_data)
    change_id = changehistory_data[changehistory_data['Action'].isin(['Update', 'Delete'])]

    if st.button("Clear history"):
        if len(changehistory_data) != 0:
            try:
                clear_history(cur, conn)
                st.success("Change history cleared successfully!")
            except Exception as e:
                st.error(f"Change history cleared failed: {e}")
        else:
            st.warning("Change history already empty.")

    st.markdown("---")

    # Restore data
    st.subheader("Restore data")

    # Display selected change history record
    selected_restore = st.selectbox("Select change history record", change_id['ChangeID'].tolist())
    selected_data = changehistory_data.loc[changehistory_data['ChangeID'] == selected_restore]
    st.dataframe(selected_data)

    if st.button("Restore"):

        # Set up data
        if len(selected_data) != 0:
            table = selected_data['Table'].values[0]
            loc = selected_data['Location'].values[0]
            subloc = selected_data['SubLocation'].values[0]
            ori_data = selected_data['OriginalData'].values[0]
            changeid = selected_data['ChangeID'].values[0]

            # Get current value from the table
            current_value = get_current_data(cur, table, loc, subloc)

            # Avoid change the same value
            if str(current_value) == str(ori_data):
                st.warning("The new value must be different from the current value.")
            else:
                try:
                    # if selected_data['Action'].values[0] == 'Update':
                        restore_update(cur, conn, table, loc, subloc, current_value, ori_data, changeid)
                    # elif selected_data['Action'].values[0] == 'Delete':

                        st.success("Data restore successfully!")
                except Exception as e:
                    st.error(f"Restore failed: {e}")
        else:
            st.error("Data restore failed.")