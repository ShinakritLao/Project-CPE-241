import streamlit as st
import pandas as pd
import numpy as np

def createuser(conn, username, salespersonid, password, nickname, email):
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,salespersonid, password, nickname, email) VALUES (%s,%s, %s, %s, %s)",
        (username,salespersonid, password, nickname, email))
    conn.commit()

def reset_password(conn, username, new_password):
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    conn.commit()

def login(users_data, conn):
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "register_mode" not in st.session_state:
        st.session_state.register_mode = False
    if "forgotpassword_mode" not in st.session_state:
        st.session_state.forgotpassword_mode = False

    if not st.session_state.logged_in and not st.session_state.register_mode and not st.session_state.forgotpassword_mode:
        with st.form("Login Form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In")
            if submit:
                if username in users_data["Username"].values:
                    db_password = users_data[users_data["Username"] == username]["Password"].values[0]
                    if password == db_password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("Username not found.")
        if st.button("Create an account"):
            st.session_state.register_mode = True
            st.rerun()
        if st.button("Forgot Password"):
            st.session_state.forgotpassword_mode = True
            st.rerun()

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
                    elif reg_username in users_data['Username'].values:
                        st.error("Username already exists.")
                    elif not salesid:
                        st.error("Salesperson ID is required.")
                    else:
                        createuser(conn, reg_username, salesid, reg_password, nickname, email)
                        st.success("Account created successfully. You can now log in.")
                        st.session_state.register_mode = False
        except ValueError as error:
            st.error("The input is invalid. it does not comply with database standards")

        if st.button("Back to login"):
            st.session_state.register_mode = False
            st.rerun()

    elif st.session_state.forgotpassword_mode:
        with st.form("Forgot Password Form"):
            st.subheader("Forgot Password")
            forgot_username = st.text_input("Username")
            forgot_username = forgot_username.lower()
            forgot_email = st.text_input("Email")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_reset = st.form_submit_button("Reset Password")

        if submit_reset:
            if forgot_username not in users_data["Username"].values:
                st.error("Username not found.")
            else:
                user_email = users_data[users_data["Username"] == forgot_username]["Email"].values[0]
                if forgot_email != user_email:
                    st.error("Email doesn't match the username.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    reset_password(conn, forgot_username, new_password)
                    st.success("Password reset successfully. You can now log in.")
                    st.session_state.forgotpassword_mode = False
                    st.rerun()

        if st.button("Back to login"):
                st.session_state.forgotpassword_mode = False
                st.rerun()

def get_username():
    return st.session_state.username