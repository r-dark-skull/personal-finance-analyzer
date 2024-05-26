import re
import asyncio
from connections import Gmail
import server
from base64 import b64decode
from bs4 import BeautifulSoup
from models import RawEmail


class GmailLoader:
    def __init__(self) -> None:

        self.__user_id = server.credentials['info']['client_email']

        self.gmail = Gmail(
            credentials=server.credentials['auth']['gmail']['credential'],
            scope=server.credentials['auth']['GMAIL_SCOPE'],
            token=server.credentials['auth']['gmail']['token'],
        )
        self.__service = self.gmail.login()

    def __gmail_part_parser(self, part: dict):
        mime = part.get('mimeType')

        if mime in ['text/plain', 'text/html']:

            text_data = b64decode(
                part.get('body').get('data')
                .replace("-", "+").replace("_", "/")
            ).decode()

            if 'html' in mime:
                soup = BeautifulSoup(text_data, 'lxml')
                text_data = soup.getText().strip().replace("\r\n", "").replace("\n", "")
                # re.sub(r'([a-z])\1+', r'\1', text_data)

            return text_data

    async def __email_parser(self, mail: dict):

        extracted_data = {}
        body = ""

        headers: list = mail.get('payload').get('headers')
        payload_body: dict = mail.get('payload').get('body')
        payload_parts: list = mail.get('payload').get('parts')

        # extracting metadata
        if headers:
            for header in headers:
                if header.get('name') in ["Date", "From"]:
                    extracted_data[header["name"].lower()] = header["value"]
                elif header.get('name') == 'Subject':
                    body += f"Subject : {header['value']}\n\nContent: "

        if not any(financial_service in extracted_data['from']
                   for financial_service in server.credentials.get('info').get('financial_services')
                   ):
            return None

        if payload_parts:
            for part in payload_parts:
                body += self.__gmail_part_parser(part)

            extracted_data["body"] = body

        return RawEmail(**extracted_data)

    async def __email_getter(self, mail_id: str):
        mail = self.__service.users().messages().get(
            userId=self.__user_id, id=mail_id
        ).execute()

        return await self.__email_parser(mail)

    async def load_emails(self, email: str, filter_date: str):
        mail_list = self.__service.users().messages().list(
            userId=self.__user_id,
            q=f"after:{filter_date} "
        ).execute()

        # creating task group
        futures = []

        async with asyncio.TaskGroup() as mail_task_group:
            for mail in mail_list.get('messages'):
                futures.append(
                    mail_task_group.create_task(
                        self.__email_getter(mail.get('id'))
                    )
                )

        return [task.result() for task in futures if task.result() is not None]
