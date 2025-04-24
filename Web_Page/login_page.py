import streamlit as st
import pandas as pd

def get_user(users_df, username):
    user_row = users_df[users_df['Username'] == username]
    if not user_row.empty:
        return {"username": user_row['Username'].values[0],"password": user_row['Password'].values[0]}
    return None

def reg_acc(conn, username, salespersonid, password, nickname, email):
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,salespersonid, password, nickname, email) VALUES (%s,%s, %s, %s, %s)",
        (username,salespersonid, password, nickname, email))
    conn.commit()

def login(users_df, conn):
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "register_mode" not in st.session_state:
        st.session_state.register_mode = False

    if not st.session_state.logged_in and not st.session_state.register_mode:
        with st.form("Login Form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In")
            if submit:
                user = get_user(users_df, username)
                if user and password == user["password"]:
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
        if st.button("Create an account"):
            st.session_state.register_mode = True
    elif st.session_state.register_mode:
        try:
            with st.form("Register Form"):
                st.subheader("Register")
                reg_username = st.text_input("Username")
                reg_username = reg_username.lower()
                salesid = st.text_input("Salesperson ID")
                reg_password = st.text_input("Password", type="password")
                check = st.text_input("Confirm Password", type="password")
                nickname = st.text_input("Nickname")
                email = st.text_input("Email")
                register_submit = st.form_submit_button("Register")
                if register_submit:
                    if reg_password != check:
                        st.error("Passwords do not match.")
                    elif get_user(users_df, reg_username):
                        st.error("Username already exists.")
                    elif not salesid:
                        st.error("Salesperson ID is required.")
                    else:
                        reg_acc(conn, reg_username, salesid, reg_password, nickname, email)
                        st.success("Account created successfully. You can now log in.")
                        st.session_state.register_mode = False
        except ValueError as error:
            st.error("The input is invalid. it does not comply with database standards")

        if st.button("Back to login"):
            st.session_state.register_mode = False

    elif st.session_state.logged_in:
        st.info(f"Logged in as: {st.session_state.user}")
