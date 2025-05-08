import streamlit as st
import pandas as pd
import numpy as np

from HistoryData.changehistory_update import history_update

def createuser(conn, username, salespersonid, password, nickname, email):
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,salespersonid, password, nickname, email) VALUES (%s,%s, %s, %s, %s)",
        (username,salespersonid, password, nickname, email))
    conn.commit()
    history_update(cur, conn, "users", username, "username", "Insert", "-", username)
    history_update(cur, conn, "users", username, "salespersonid", "Insert", "-", salespersonid)
    history_update(cur, conn, "users", username, "password", "Insert", "-", "Hidden")
    history_update(cur, conn, "users", username, "nickname", "Insert", "-", nickname)
    history_update(cur, conn, "users", username, "email", "Insert", "-", email)

def reset_password(conn, username, new_password):
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    conn.commit()
    history_update(cur, conn, "users", username, "password", "Update", "Hidden", "Hidden")

def get_user_role(position):
    position = position.lower()
    if "chief" in position:
        return "Chief"
    elif "manager" in position:
        return "Manager"
    elif "representative" in position:
        return "Representative"
    else:
        return "Representative"  # fallback

def login(users_data,salesperson_data, conn):
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
                    user_status = users_data[users_data["Username"] == username]["Status"].values[0]
                    if user_status.lower() == "banned":
                        st.error("Your account has been banned. Please contact the administrator.")
                    elif password == db_password:
                        if user_status != "Active":
                            cur = conn.cursor()
                            cur.execute("UPDATE Users SET Status = %s WHERE Username = %s", ("Active", username))
                            history_update(cur, conn, "users", username, "status", "Login", "Inactive", "Active")
                            conn.commit()
                            # Get user position from salesperson data
                            position = salesperson_data[salesperson_data["SalesPersonID"] ==
                                                        users_data[users_data["Username"] == username][
                                                            "SalesPersonID"].values[0]]["Position"].values[0]

                            # Set user role in session
                            st.session_state.role = get_user_role(position)
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("Username not found.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create an account", use_container_width=True):
                st.session_state.register_mode = True
                st.rerun()
        with col2:
            if st.button("Forgot Password", use_container_width=True):
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
                    st.stop()
                elif reg_username in users_data['Username'].values:
                    st.error("Username already exists.")
                    st.stop()
                elif salesid in users_data['SalesPersonID'].values:
                    st.error("Salesperson ID already exists.")
                    st.stop()
                elif salesid not in salesperson_data['SalesPersonID'].values:
                    st.error("Salesperson ID is not exists.")
                    st.stop()
                elif not salesid:
                    st.error("Salesperson ID is required.")
                else:
                    st.session_state["pending_register_data"] = {
                        "username": reg_username,
                        "salesid": salesid,
                        "password": reg_password,
                        "nickname": nickname,
                        "email": email
                    }
                    st.session_state["confirm_register"] = True
                    st.rerun()

            if st.session_state.get("confirm_register", False):
                st.warning("⚡ **Confirm Creating New Account?**")
                col1, col2 = st.columns(2)
                with col2:
                    if st.button("✅ Confirm Register", use_container_width=True, key="confirm_register_btn"):
                        data = st.session_state["pending_register_data"]
                        createuser(conn, data["username"], data["salesid"], data["password"], data["nickname"],data["email"])
                        st.success("Account created successfully. You can now log in.")
                        st.session_state.register_mode = False
                        st.session_state.pop("pending_register_data", None)
                        st.session_state["confirm_register"] = False
                        st.rerun()
                with col1:
                    if st.button("❌ Cancel Register", use_container_width=True, key="cancel_register_btn"):
                        st.session_state.pop("pending_register_data", None)
                        st.session_state["confirm_register"] = False
                        st.rerun()
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
                user_row = users_data[users_data["Username"] == forgot_username]
                user_email = user_row["Email"].values[0]
                user_status = user_row["Status"].values[0]

                if user_status == "Banned":
                    st.error("Your account has been banned. Cannot reset password.")
                    st.stop()
                elif forgot_email != user_email:
                    st.error("Email doesn't match the username.")
                    st.stop()
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                    st.stop()
                else:
                    st.session_state["pending_reset_data"] = {
                        "username": forgot_username,
                        "new_password": new_password
                    }
                    st.session_state["confirm_reset_password"] = True
                    st.rerun()

        if st.session_state.get("confirm_reset_password", False):
            st.warning("⚡ **Confirm Resetting Password?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Reset", use_container_width=True, key="confirm_reset_btn"):
                    data = st.session_state["pending_reset_data"]
                    reset_password(conn, data["username"], data["new_password"])
                    st.success("Password reset successfully. You can now log in.")
                    st.session_state.forgotpassword_mode = False
                    st.session_state.pop("pending_reset_data", None)
                    st.session_state["confirm_reset_password"] = False
                    st.rerun()
            with col1:
                if st.button("❌ Cancel Reset", use_container_width=True, key="cancel_reset_btn"):
                    st.session_state.pop("pending_reset_data", None)
                    st.session_state["confirm_reset_password"] = False
                    st.rerun()

        if st.button("Back to login"):
                st.session_state.forgotpassword_mode = False
                st.rerun()

def get_username():
    return st.session_state.username