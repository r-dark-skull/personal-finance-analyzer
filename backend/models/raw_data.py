from pydantic import Field
from base import MongoDocument


class RawEmail(MongoDocument):
    sender: str = Field(alias='from')
    mail_body: str = Field(alias="body")
    date: str
    is_analyzed: bool = Field(default=False)
    is_transaction: bool | None = Field(default=None)
