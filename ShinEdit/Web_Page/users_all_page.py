import streamlit as st
import pandas as pd
import numpy as np

from HistoryData.changehistory_update import history_update

def users_all_page(cur, conn, display_users):

    # ------------------ DELETE USER ------------------
    st.subheader("Delete User")

    selected_data = st.selectbox("Select Username to Delete", display_users['Username'].tolist())
    current_data = display_users.loc[display_users['Username'] == selected_data]
    st.dataframe(current_data)

    if st.button("Delete User", key="delete_user_btn"):
        st.session_state["delete_username"] = selected_data
        st.session_state["confirm_delete"] = True

    if st.session_state.get("confirm_delete", False):
        st.warning("⚡ **Confirm Deleting User?**")
        col1, col2 = st.columns(2)
        with col2:
            if st.button("✅ Confirm Delete", use_container_width=True, key="confirm_delete_user_btn"):
                try:
                    cur.execute("DELETE FROM Users WHERE Username = %s", (st.session_state["delete_username"],))
                    conn.commit()
                    history_update(cur, conn, "users", st.session_state["delete_username"], "-", "Delete", "-", "-")

                    st.warning("✅ User deleted successfully!")
                except Exception as e:
                    st.error(f"❌ Delete failed: {e}")
                finally:
                    st.session_state["confirm_delete"] = False
                    st.rerun()
        with col1:
            if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_delete_user_btn"):
                st.session_state["confirm_delete"] = False
                st.rerun()

    # ------------------ BAN USER ------------------

    st.markdown("---")
    st.subheader("Banned / Unbanned User")

    for idx, selected_user_data in display_users.iterrows():

        current_user_users = pd.DataFrame(selected_user_data).T
        st.dataframe(current_user_users)

        cur.execute("SELECT Status FROM Users WHERE Username = %s", (selected_user_data['Username'],))
        current_status = cur.fetchone()[0]

        if current_status != 'Banned':
            button_status = "Banned"
            database_status = button_status
        else:
            button_status = "Unbanned"
            database_status = "Inactive"

        if st.button(f"{button_status}", key=f"user_status_btn_{idx}"):
            st.session_state[f"username_{idx}"] = selected_user_data['Username']
            st.session_state[f"confirm_status_{idx}"] = True

        if st.session_state.get(f"confirm_status_{idx}", False):
            st.warning(f"⚡ **Confirm {button_status} User?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button(f"✅ Confirm {button_status}", use_container_width=True, key=f"confirm_user_status_{idx}"):
                    try:
                        cur.execute(f"UPDATE Users SET Status = %s WHERE Username = %s",
                                    (database_status, st.session_state[f"username_{idx}"]))
                        conn.commit()
                        history_update(cur, conn, "users", st.session_state[f"username_{idx}"], "status", button_status,
                                       current_status, database_status)

                        st.warning(f"✅ User {button_status} successfully!")
                    except Exception as e:
                        st.error(f"❌ {button_status} failed: {e}")
                    finally:
                        st.session_state[f"confirm_status_{idx}"] = False
                        st.rerun()
            with col1:
                if st.button(f"❌ Cancel {button_status}", use_container_width=True, key=f"cancel_user_status_btn_{idx}"):
                    st.session_state[f"confirm_status_{idx}"] = False
                    st.rerun()