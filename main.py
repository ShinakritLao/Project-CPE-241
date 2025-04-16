import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


# Function get sales data
@st.cache_data
def get_sales_data():
    # Sample data for all 3 people for 3 years
    data = {
        "Sales Name": ["AAA ZZZ"] * 36 + ["BBB YYY"] * 36 + ["CCC XXX"] * 36,
        "Year": [2024] * 12 + [2023] * 12 + [2022] * 12 + [2024] * 12 + [2023] * 12 + [2022] * 12 + [2024] * 12 + [
            2023] * 12 + [2022] * 12,
        "Month": ["01 Jan", "02 Feb", "03 Mar", "04 Apr", "05 May", "06 Jun", "07 Jul", "08 Aug", "09 Sep", "10 Oct",
                  "11 Nov", "12 Dec"] * 9,
        "Sales": [
            100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210,  # AAA ZZZ 2024
            90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145,  # AAA ZZZ 2023
            80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135,  # AAA ZZZ 2022
            200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310,  # BBB YYY 2024
            190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240, 245,  # BBB YYY 2023
            180, 185, 190, 195, 200, 205, 210, 215, 220, 225, 230, 235,  # BBB YYY 2022
            300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410,  # CCC XXX 2024
            290, 295, 300, 305, 310, 315, 320, 325, 330, 335, 340, 345,  # CCC XXX 2023
            280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335,  # CCC XXX 2022
        ]
    }
    return pd.DataFrame(data)


# Function get product data
@st.cache_data
def get_product_data():
    # Sample data for all 3 people for 3 years
    data = {
        "Sales Name": ["AAA ZZZ"] * 9 + ["BBB YYY"] * 9 + ["CCC XXX"] * 9,
        "Year": [2024, 2023, 2022] * 9,
        "ProductID": [101, 102, 103, 104, 105, 106, 107, 108, 109] * 3,
        "ProductName": ["Product A", "Product B", "Product C", "Product D", "Product E", "Product F", "Product G",
                        "Product H", "Product I"] * 3,
        "NumberOfProduct": [10, 20, 30, 40, 50, 60, 70, 80, 90] * 3,
        "TotalSales": [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000] * 3,
        "TotalCosts": [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500] * 3,
        "Status": ["Profit", "Profit", "Profit", "Profit", "Profit", "Profit", "Profit", "Profit", "Profit"] * 3
    }
    return pd.DataFrame(data)


# Function get debtor data
@st.cache_data
def get_debtor_data():
    # Sample data for all 3 people for 3 years
    data = {
        "Sales Name": ["AAA ZZZ"] * 9 + ["BBB YYY"] * 9 + ["CCC XXX"] * 9,
        "Year": [2024, 2023, 2022] * 9,
        "CompanyName": ["Company A", "Company B", "Company C", "Company D", "Company E", "Company F", "Company G",
                        "Company H", "Company I"] * 3,
        "ProductID": [101, 102, 103, 104, 105, 106, 107, 108, 109] * 3,
        "ProductName": ["Product A", "Product B", "Product C", "Product D", "Product E", "Product F", "Product G",
                        "Product H", "Product I"] * 3,
        "Price": [100, 200, 300, 400, 500, 600, 700, 800, 900] * 3,
        "Debt": [10, 20, 30, 40, 50, 60, 70, 80, 90] * 3,
        "Paid": [90, 180, 270, 360, 450, 540, 630, 720, 810] * 3,
        "Date": ["2024-01-01", "2023-02-01", "2022-03-01", "2024-04-01", "2023-05-01", "2022-06-01", "2024-07-01",
                 "2023-08-01", "2022-09-01"] * 3,
        "Status": ["X", "X", "X", "X", "X", "X", "X", "X", "X"] * 3
    }
    return pd.DataFrame(data)


# Function get data for KPI
@st.cache_data
def get_kpi_data():
    data = {
        "Sales Name": ["AAA ZZZ"] * 3 + ["BBB YYY"] * 3 + ["CCC XXX"] * 3,
        "Year": [2024, 2023, 2022] * 3,
        "TargetQ": [200, 150, 100] * 3,
        "Quotation": [150, 100, 50] * 3,
        "TargetSO": [150, 100, 50] * 3,
        "SaleOrder": [100, 75, 25] * 3,
        "AllCustomer": [300] * 9,
        "CustomerHand": [50, 30, 20] * 3,
    }
    return pd.DataFrame(data)


