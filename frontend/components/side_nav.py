from datetime import date
import time
import streamlit as st


async def render_side_nav():
    with st.sidebar:

        # # Date filter container
        # with st.container():
        #     st.write("### Data Filter")

        #     changed_date = st.date_input(
        #         "Select Date Range",
        #         (date(2024, 1, 1), date(2024, 1, 1)),
        #         date(2024, 1, 1),
        #         date(2099, 12, 31),
        #         format="YYYY.MM.DD"
        #     )

        # new expense form
        with st.container():
            with st.form("New Expense Form", border=False):
                st.write("### Add New Expense")

                vendor_name = st.text_input("Vendor Name")
                vendor_id = st.text_input("Vendor Id")

                col0, col1 = st.columns(2)
                exp_date = col0.date_input("Expense Date")
                category = col1.text_input("Expense Category")

                col2, col3 = st.columns(2)

                amount = col2.number_input("Expense Amount")
                exp_type = col3.selectbox("Expense Type", options=["DR", "CR"])

                def submit_handler():
                    print(vendor_name, vendor_id, exp_date,
                          category, amount, exp_type)

                st.form_submit_button(
                    "Add Expense", on_click=submit_handler, use_container_width=True)

    # return changed_date
