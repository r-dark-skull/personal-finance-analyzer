import pandas as pd
from streamlit_echarts import st_echarts as ste
import streamlit as st
from server import context


def get_pie_chart_layout(title: str, data: list[dict]) -> dict:
    return {
        "title": {
            "text": title,
            "left": 'center',
            "top": 20,
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "series": [
            {
                "name": title,
                "type": 'pie',
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": True,
                "itemStyle": {
                },
                "emphasis": {
                    "label": {"show": True, "fontWeight": "bold"}
                },
                "selectedMode": 'multiple',
                "data": data,
                "label": {
                    "formatter": ' {b}: {c} - {d}% ',
                },
                "labelLine": {
                    "lineStyle": {
                    },
                    "smooth": 0.2,
                    "length": 10,
                    "length2": 20
                },
                "animationType": 'scale',
                "animationEasing": 'elasticOut'
            }
        ]
    }


def get_line_chart_layout(title: str, dframe: pd.DataFrame, xaxis_label: str, yaxis_label: str):
    return {
        "title": {
            "text": title,
            "left": 'center',
            "top": 20,
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "xAxis": {
            "type": 'category',
            "data": dframe[xaxis_label].tolist()
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [
            {
                "data": dframe[yaxis_label].tolist(),
                "type": 'line'
            }
        ]
    }


async def categorical_chart():
    categorical_data: pd.DataFrame = context.get("catg_tsx")

    if not categorical_data.empty:
        with st.container():
            st.write("## Categorical Expense")

            chart_options = get_pie_chart_layout(
                "Categorical Expense", categorical_data.to_dict(orient='records'))
            ste(options=chart_options, height="600px")


async def daily_expenditure_chart():
    daily_data: pd.DataFrame = context.get('daily_tsx')
    daily_data.sort_values(by='name', ascending=True, inplace=True)

    daily_data["name"] = daily_data["name"].apply(
        lambda x: x.strftime('%b %d')
    )

    if not daily_data.empty:
        with st.container():
            st.write("## Daily Expenditure Chart")

            chart_options = get_line_chart_layout(
                title="Daily Expenditure",
                dframe=daily_data,
                xaxis_label="name",
                yaxis_label="value"
            )
            ste(options=chart_options, height="600px")
