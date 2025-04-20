import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def dashboard(salesyear, salesperson, sales_data, product_data, kpi_data, debtor_data):
    # Create dropdowns for Sales Name and Year
    col1, col2 = st.columns([1, 1])
    with col1:
        DropdownSalesName = st.selectbox("Select Sales", salesperson)
    with col2:
        DropdownYears = st.selectbox("Select Years", salesyear)

    # Display header with selected Sales Name and Year
    if DropdownSalesName != "Sales Name" and DropdownYears != "Years":
        st.header(f"({DropdownSalesName}, {DropdownYears})")
    else:
        st.header("SALES")

    # Create a 2x2 grid for the sales tab
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Filter sales data based on dropdown
    if DropdownSalesName != "Sales Name" and DropdownYears != "Years":
        filtered_sales_data = sales_data

        # Create decorated pie chart using Altair for col1
        base = alt.Chart(filtered_sales_data).encode(
            theta=alt.Theta("Sales", stack=True),
            radius=alt.Radius("Sales", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
            color=alt.Color("Month", scale=alt.Scale(scheme='category20')),
            tooltip=["Month", "Sales"]
        )

        # Customizing the appearance of the pie chart
        circle_chart = base.mark_arc(
            innerRadius=20,
            outerRadius=120,
            opacity=0.8,  # Adjust opacity for better visibility
            strokeWidth=3,  # Add stroke for better separation
            stroke='gray'  # Set stroke color to white for contrast
        ).configure_legend(
            title=None,  # Remove legend title
            labelFontSize=20,  # Adjust legend label font size
            labelLimit=200,  # Increase label limit for clarity
        )

        with col1:
            st.subheader("Monthly Sales")
            st.altair_chart(circle_chart, use_container_width=True)

        filtered_kpi_data = kpi_data

        with col2:
            st.subheader("Key Performance Indicators")
            # Create a 2x2 grid for the KPI tab
            kpi1, kpi2 = st.columns(2)
            kpi3, kpi4 = st.columns(2)


            # Function to create a KPI metric with customized font size, colored background, and aligned text to the right
            def create_metric(label, value, delta):
                formatted_delta = "{:,}".format(float(delta.replace(',', ''))) if delta else ""
                st.markdown(
                    f"""
                        <div style="background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; padding: 10px;
                        margin-bottom: 10px; text-align: right;">
                            <div style="font-size:24px;">{label}</div>
                            <div style="font-size:30px;">{value}</div>
                            <div style="font-size:20px; color:green;">{formatted_delta}</div>
                        </div>
                        """,
                    unsafe_allow_html=True
                )


            try:
                quotation_rate = (filtered_kpi_data['Quotation'].values[0] / filtered_kpi_data['TargetQ'].values[
                    0]) * 100
                sale_order_rate = (filtered_kpi_data['SaleOrder'].values[0] / filtered_kpi_data['TargetSO'].values[
                    0]) * 100
                conversion_rate = (filtered_kpi_data['SaleOrder'].values[0] / filtered_kpi_data['Quotation'].values[
                    0]) * 100
                customers = f"{filtered_kpi_data['CustomerHand'].values[0]} / {filtered_kpi_data['AllCustomer'].values[0]}"

                with kpi1:
                    create_metric("Quotation Rate", f"{quotation_rate:.2f}%",
                                  f"{filtered_kpi_data['Quotation'].values[0]}")
                with kpi2:
                    create_metric("Sale Order Rate", f"{sale_order_rate:.2f}%",
                                  f"{filtered_kpi_data['SaleOrder'].values[0]}")
                with kpi3:
                    create_metric("Conversion Rate", f"{conversion_rate:.2f}%", "")
                with kpi4:
                    create_metric("Customers", customers, "")
            except Exception as error:
                st.warning(f"Error in KPI calculations: {error}")

        # Filter debtor data based on dropdown for col3
        filtered_debtor_data = debtor_data
        with col3:
            st.subheader("Debtors")
            st.dataframe(filtered_debtor_data.reset_index(drop=True))

        # Filter product data based on dropdown for col4
        filtered_product_data = product_data

        with col4:
            st.subheader("Product List")
            st.dataframe(filtered_product_data.reset_index(drop=True))

    else:
        st.warning("Please select a valid Sales and Year from the dropdowns.")