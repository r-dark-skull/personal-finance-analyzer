import asyncio
import logging
from controller import TxController
from components import *
import streamlit as st


logging.basicConfig(level=logging.INFO)

tx_client = TxController()


def header():
    st.write("# Personal Finance Analyzer")


async def run():
    header()

    filter = await render_side_nav()
    await tx_client.set_date_range(*filter)
    await display_metrics()
    await categorical_chart()
    await daily_expenditure_chart()
    await transaction_table()


asyncio.run(run())
