import os
import requests
from datetime import date
import streamlit as st
from server import context
from uuid import uuid4
from controller import NetworkClient


async def render_side_nav():
    with st.sidebar:

        # Date filter container
        with st.container():
            st.write("### Data Filter")

            changed_date = st.date_input(
                "Select Date Range",
                (date.today().replace(day=1), date.today()),
                date(2024, 1, 1),
                date(2099, 12, 31),
                format="YYYY.MM.DD"
            )

            context['date_filters'] = changed_date

        # Add new Category
        with st.container():
            with st.form("Add Category", border=False, clear_on_submit=True):

                category = st.text_input(label="New Category")
                st.form_submit_button(use_container_width=True)

                context['categories'].add(category)

        # new expense form
        with st.container():
            with st.form("New Expense Form", border=False, clear_on_submit=True):
                st.write("### Add New Expense")

                vendor_name = st.text_input("Vendor Name")
                vendor_id = st.text_input("Vendor Id")

                col0, col1 = st.columns(2)
                exp_date = col0.date_input("Expense Date")
                category = col1.text_input("Expense Category")

                col2, col3 = st.columns(2)

                amount = col2.number_input("Expense Amount")
                exp_type = col3.selectbox("Expense Type", options=["DR", "CR"])

                def submit_handler(**kwargs):
                    NetworkClient.post_request(
                        url=f"{os.getenv('SERVER_URL')}{
                            os.getenv('TRANSACTION_PATH')}/add/new",
                        frame=kwargs
                    )

                submitted = st.form_submit_button(
                    "Add Expense", use_container_width=True
                )

                if submitted:
                    submit_handler(**{
                        '_id': uuid4(),
                        "amount": amount,
                        "tx_type": exp_type,
                        "vendor": vendor_name,
                        "date": exp_date,
                        "category": category,
                        "vendor_id": vendor_id,
                        "is_deleted": False
                    })

    return context['date_filters']
