import asyncio
from connections import Gmail
import server
from base64 import b64decode
from bs4 import BeautifulSoup
from models import RawEmail
from pydantic import ValidationError
from hashlib import sha256

from logging import getLogger

logger = getLogger(__name__)


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
        else:
            logger.warning(f"MIME TYPE not in html/text : {mime}")
            logger.debug(f"{part}")
            return None

    def __create_mail_id(self, mail_body: str, date: str, sender: str) -> str:
        text = f"MAIL BODY: {mail_body}\nOnDate: {date}\nSender: {sender}"
        return sha256(text.encode()).hexdigest()

    async def __email_parser(self, mail: dict, mail_id: str):
        extracted_data = {}
        body = ""
        try:
            headers: list = mail.get('payload').get('headers')
            payload_body: dict = mail.get('payload').get('body')
            payload_parts: list = mail.get('payload').get('parts')

            # extracting metadata
            if headers:
                for header in headers:
                    if header.get('name') in ["Date", "From"]:
                        extracted_data[header["name"].lower()
                                       ] = header["value"]
                    elif header.get('name') == 'Subject':
                        body += f"Subject : {header['value']}\n\nContent: "

            if not any(financial_service in extracted_data['from']
                       for financial_service in server.credentials.get('info').get('financial_services')
                       ):
                return None

            if payload_parts:
                for part in payload_parts:
                    body += self.__gmail_part_parser(part) or ""

                extracted_data["body"] = body

                try:

                    mid = self.__create_mail_id(
                        mail_body=extracted_data['body'],
                        date=extracted_data['date'],
                        sender=extracted_data['from']
                    )

                    return RawEmail(_id=mid, **extracted_data)
                except ValidationError as ve:
                    logger.error(
                        f"Validation Error in Raw Email for MAIL ID - [{mail_id}] : {ve}")
                    with open("/develop/cache/validation_errors.log", "a") as ve_file:
                        ve_file.write(f"{mail_id}\n")
        except Exception as e:
            logger.error(
                f"Error in Email Parser : {e}"
            )
            raise e

    async def __email_getter(self, mail_id: str):

        try:
            mail = self.__service.users().messages().get(
                userId=self.__user_id, id=mail_id
            ).execute()
        except Exception as e:
            logger.error(f"Error in Email Getter : {e}")
            raise e

        return await self.__email_parser(mail, mail_id)

    async def load_emails(self, start_date: str, end_date: str = None):

        mail_list = []
        nextPageToken = ""

        filter_string = f"after:{start_date} before:{end_date}" \
            if end_date else f"after: {start_date}"

        while nextPageToken is not None:
            resp = self.__service.users().messages().list(
                userId=self.__user_id,
                maxResults=500,
                pageToken=nextPageToken,
                q=filter_string
            ).execute()

            mail_list += resp.get('messages')
            nextPageToken = resp.get('nextPageToken')
            # nextPageToken = None

        logger.debug(f"Total Number of Mails : {len(mail_list)}")
        logger.debug(f"Mail Ids: {mail_list}")

        # creating task group
        futures = []
        try:
            async with asyncio.TaskGroup() as mail_task_group:
                for mail in mail_list:
                    futures.append(
                        mail_task_group.create_task(
                            self.__email_getter(mail.get('id'))
                        )
                    )
        except Exception as e:
            logger.error(
                f"Error in Loading Emails : {e}"
            )
            raise e

        return [task.result() for task in futures if task.result() is not None]