# Main function set up Streamlit
def main():
    # SetUp wide mode
    st.set_page_config(layout="wide")

    # Create tabs
    Sales_Dashboard, Sales_CRUD = st.tabs(["Sales Dashboard", "Sales CRUD"])

    # Load Data 1
    sales_data = get_sales_data()
    product_data = get_product_data()
    debtor_data = get_debtor_data()
    kpi_data = get_kpi_data()

    with Sales_Dashboard:
        # Create dropdowns for Sales Name and Year
        col1, col2 = st.columns([1, 1])
        with col1:
            DropdownSalesName = st.selectbox("Select Sales", ["Sales Name", "AAA ZZZ", "BBB YYY", "CCC XXX"])
        with col2:
            DropdownYears = st.selectbox("Select Years", ["Years", "2024", "2023", "2022"])

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
            filtered_sales_data = sales_data[
                (sales_data["Sales Name"] == DropdownSalesName) & (sales_data["Year"] == int(DropdownYears))]

            # Ensure the months ordered
            month_order = ["01 Jan", "02 Feb", "03 Mar", "04 Apr", "05 May", "06 Jun", "07 Jul", "08 Aug", "09 Sep",
                           "10 Oct", "11 Nov", "12 Dec"]
            filtered_sales_data["Month"] = pd.Categorical(filtered_sales_data["Month"], categories=month_order,
                                                          ordered=True)
            filtered_sales_data = filtered_sales_data.sort_values("Month")

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

            # Filter KPI data based on dropdown for col2
            filtered_kpi_data = kpi_data[
                (kpi_data["Sales Name"] == DropdownSalesName) & (kpi_data["Year"] == int(DropdownYears))]

            with col2:
                st.subheader("Key Performance Indicators")
                # Create a 2x2 grid for the KPI tab
                kpi1, kpi2 = st.columns(2)
                kpi3, kpi4 = st.columns(2)

                # Function to create a KPI metric with customized font size, colored background, and aligned text to the right
                def create_metric(label, value, delta):
                    st.markdown(
                        f"""
                         <div style="background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px; padding: 10px; 
                         margin-bottom: 10px; text-align: right;">
                             <div style="font-size:24px;">{label}</div>
                             <div style="font-size:30px;">{value}</div>
                             <div style="font-size:20px; color:green;">{delta}</div>
                         </div>
                         """,
                        unsafe_allow_html=True
                    )

                # Use the updated function in your main function for each KPI column

                with kpi1:
                    create_metric("Quotation Rate",
                                  f"{(filtered_kpi_data['Quotation'].values[0] / filtered_kpi_data['TargetQ'].values[0]) * 100:.2f}%",
                                  f"{filtered_kpi_data['Quotation'].values[0]}")

                with kpi2:
                    create_metric("Sale Order Rate",
                                  f"{(filtered_kpi_data['SaleOrder'].values[0] / filtered_kpi_data['TargetSO'].values[0]) * 100:.2f}%",
                                  f"{filtered_kpi_data['SaleOrder'].values[0]}")

                with kpi3:
                    conversion_rate = (filtered_kpi_data['SaleOrder'].values[0] / filtered_kpi_data['Quotation'].values[
                        0]) * 100
                    create_metric("Conversion Rate", f"{conversion_rate:.2f}%", "")

                with kpi4:
                    create_metric("Conversion Rate",
                                  f"{filtered_kpi_data['CustomerHand'].values[0]} / {filtered_kpi_data['AllCustomer'].values[0]}",
                                  "")

            # Filter debtor data based on dropdown for col3
            filtered_debtor_data = debtor_data[
                (debtor_data["Sales Name"] == DropdownSalesName) & (debtor_data["Year"] == int(DropdownYears))]
            filtered_debtor_data = filtered_debtor_data.drop(columns=["Sales Name", "Year"])

            with col3:
                st.subheader("Debtors")
                st.dataframe(filtered_debtor_data.reset_index(drop=True))

            # Filter product data based on dropdown for col4
            filtered_product_data = product_data[
                (product_data["Sales Name"] == DropdownSalesName) & (product_data["Year"] == int(DropdownYears))]
            filtered_product_data = filtered_product_data.drop(columns=["Sales Name", "Year"])

            with col4:
                st.subheader("Product List")
                st.dataframe(filtered_product_data.reset_index(drop=True))

        else:
            st.warning("Please select a valid Sales and Year from the dropdowns.")

    with Sales_CRUD:
        st.header("Sales CRUD")
        #test


# Run main function
if __name__ == "__main__":
    main()