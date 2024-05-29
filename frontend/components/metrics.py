import streamlit as st


async def display_metrics(metric_data: dict):

    with st.container():
        st.write("## Expense Quick Lookup")

        columns = st.columns(4)

        columns[0].metric(
            label="Current Month Expense",
            value=metric_data['current_month']['value'], delta=metric_data['current_month']['delta'], delta_color="inverse"
        )

        columns[1].metric(
            label="Current Week Expense",
            value=metric_data['current_week']['value'], delta=metric_data['current_week']['delta'], delta_color="inverse"
        )

        columns[2].metric(
            label="Food (Month)",
            value=metric_data['month_category']['value'], delta=metric_data['month_category']['delta'], delta_color="inverse"
        )

        columns[3].metric(
            label="Travel (Week)",
            value=metric_data['week_category']['value'], delta=metric_data['week_category']['delta'], delta_color="inverse"
        )
