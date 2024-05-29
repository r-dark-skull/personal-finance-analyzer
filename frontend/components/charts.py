from streamlit_echarts import st_echarts as ste
import streamlit as st


def get_chart_layout(title: str, data: list[dict]) -> dict:

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
        "visualMap": {
            "show": False,
            "min": 300,
            "max": 1600,
            "inRange": {
                "color": ["#ffc40c", "#E74C3C", "#212F3D"]
            }
        },
        "series": [
            {
                "name": 'Access From',
                "type": 'pie',
                "radius": '55%',
                "selectedMode": 'multiple',
                "center": ['50%', '50%'],
                "data": data,
                "roseType": 'radius',
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
                "itemStyle": {
                },
                "animationType": 'scale',
                "animationEasing": 'elasticOut'
            }
        ]
    }


async def weekly_chart(weekly_data: list[dict]):

    with st.container():
        st.write("## Weekly Expense Chart")

        chart_options = get_chart_layout("Weekly Expense", weekly_data)
        ste(options=chart_options, height="600px")


async def monthly_chart(monthly_data: list[dict]):

    with st.container():
        st.write("## Monthly Expense Chart")

        chart_options = get_chart_layout("Monthly Expense", monthly_data)
        ste(options=chart_options, height="600px")
