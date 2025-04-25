import streamlit as st
import pandas as pd

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
        cur = conn.cursor()
        cur.execute("""
               UPDATE Users SET Nickname = %s, Email = %s
               WHERE Username = %s
           """, (new_nickname, new_email, username))

        #check if new password enter or not
        if new_password.strip():
            cur.execute("""
                   UPDATE Users SET Password = %s
                   WHERE Username = %s
               """, (new_password, username))

        cur.execute("""
            UPDATE SalesPerson SET PhoneNumber = %s
            WHERE SalesPersonID = %s
        """, (new_phone, current_user["SalesPersonID"].values[0]))
        conn.commit()

        st.success("Information updated successfully!")
        st.session_state.modify_page = False
        st.rerun()

    if st.button("Cancel"):
        st.session_state.modify_page = False
        st.rerun()

