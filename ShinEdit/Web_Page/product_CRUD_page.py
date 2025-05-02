import streamlit as st
import pandas as pd

from GetData.newproductdata import get_one_newproductdata
from DropdownInfo.filtersearch import get_details
from HistoryData.query_data import updatedata
from HistoryData.changehistory_update import history_update

def Product_CRUD(cur, conn, all_data, display_data):
    st.header("Product Record")

    # ------------------ FILTER SEARCH ------------------
    col1, col2 = st.columns(2)

    with col1:
        filopt = ["Default", "ProductID", "Status", "ImportLoc"]
        filters = st.selectbox("Filter Search", filopt, index=0, key='Filter_Product')

    with col2:
        if filters == 'Default':
            st.selectbox("Select Details", options=[], disabled=True, key='Details_Product')
            displaying = display_data
        else:
            details = get_details(cur, 'Product', filters)
            selected_details = st.selectbox("Select Details", details, index=0)
            displaying = get_one_newproductdata(cur, filters, selected_details)

    # ------------------ DISPLAY DATA ------------------
    st.dataframe(displaying)
    add_record, update_record, delete_record = st.tabs(['Add', 'Update', 'Delete'])

    # ------------------ ADD RECORD ------------------
    with add_record:
        if len(all_data) == 0:
            new_value = "P001"
        else:
            last_value = all_data['ProductID'].iloc[-1]
            prefix = ''.join(filter(str.isalpha, last_value))
            number = ''.join(filter(str.isdigit, last_value))
            new_number = str(int(number) + 1).zfill(len(number))
            new_value = prefix + new_number

        st.subheader("Add New Product")

        with st.form("Add Product Record"):
            new_id = st.text_input("Product ID", value=new_value, disabled=True)
            product_name = st.text_input("Product Name")
            in_stock = st.number_input("In Stock Quantity", min_value=0)
            status = st.selectbox("Status", ["profit", "loss", "break-even"])
            import_loc = st.text_input("Import Location")
            submitted = st.form_submit_button("Add Product")

            if submitted:
                st.session_state["new_product_data"] = {
                    "id": new_id,
                    "name": product_name,
                    "stock": in_stock,
                    "status": status,
                    "importloc": import_loc
                }
                st.session_state["confirm_add_product"] = True

        if st.session_state.get("confirm_add_product", False):
            st.warning("⚡ **Confirm Adding New Product?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Add", use_container_width=True, key="confirm_product_add_btn"):
                    try:
                        data = st.session_state["new_product_data"]
                        cur.execute(
                            "INSERT INTO product (productid, productname, instock, status, importloc) VALUES (%s, %s, %s, %s, %s)",
                            (data["id"], data["name"], data["stock"], data["status"], data["importloc"])
                        )
                        conn.commit()

                        for field in data:
                            history_update(cur, conn, "product", data["id"], field, "Insert", "-", data[field])

                        st.success("✅ New product added successfully!")
                    except Exception as e:
                        st.error(f"❌ Insert failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_add_product"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Add", use_container_width=True, key="cancel_product_add_btn"):
                    st.session_state["confirm_add_product"] = False
                    st.rerun()

    # ------------------ UPDATE RECORD ------------------
    with update_record:
        st.subheader("Update Product")

        selected_update = st.selectbox("Select Product to Update", all_data["ProductID"].tolist(), key="update_product")
        update_data = get_one_newproductdata(cur, 'ProductID',selected_update)
        st.dataframe(update_data)

        with st.form("Update Product Record"):
            update_name = st.text_input("Product Name", value=update_data['ProductName'][0])
            update_stock = st.number_input("In Stock", value=update_data['InStock'][0], min_value=0)
            update_status = st.selectbox("Status", ["profit", "loss", "break-even"],index=["profit", "loss", "break-even"].index(update_data['Status'][0]))
            update_import = st.text_input("Import Location", value=update_data['ImportLoc'][0])

            update_submitted = st.form_submit_button("Update Product")

            if update_submitted:
                st.session_state["update_product_data"] = {
                    "productid": selected_update,
                    "productname": update_name,
                    "instock": update_stock,
                    "status": update_status,
                    "importloc": update_import,
                    "current": update_data.iloc[0]
                }
                st.session_state["confirm_update_product"] = True

        if st.session_state.get("confirm_update_product", False):
            st.warning("⚡ **Confirm Updating Product Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Update", use_container_width=True, key="confirm_product_update_btn"):
                    try:
                        data = st.session_state["update_product_data"]
                        current = data["current"]

                        if data["productname"] != current['ProductName']:
                            updatedata(cur, conn, 'product', data["productid"], 'productname', current['ProductName'],
                                       data["productname"])

                        if data["instock"] != current['InStock']:
                            updatedata(cur, conn, 'product', data["productid"], 'instock', current['InStock'],
                                       data["instock"])

                        if data["status"] != current['Status']:
                            updatedata(cur, conn, 'product', data["productid"], 'status', current['Status'],
                                       data["status"])

                        if data["importloc"] != current['ImportLoc']:
                            updatedata(cur, conn, 'product', data["productid"], 'importloc', current['ImportLoc'],
                                       data["importloc"])

                        conn.commit()
                        st.success("✅ Product updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Update failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_update_product"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Update", use_container_width=True, key="cancel_product_update_btn"):
                    st.session_state["confirm_update_product"] = False
                    st.rerun()

    # ------------------ DELETE RECORD ------------------
    with delete_record:
        st.subheader("Delete Product")

        selected_delete = st.selectbox("Select Product to Delete", all_data["ProductID"].tolist(), key="delete_product")
        delete_data = get_one_newproductdata(cur, 'ProductID', selected_delete)
        st.dataframe(delete_data)

        if st.button("Delete Record", key="delete_product_btn"):
            st.session_state["delete_product_data"] = {
                "id": selected_delete,
                "name": delete_data['ProductName'][0],
                "stock": delete_data['InStock'][0],
                "status": delete_data['Status'][0],
                "importloc": delete_data['ImportLoc'][0]
            }
            st.session_state["confirm_delete_product"] = True

        if st.session_state.get("confirm_delete_product", False):
            st.warning("⚡ **Confirm Deleting Product Record?**")
            col1, col2 = st.columns(2)
            with col2:
                if st.button("✅ Confirm Delete", use_container_width=True, key="confirm_product_delete_btn"):
                    try:
                        data = st.session_state["delete_product_data"]

                        cur.execute("DELETE FROM product WHERE productid = %s", (data["id"],))
                        conn.commit()

                        for field in data:
                            if field != "id":
                                history_update(cur, conn, "productid", data["id"], field, "Delete", data[field], "-")
                                history_update(cur, conn, "productname", data["id"], field, "Delete", data[field], "-")
                                history_update(cur, conn, "instock", data["id"], field, "Delete", data[field], "-")
                                history_update(cur, conn, "status", data["id"], field, "Delete", data[field], "-")
                                history_update(cur, conn, "importloc", data["id"], field, "Delete", data[field], "-")

                        st.success("✅ Product deleted successfully!")
                    except Exception as e:
                        st.error(f"❌ Delete failed: {e}")
                        st.stop()
                    finally:
                        st.session_state["confirm_delete_product"] = False
                        st.rerun()
            with col1:
                if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_product_delete_btn"):
                    st.session_state["confirm_delete_product"] = False
                    st.rerun()