import json
import os
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from .email_loader import GmailLoader
import server
from typing import List
from models import RawEmail, Transaction
from connections import OpenAiConnect


class EmailManager:
    def __init__(self) -> None:
        self.__loader = GmailLoader()
        self.ai_connect = OpenAiConnect()

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

    async def __un_analyzed_mails(self) -> List[RawEmail]:
        return [
            RawEmail(**document)
            for document in server.context.get('database')[
                os.getenv('MAIL_COLLECTION')].find({
                    "is_analyzed": False
                })
        ]

    async def email_analyzer(self):
        mails_to_analyze = await self.__un_analyzed_mails()

        for mail in mails_to_analyze:
            js_response = json.loads(
                self.ai_connect.get_analysis(mail.mail_body)
            )

            js_response['date'] = datetime.strptime(
                js_response['date'], "%Y-%m-%d"
            )
            js_response['id'] = mail.id

            trx = jsonable_encoder(Transaction(**js_response))
            server.context['database'][
                os.getenv('TRANSACTION_COLLECTION')
            ].insert_one(trx)
