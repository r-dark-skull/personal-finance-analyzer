import os
import json
import requests
import pandas as pd
import streamlit as st
from server import context
from controller import NetworkClient


def prepare_options():
    return {
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
            ],
        ),
        "vendor": {
            "label": "Vendor Name"
        },
        "category": st.column_config.SelectboxColumn(
            label="Category",
            required=True,
            options=context.get("categories")
        ),
        "date": st.column_config.DateColumn(
            label="Date"
        ),
        "is_deleted": "Delete?"
    }


async def create_component(frame: pd.DataFrame):
    return st.data_editor(
        frame,
        column_config=prepare_options(),
        disabled=["date", "amount"],
        hide_index=True,
        use_container_width=True
    )


def refresh():
    context['transactions'] = None
    st.rerun()


def save_changes(changes: pd.DataFrame):
    NetworkClient.post_request(
        url=f"{os.getenv('SERVER_URL')}{os.getenv(
            'TRANSACTION_PATH')}/[_id]",
        frame=changes
    )
    refresh()


@st.experimental_dialog("Save Preview", width="large")
def handle_preview(changed_rows: pd.DataFrame):
    st.dataframe(
        changed_rows,
        column_config={
            "_id": None,
            "vendor_id": "Vendor ID",
            "amount": "Amount (INR)",
            "tx_type": "Transaction Type",
            "vendor": "Vendor Name",
            "category": "Category",
            "date": "Date",
            "is_deleted": "Delete?"
        },
        hide_index=True,
        use_container_width=True
    )


def handle_delete_expense(changes: pd.DataFrame):
    NetworkClient.post_request(
        url=f"{os.getenv('SERVER_URL')}{os.getenv(
            'TRANSACTION_PATH')}/delete/[_id]",
        frame=changes
    )
    refresh()


async def get_changes(saved: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:

    if saved.shape != frame.shape:
        refresh()

    elif not saved.equals(frame):
        # extra row in saved
        # extra row in not saved
        # not saved = saved

        # data change in not saved
        # keep changes untill saved
        # as saved -> not saved = saved

        return frame[~frame['_id'].isin(frame.merge(
            saved, how='inner', indicator=False)['_id'])]

    return pd.DataFrame()


async def transaction_table():
    frame: pd.DataFrame = context.get('transactions')
    saved: pd.DataFrame = context.get('saved_transactions')

    frame.sort_values(by='date', inplace=True, ascending=False)
    saved.sort_values(by='date', inplace=True, ascending=False)

    if not frame.empty:
        edited = await create_component(frame)
        context['transactions'] = edited
        changed_rows = await get_changes(saved, edited)

        if not changed_rows.empty:
            _, del_col, prev_col, col = st.columns(4)

            if del_col.button(
                label="Delete Expense",
                use_container_width=True,
            ):
                handle_delete_expense(**{
                    "changes": changed_rows[changed_rows['is_deleted'] == True]
                })

            if prev_col.button(
                label="Show Preview",
                use_container_width=True,
            ):

                handle_preview(**{
                    'changed_rows': changed_rows
                })

            if col.button(
                label="Save",
                type='primary',
                use_container_width=True,
            ):
                save_changes(**{
                    "changes": changed_rows
                })
