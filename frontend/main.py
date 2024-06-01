from dotenv import load_dotenv
load_dotenv()

from controller import TxController
from components import *
import streamlit as st
import pandas as pd
from datetime import date
import asyncio

import logging


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
