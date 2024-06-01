import asyncio
import pandas as pd
from datetime import date
from .network import NetworkClient
from .trx_parser import TxParser
from .analyzer import TxAnalyzer
from server import context
from logging import getLogger


logger = getLogger(__name__)


class TxController:
    def __init__(self) -> None:
        self.__end_date = date.today()
        self.__start_date = self.__end_date.replace(day=1)

        self.__nwc = NetworkClient()
        self.__processor = TxParser()
        self.__analyzer = TxAnalyzer()

    async def __refresh(self):

        try:
            dframe: pd.DataFrame = await self.__processor.parse_json(
                await self.__nwc.get_data_for(
                    start=self.__start_date,
                    end=self.__end_date
                )
            )

            assert not dframe.empty

            # analyze the data
            await self.__analyzer.analyze(dframe, self.__start_date, self.__end_date)

            if context.get('transactions') is None:
                context['transactions'] = dframe
            context['saved_transactions'] = dframe

        except Exception as e:
            logger.error(e)

    async def set_date_range(self, start: date = None, end: date = None):
        self.__start_date = start or date.today()
        self.__end_date = end or date.today()

        await self.__refresh()
