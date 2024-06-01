import os
import aiohttp
import requests
from fastapi.encoders import jsonable_encoder
import pandas as pd


class NetworkClient:
    def __init__(self) -> None:
        self.__base_url = f"{os.getenv('SERVER_URL')}{
            os.getenv('TRANSACTION_PATH')}"

        self.__get_data_url_template = "{base_url}/{start}/{end}"

    async def get_data_for(self, start: str, end: str) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.__get_data_url_template.format(
                    base_url=self.__base_url,
                    start=start,
                    end=end
                )
            ) as response:
                return await response.json()

    @classmethod
    def post_request(cls, url: str, frame: pd.DataFrame | dict):
        if isinstance(frame, pd.DataFrame):
            frame['date'] = frame['date'].dt.strftime("%Y-%m-%d")

            for idx in range(frame.shape[0]):
                requests.post(
                    url=url.replace('[_id]', frame.iloc[idx]['_id']),
                    json=frame.iloc[idx].to_dict()
                )
        else:
            requests.post(
                url=url,
                json=jsonable_encoder(frame)
            )
