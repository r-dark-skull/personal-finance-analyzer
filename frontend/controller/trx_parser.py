import pandas as pd
from logging import getLogger

logger = getLogger(__name__)


class TxParser:
    def __init__(self) -> None:
        pass

    async def __apply_amount_properties(self, dframe: pd.DataFrame):
        # negative credit amount
        dframe.loc[dframe['tx_type'] == 'CR', 'amount'] *= -1

        # amount round to 2 digits
        dframe['amount'] = dframe['amount'].round(2)

    async def __apply_date_properties(self, dframe: pd.DataFrame):
        dframe['date'] = pd.to_datetime(dframe['date'])

    async def parse_json(self, js_data: list | dict) -> pd.DataFrame:
        try:
            dframe = pd.DataFrame(js_data)
            assert not dframe.empty

            # trx type based amount modification
            await self.__apply_amount_properties(dframe)

            # date modification
            await self.__apply_date_properties(dframe)

            return dframe

        except AssertionError as ase:
            logger.error(ase)
            logger.error(
                f"Got empty transaction data set! No Transactions to load"
            )
        except Exception as e:
            logger.error(e)

        return pd.DataFrame()
