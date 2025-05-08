import streamlit as st
import pandas as pd

from HistoryData.changehistory_update import history_update
from HistoryData.query_data import updatedata

def show_user_sidebar(users_data, salespersondata, username,conn):
    # Merge user table and salesperson table
    user_info = pd.merge(users_data, salespersondata, on="SalesPersonID", how="inner")
    current_user = user_info[user_info["Username"] == username]

    with st.sidebar:
        st.subheader("👤 User Info")
        st.write(f"**Username:** {current_user['Username'].values[0]}")
        st.write(f"**Name:** {current_user['SalesName'].values[0]}")
        st.write(f"**Nickname:** {current_user['Nickname'].values[0]}")
        st.write(f"**Position:** {current_user['Position'].values[0]}")
        st.write(f"**Email:** {current_user['Email'].values[0]}")
        st.write(f"**Phone:** {current_user['PhoneNumber'].values[0]}")
        st.write(f"**Gender:** {current_user['Gender'].values[0]}")

        # Modify button
        if st.button("Modify Info"):
            st.session_state.modify_page = True

        # Logout
        if st.button("Logout"):
            cur = conn.cursor()
            cur.execute("UPDATE Users SET Status = %s WHERE Username = %s", ("Inactive", username))
            conn.commit()

            history_update(cur, conn, "users", username, "status", "Logout", "Active", "Inactive")

            st.session_state.logged_in = False
            st.rerun()

def edit_user_page(users_data, salespersondata, username, conn):
    # Merge user table and salesperson table
    user_info = pd.merge(users_data, salespersondata, on="SalesPersonID", how="inner")
    current_user = user_info[user_info["Username"] == username]

    #Edit page
    st.subheader("Edit Your Information")
    new_nickname = st.text_input("New Nickname", current_user["Nickname"].values[0])
    new_email = st.text_input("New Email", current_user["Email"].values[0])
    new_phone = st.text_input("New Phone", current_user["PhoneNumber"].values[0])
    new_password = st.text_input("New Password", type="password")

    if st.button("Save Changes"):
        st.session_state["edit_data"] = {
            "username" : current_user['Username'].values[0],
            "spid" : current_user['SalesPersonID'].values[0],
            "nickname": new_nickname,
            "email": new_email,
            "phone": new_phone,
            "password": new_password,
            "current" : current_user.iloc[0]
        }
        st.session_state["confirm_edit"] = True

    if st.session_state.get("confirm_edit", False):
        st.warning("⚡ **Confirm Editing User Information ?**")
        col1, col2 = st.columns(2)
        with col2:
            if st.button("✅ Confirm Edit", use_container_width=True, key="confirm_edit_btn"):
                try:
                    data = st.session_state["edit_data"]
                    current = data['current']
                    cur = conn.cursor()

                    if data['nickname'] != current["Nickname"]:
                        updatedata(cur, conn, 'users', data['username'], 'nickname', current["Nickname"], data['nickname'])

                    if new_email != current["Email"]:
                        updatedata(cur, conn, 'users', data['username'], 'email', current["Email"], data['email'])

                    if new_phone != current["PhoneNumber"]:
                        updatedata(cur, conn, 'salesperson', data['spid'], 'phonenumber',
                                       current["PhoneNumber"], data['phone'])

                    # check if new password enter or not
                    if new_password.strip():
                        cur.execute("UPDATE Users SET Password = %s WHERE Username = %s", (data['password'], data['username']))
                        conn.commit()
                        history_update(cur, conn, "users", data['username'], "password", "Update", "Hidden", "Hidden")

                    st.success("Information updated successfully!")

                except Exception as e:
                    st.error(f"❌ Update failed: {e}")
                    st.stop()

                finally:
                    st.session_state["confirm_edit"] = False
                    st.rerun()

        with col1:
            if st.button("❌ Cancel Edit", use_container_width=True, key="cancel_edit_btn"):
                st.session_state["confirm_edit"] = False
                st.rerun()

    if st.button("Cancel"):
        st.session_state.modify_page = False
        st.rerun()