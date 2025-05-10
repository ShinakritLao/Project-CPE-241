import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

from GetData.salespersondata import get_salespersondata
from GetData.salespersondata import get_one_salespersondata
from DropdownInfo.filtersearch import get_details
from HistoryData.query_data import updatedata
from HistoryData.changehistory_update import history_update

def SalesPerson_CRUD(cur, conn, all_data, display_data):
    st.header("Sales Person Record")

    # ------------------ FILTER SEARCH ------------------
    col1, col2 = st.columns(2)

    with col1:
        filopt = ["Default", "Gender", "Position"]
        filters = st.selectbox("Filter Search", filopt, index=0, key='Filter_SalesPerson')

    with col2:
        if filters == 'Default':
            st.selectbox("Select Details", options=[], disabled=True, key='Details_SalesPerson')
            displaying = display_data
        else:
             details = get_details(cur, 'SalesPerson', filters)
             selected_details = st.selectbox("Select Details", details, index=0, key="filter_details_salesperson")
             displaying = get_one_salespersondata(cur, filters, selected_details)

    # ------------------ DISPLAY DATA & SET UP ------------------
    st.dataframe(displaying)
    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # ------------------ ADD RECORD ------------------
    with add_record:
        if len(all_data) == 0:
            new_value = "SP001"
        else:
            last_value = all_data['SalesPersonID'].iloc[-1]
            prefix = ''.join(filter(str.isalpha, last_value))
            number = ''.join(filter(str.isdigit, last_value))
            new_number = str(int(number) + 1).zfill(len(number))
            new_value = prefix + new_number

        st.subheader("Add New Sales Person Record")

        with st.form("Add Sales Person Record"):
            new_id = st.text_input("Sales Person ID", value=new_value, disabled=True)
            sales_name = st.text_input("Sales Name")
            dob = st.date_input("Date of Birth", min_value = date(1970, 1, 1), max_value = date(2005, 12, 31))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            position = st.text_input("Position")
            phone_number = st.text_input("Phone Number")
            submitted = st.form_submit_button("Add Sales Person")

            if submitted:
                st.session_state["new_salesperson_data"] = {
                    "id": new_id,
                    "sales_name": sales_name,
                    "dob": dob,
                    "gender": gender,
                    "position": position,
                    "phone_number": phone_number
                }
                st.session_state["confirm_add_salp"] = True

        if st.session_state.get("confirm_add_salp", False):
            st.warning("⚡ **Confirm Adding New Sales Person Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Add", use_container_width=True, key="confirm_salp_add_btn"):
                    try:
                        data = st.session_state["new_salesperson_data"]
                        cur.execute(
                            "INSERT INTO salesperson (salespersonid, salesname, dob, gender, position, phonenumber) VALUES (%s, %s, %s, %s, %s, %s)",
                            (data["id"], data["sales_name"], data["dob"], data["gender"], data["position"], data["phone_number"])
                        )
                        conn.commit()

                        history_update(cur, conn, "salesperson", data["id"], "salespersonid", "Insert", "-", data["id"])
                        history_update(cur, conn, "salesperson", data["id"], "salesname", "Insert", "-", data["sales_name"])
                        history_update(cur, conn, "salesperson", data["id"], "dob", "Insert", "-", str(data["dob"]))
                        history_update(cur, conn, "salesperson", data["id"], "gender", "Insert", "-", data["gender"])
                        history_update(cur, conn, "salesperson", data["id"], "position", "Insert", "-", data["position"])
                        history_update(cur, conn, "salesperson", data["id"], "phonenumber", "Insert", "-", data["phone_number"])

                        st.success("✅ New sales person record added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_add_sp"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width=True, key="cancel_sp_add_btn"):
                    st.session_state["confirm_add_sp"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update Sales Person Record")

        selected_update = st.selectbox("Select Sales Person to Update", all_data["SalesPersonID"].tolist(),
                                       key="update_salesperson")
        update_data = get_salespersondata(cur).loc[get_salespersondata(cur)["SalesPersonID"] == selected_update]
        st.dataframe(update_data)

        with st.form("Update Sales Person Record"):
            sales_name = st.text_input("Sales Name", value=update_data['SalesName'].iloc[0])
            dob = st.date_input("Date of Birth", value=pd.to_datetime(update_data['DOB'].iloc[0]),
                                min_value = date(1970, 1, 1), max_value = date(2005, 12, 31))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(update_data['Gender'].iloc[0]))
            position = st.text_input("Position", value=update_data['Position'].iloc[0])
            phone_number = st.text_input("Phone Number", value=update_data['PhoneNumber'].iloc[0])
            update_submitted = st.form_submit_button("Update Sales Person Record")

            if update_submitted:
                st.session_state["update_salesperson_data"] = {
                    "salespersonid": selected_update,
                    "sales_name": sales_name,
                    "dob": dob,
                    "gender": gender,
                    "position": position,
                    "phone_number": phone_number,
                    "current": update_data.iloc[0]
                }
                st.session_state["confirm_update_sp"] = True

        if st.session_state.get("confirm_update_sp", False):
            st.warning("⚡ **Confirm Updating Sales Person Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Update", use_container_width=True, key="confirm_salp_update_btn"):
                    try:
                        data = st.session_state["update_salesperson_data"]
                        current = data["current"]

                        if data["sales_name"] != current['SalesName']:
                            updatedata(cur, conn, 'salesperson', data["salespersonid"], 'salesname', current['SalesName'], data["sales_name"])
                        if data["dob"] != current['DOB']:
                            updatedata(cur, conn, 'salesperson', data["salespersonid"], 'dob', current['DOB'], str(data["dob"]))
                        if data["gender"] != current['Gender']:
                            updatedata(cur, conn, 'salesperson', data["salespersonid"], 'gender', current['Gender'], data["gender"])
                        if data["position"] != current['Position']:
                            updatedata(cur, conn, 'salesperson', data["salespersonid"], 'position', current['Position'], data["position"])
                        if data["phone_number"] != current['PhoneNumber']:
                            updatedata(cur, conn, 'salesperson', data["salespersonid"], 'phonenumber', current['PhoneNumber'], data["phone_number"])

                        conn.commit()
                        st.success("✅ Record updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_update_sp"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width=True, key="cancel_salp_update_btn"):
                    st.session_state["confirm_update_sp"] = False
                    st.rerun()

    # ------------------ DELETE RECORD ------------------
    with delete_record:
        st.subheader("Delete Sales Person Record")

        selected_delete = st.selectbox("Select Sales Person to Delete", all_data["SalesPersonID"].tolist(),
                                       key="delete_salesperson")
        delete_data = get_salespersondata(cur).loc[get_salespersondata(cur)["SalesPersonID"] == selected_delete]
        st.dataframe(delete_data)

        # Use a unique key based on selected_delete (SalesPersonID)
        if st.button(f"Delete Record {selected_delete}", key=f"delete_sp_btn_{selected_delete}"):
            st.session_state["delete_salesperson_data"] = {
                "id": selected_delete,
                "sales_name": delete_data['SalesName'].iloc[0],
                "dob": delete_data['DOB'].iloc[0],
                "gender": delete_data['Gender'].iloc[0],
                "position": delete_data['Position'].iloc[0],
                "phone_number": delete_data['PhoneNumber'].iloc[0]
            }
            st.session_state["confirm_delete_sp"] = True

        if st.session_state.get("confirm_delete_sp", False):
            st.warning("⚡ **Confirm Deleting Sales Person Record?**")
            col1, col2 = st.columns(2)
            with col2:
                # Make sure the confirm button has a unique key as well
                if st.button(f"✅ Confirm Delete {selected_delete}", use_container_width=True,
                             key=f"confirm_sp_delete_btn_{selected_delete}"):
                    try:
                        data = st.session_state["delete_salesperson_data"]

                        cur.execute("DELETE FROM salesperson WHERE salespersonid = %s", (data["id"],))
                        conn.commit()

                        history_update(cur, conn, "salesperson", data["id"], "salespersonid", "Delete", data["id"], "-")
                        history_update(cur, conn, "salesperson", data["id"], "sales_name", "Delete", data["sales_name"], "-")
                        history_update(cur, conn, "salesperson", data["id"], "dob", "Delete", data["dob"], "-")
                        history_update(cur, conn, "salesperson", data["id"], "gender", "Delete", data["gender"], "-")
                        history_update(cur, conn, "salesperson", data["id"], "position", "Delete", data["position"], "-")
                        history_update(cur, conn, "salesperson", data["id"], "phone_number", "Delete", data["phone_number"], "-")

                        st.success("✅ Record deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_delete_sp"] = False
                        st.rerun()
            with col1:
                if st.button(f"❌ Cancel Delete {selected_delete}", use_container_width=True,
                             key=f"cancel_sp_delete_btn_{selected_delete}"):
                    st.session_state["confirm_delete_sp"] = False
                    st.rerun()


