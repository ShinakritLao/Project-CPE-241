import streamlit as st
import pandas as pd
import numpy as np

# Login credentials
USER_CREDENTIALS = {
    "admin": "admin123",
    "salesuser": "sales2025"
}

def login(users_data):
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with st.form("Login Form"):
            st.subheader("Please log in")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")