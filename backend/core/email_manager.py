import json
import os
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from .email_loader import GmailLoader
import server
from typing import List
from models import RawEmail, Transaction
from connections import OpenAiConnect

from logging import getLogger

logger = getLogger(__name__)


class EmailManager:
    def __init__(self) -> None:
        self.__loader = GmailLoader()
        self.ai_connect = OpenAiConnect()

    async def fetch_and_save_emails(self, start_date: str, end_date: str = None):
        try:
            emails: List[RawEmail] = await self.__loader.load_emails(
                email=server.credentials.get('info').get('client_email'),
                filter_date=start_date
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
            logger.error(e)
            return False

    async def __un_analyzed_mails(self) -> List[RawEmail]:
        return [
            RawEmail(**document)
            for document in server.context.get('database')[
                os.getenv('MAIL_COLLECTION')].find({
                    "is_analyzed": False
                })
        ]

    # async def categorizer(self, js_response: dict) -> str | None:

    #     vendor_id = js_response['vendor_id']
    #     document = server.context['database'][
    #         os.getenv('CATEGORY_COLLECTION')
    #     ].find({"vendor_id": vendor_id})

        # if js_response['category'].lower() != "unknown":
        #     ...
        # else:
        #     ...

    async def email_analyzer(self):
        mails_to_analyze = await self.__un_analyzed_mails()

        for mail in mails_to_analyze:
            js_response = json.loads(
                self.ai_connect.get_analysis(mail.mail_body)
            )

            if len(js_response):

                js_response['date'] = datetime.strptime(
                    js_response['date'], "%Y-%m-%d"
                )
                js_response['id'] = mail.id

                # getting and saving category
                # category = await self.email_analyzer(js_response)

                trx = jsonable_encoder(Transaction(**js_response))
                server.context['database'][
                    os.getenv('TRANSACTION_COLLECTION')
                ].insert_one(trx)
