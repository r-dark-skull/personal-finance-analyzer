import pandas as pd
from datetime import date
from server import context


class TxAnalyzer:

    async def __calc_total_amount(self, dframe: pd.DataFrame):
        context['metrices']['total_sum'] = dframe['amount'].sum()

    async def __calc_max_category_amount(self, dframe: pd.DataFrame):
        grouped = dframe.groupby('category')['amount'].sum().reset_index()
        max_data = grouped.loc[grouped['amount'].idxmax()]

        context['catg_tsx'] = grouped.rename(
            columns={"category": "name", "amount": "value"}
        )
        context['metrices']['max_catg'] = max_data

    async def __calc_top_time_amount(self, dframe: pd.DataFrame, start: date, end: date):
        t_grouped = dframe.groupby('date')['amount'].sum().reset_index()
        max_day_exp = t_grouped.loc[t_grouped['amount'].idxmax()]

        context['daily_tsx'] = t_grouped.rename(
            columns={"date": "name", "amount": "value"}
        )
        context['metrices']['max_daily'] = max_day_exp

    async def analyze(self, dframe: pd.DataFrame, start_date: date, end_date: date):

        context['metrices'] = {}
        context['categories'].update(dframe['category'].unique())

        await self.__calc_total_amount(dframe)
        await self.__calc_max_category_amount(dframe)
        await self.__calc_top_time_amount(dframe, start_date, end_date)
