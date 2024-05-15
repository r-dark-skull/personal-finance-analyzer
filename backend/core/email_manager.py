import os
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from .email_loader import GmailLoader
import server
from typing import List
from models import RawEmail


class EmailManager:
    def __init__(self) -> None:
        self.__loader = GmailLoader()

    async def fetch_and_save_emails(self):
        try:
            emails: List[RawEmail] = await self.__loader.load_emails(
                email=server.credentials.get('info').get('client_email'),
                filter_date=datetime.now().strftime("%Y-%m-%d")
            )

            for mail in emails:

                # recheck : must be always true
                if any(financial_service in mail.sender
                        for financial_service in server.credentials.get('info').get('financial_services')
                       ):

                    email = jsonable_encoder(mail)

                    server.context['database'][
                        os.getenv('MAIL_COLLECTION')
                    ].insert_one(email)
            return True
        except Exception as e:
            return False

    async def email_analyzer(self):
        ...
