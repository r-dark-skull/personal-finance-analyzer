import pandas as pd
from datetime import date, timedelta
from .gatherer import data_requester
from dateutil.relativedelta import relativedelta


async def categorical_summation(js_data: dict) -> list[dict]:
    dataframe = pd.DataFrame(js_data)

    grouped_data = dataframe.groupby("category").sum('amount').reset_index()
    grouped_data.rename(columns={"category": "name",
                                 "amount": "value"}, inplace=True)

    return grouped_data.to_dict(orient='records')


async def calculate_metrices(current_month, current_week, previous_month, previous_week):
    current_month = pd.DataFrame(current_month)
    current_week = pd.DataFrame(current_week)
    previous_month = pd.DataFrame(previous_month)
    previous_week = pd.DataFrame(previous_week)

    current_month_sum = current_month['value'].sum()
    previous_month_sum = previous_month["value"].sum()

    current_week_sum = current_week['value'].sum()
    previous_week_sum = previous_week['value'].sum()

    curren_week_dominant_catg = current_week[current_week.value == current_week.value.max(
    )].name.values[0]
    previous_week_catg_value = previous_week[previous_week.name ==
                                             curren_week_dominant_catg].value.values[0]

    curren_month_dominant_catg = current_month[current_month.value == current_month.value.max(
    )].name.values[0]
    previous_month_catg_value = previous_month[previous_month.name ==
                                               curren_week_dominant_catg].value.values[0]

    return {
        "current_month": {
            "value": current_month_sum,
            "delta": current_month_sum - previous_month_sum
        },
        "current_week": {
            "value": current_week_sum,
            "delta": current_week_sum - previous_week_sum
        },
        "month_category": {
            "value": current_month.value.max(),
            "delta": current_month.value.max() - previous_month_catg_value,
            "category": curren_month_dominant_catg
        },
        "week_category": {
            "value": current_week.value.max(),
            "delta": current_week.value.max() - previous_week_catg_value,
            "category": curren_week_dominant_catg
        }
    }


async def apply_aggrigations(date_range: tuple[date]) -> tuple:

    today_date = date.today()
    weekday = today_date.isoweekday()
    start_of_week = today_date - timedelta(days=weekday - 1)
    start_of_month = today_date.replace(day=1)

    end_of_previous_week = start_of_week - timedelta(days=1)
    start_of_previous_week = end_of_previous_week - timedelta(days=6)

    previous_month = start_of_month - relativedelta(days=1)
    start_of_previous_month = previous_month.replace(day=1)
    end_of_previous_month = previous_month

    # current week data
    week_data = await categorical_summation(
        await data_requester(
            start_date=start_of_week,
            end_date=today_date
        )
    )

    # current month data
    current_month_transactions = await data_requester(
        start_date=start_of_month,
        end_date=today_date
    )

    month_data = await categorical_summation(
        current_month_transactions
    )

    # previous week data
    previous_week = await categorical_summation(
        await data_requester(
            start_date=start_of_previous_week,
            end_date=end_of_previous_week
        )
    )

    # previous month
    previous_month = await categorical_summation(
        await data_requester(
            start_date=start_of_previous_month,
            end_date=end_of_previous_month
        )
    )

    metrices = await calculate_metrices(
        current_month=month_data,
        current_week=week_data, previous_month=previous_month,
        previous_week=previous_week
    )

    return metrices, week_data, month_data, pd.DataFrame(current_month_transactions)
