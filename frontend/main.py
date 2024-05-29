
import asyncio
import json
import pandas as pd
import streamlit as st
from components import *
from controller import apply_aggrigations, data_requester


def header():
    st.write("# Personal Finance Analyzer")


async def run():
    header()

    date_filters = await render_side_nav()

    metrics_data, weekly_data, monthly_data, transactional_data = await apply_aggrigations(date_filters)

    await display_metrics(metrics_data)
    await weekly_chart(weekly_data)
    await monthly_chart(monthly_data)
    await transaction_table(transactional_data)


asyncio.run(run())
