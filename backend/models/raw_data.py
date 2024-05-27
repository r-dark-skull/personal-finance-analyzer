import uuid
from pydantic import BaseModel, Field


class RawEmail(BaseModel):
    id: str = Field(alias="_id")
    sender: str = Field(alias='from')
    mail_body: str = Field(alias="body")
    date: str
    is_analyzed: bool = Field(default=False)
    is_transaction: bool | None = Field(default=None)

    class Config:
        populate_by_name = True
