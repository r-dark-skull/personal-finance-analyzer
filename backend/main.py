import asyncio
import json
from router import create_app
import server
from core import GmailLoader
app = create_app()


# loader = GmailLoader()


# async def get_resulls():
#     mails = await loader.load_emails(
#         email="garg.arnav77@gmail.com",
#         filter_date="2024-05-15"
#     )

#     json.dump(mails, open("mails.json", "w"))


# asyncio.run(get_resulls())
