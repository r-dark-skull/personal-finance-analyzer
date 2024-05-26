import pandas as pd
import streamlit as st


async def change_handler(edited_rows: pd.DataFrame):
    print(edited_rows)
    ...


async def transaction_table(transaction_data: pd.DataFrame):
    with st.container():
        st.write("## Transactions")

        edited = st.data_editor(
            transaction_data, num_rows="fixed",
            column_config={
                "_id": None,
                "vendor_id": None,
                "amount": {
                    "label": "Amount (INR)",
                },
                "tx_type": st.column_config.SelectboxColumn(
                    label="Transaction Type",
                    required=True,
                    options=[
                        "DR",
                        "CR"
                    ]
                ),
                "vendor": {
                    "label": "Vendor Name"
                },
                "category": st.column_config.SelectboxColumn(
                    label="Category",
                    required=True,
                    options=[
                        "Food",
                        "Entertainment",
                        "Travel",
                        "Shopping",
                        "Clothes",
                        "Study",
                        "Unknown"
                    ]
                ),
                "date": st.column_config.DateColumn(
                    label="Date"
                )
            },
            disabled=["date", "amount"],
            hide_index=True,
        )

        changed_rows = edited[(edited != transaction_data).any(axis=1)]

        await change_handler(changed_rows)
