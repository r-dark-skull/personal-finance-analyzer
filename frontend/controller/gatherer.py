import json
import requests


async def data_requester(start_date: str, end_date: str = None) -> list[dict]:
    """Custom Data Fetcher from BackEnd"""
    