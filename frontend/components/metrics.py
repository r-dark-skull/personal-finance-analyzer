import streamlit as st
from server import context


async def display_metrics():
    metric_data = context.get('metrices')

    if metric_data:
        with st.container():
            st.write("## Expense Quick Lookup")

            columns = st.columns(3)

            columns[0].metric(
                label="Total Expense",
                value=round(metric_data['total_sum'], 2)
            )

            columns[1].metric(
                label="Top Category ("
                f"{metric_data['max_catg']['category']}"
                ")",
                value=round(metric_data['max_catg']['amount'], 2)
            )

            columns[2].metric(
                label="Most Expensive day ("
                f"{metric_data['max_daily']['date'].strftime('%b %d')}"
                ")",
                value=round(metric_data['max_daily']['amount'], 2)
            )
